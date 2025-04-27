# pip install -q -U google-genai to use gemini as a client
import json
import sys
from typing import Optional

from agent.tavily_agent import tavily_search
from utils.data_back_util import append_string_to_json_file, append_to_json_file, JSON_FILE
sys.path.append('./libraries/PathRAG')

import os
import numpy as np
from google import genai
from google.genai import types
from dotenv import load_dotenv
from utils.constants import MODEL_ID

from libraries.PathRAG.PathRAG.utils import EmbeddingFunc
from libraries.PathRAG.PathRAG import PathRAG, QueryParam
from libraries.PathRAG.PathRAG.llm import ollama_embed
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from langchain_google_genai import ChatGoogleGenerativeAI
from sentence_transformers import SentenceTransformer



import nest_asyncio

# Apply nest_asyncio to solve event loop issues
nest_asyncio.apply()

load_dotenv()
gemini_api_key = os.getenv("GOOGLE_API_KEY")
WORKING_DIR = "./knowledge_base/path_rag"

llm = ChatGoogleGenerativeAI(model=MODEL_ID, temperature=0.0)

async def llm_model_func(
    prompt, system_prompt=None, history_messages=[], keyword_extraction=False, **kwargs
) -> str:
    # 1. Initialize the GenAI Client with your Gemini API Key
    client = genai.Client(api_key=gemini_api_key)

    # 2. Combine prompts: system prompt, history, and user prompt
    if history_messages is None:
        history_messages = []

    combined_prompt = ""
    if system_prompt:
        combined_prompt += f"{system_prompt}\n"

    for msg in history_messages:
        # Each msg is expected to be a dict: {"role": "...", "content": "..."}
        combined_prompt += f"{msg['role']}: {msg['content']}\n"

    # Finally, add the new user prompt
    combined_prompt += f"user: {prompt}"

    # 3. Call the Gemini model
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=[combined_prompt],
        config=types.GenerateContentConfig(max_output_tokens=500, temperature=0.1),
    )

    # 4. Return the response text
    return response.text

async def embedding_func(texts: list[str]) -> np.ndarray:
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(texts, convert_to_numpy=True)
    return embeddings

def initialize_rag():
    rag = PathRAG(
        working_dir=WORKING_DIR,
        llm_model_func=llm_model_func,
        embedding_func=EmbeddingFunc(
            embedding_dim=384,
            max_token_size=8192,
            func=embedding_func,
        ),
    )

    return rag

# Initialize RAG instance
rag = initialize_rag()

def format_result(result):
    from datetime import date

    today = date.today().isoformat()
    text = f"Title: {result['title']}\nURL: {result['url']}\nContent: {result['content']}\nDateAdded: {today}"
    print(f"Text to insert: {text}")
    return text


class AgentState(BaseModel):
    history: list
    compiled_history: Optional[str]
    query: str
    rag_response: Optional[str]
    tavily_response: Optional[str]
    response: Optional[str]

async def get_previous_user_query(state: AgentState):
    # Extract the last user message from the history
    formatted_history = ""
    if isinstance(state.history, list):
        for msg in state.history:
                if msg.get("role") == "user":
                    role = msg.get("role", "user").capitalize()
                    content = msg.get("message", "")
                    formatted_history += f"{role}: {content}\n"

    return formatted_history

async def starting(state: AgentState):
    prompt = ChatPromptTemplate.from_messages(
    [
            ("system", """You are a helpful assistant. The user will first ask a question and then ask a follow-up question. You need to complete the new query by combining the information from both the old and new queries. 
    If the new query contains new details, you should integrate them into the old query context to provide a more specific query.
    For example:
    - First Query: "Find Java jobs"
    - Second Query: "In Bangalore"
    Resulting query: "Find Java jobs in Bangalore"
    Your job is to gather details from both queries and complete the current user query by including the relevant details from the first query."""),
            
            # Older query
            ("user", "Old query: {old_query}"),
            
            # New query
            ("user", "New query: {new_query}"),
        ]
    )
#     prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system", """You are a helpful assistant.

# The user will ask an initial query and then follow up with another query.

# - If the second query is closely related to the first query (same subject/topic), you must combine details from both to form a complete query.
# - If the second query is about a **completely different topic**, you must **ignore the old query** and treat the new query as a fresh query.

# Examples:
# - Old query: "Find Java jobs"
# - New query: "In Bangalore"
# Result: "Find Java jobs in Bangalore"

# - Old query: "Find React jobs"
# - New query: "Check upcoming AI events"
# Result: "Check upcoming AI events"

# Always first check if the new query is related to the old query. If unrelated, only use the new query."""),

#         # Older query
#         ("user", "Old query: {old_query}"),

#         # New query
#         ("user", "New query: {new_query}"),
#     ]
# )
    old_query = await get_previous_user_query(state)
    prompt_input = prompt.format_prompt(old_query=old_query, new_query=state.query, completed_query="")

    # Get the response from the language model
    response = llm.invoke( prompt_input)
    state.query = response.content
    print("---")
    print(f"Updated query: {state.query}")
    print("---")
    return state

async def invalid(state: AgentState):
    state.response = "Your query is out of scope. Please ask something related to jobs, careers, professional events, or communities."
    return state

async def is_valid(state: AgentState):
    prompt = """
system:
Check older chat history and the query analyze both and If the query is related to older history and/or jobs, careers, professional events, or communities, then return "valid" or "invalid" otherwise.
Important: Only return "valid" or "invalid" without any additional text or explanation.
---
user_query:
{user_query}
"""
    history = state.history
    formatted_history = await get_previous_user_query(state)

    formatted_history = f"{formatted_history}\nuser: {state.query}"
    print("---")
    print(f"is valid Formatted history: {formatted_history}")
    print("---")
    print(f"User query: {state.query}")
    print("---")
    prompt = prompt.format(user_query=state.query)
    response = await llm.ainvoke(prompt)
    if response.content == "valid":
        return "query_rag"
    else:
        return "invalid"

async def run_query_rag(state: AgentState):
    query = state.query
    compiled_history = state.compiled_history
    
    prompt = """
Chat history summary:
{compiled_history}
User Query:
{query}
"""
    prompt = prompt.format(compiled_history=compiled_history, query=query)
    response = await rag.aquery(prompt, param=QueryParam(mode="hybrid"))

    state.rag_response = response
    return state

async def tavily_search_agent(state: AgentState):
    prompt = """
Previous User Query:
{compiled_history}
Current User Query:
{query}
"""
    prompt = prompt.format(compiled_history=state.compiled_history, query=state.query)
    out = await tavily_search("12345", prompt, state.compiled_history)
    print("---")
    print(f"Tavily Search Result: {out}")
    print("---")
    state.tavily_response = out
    append_string_to_json_file(JSON_FILE, state.tavily_response)
    return state

async def run_response_summarize(state: AgentState):

    prompt_template = """
System:
You are a professional and intelligent assistant that shows the web search data and internal data results to the user. Your goal is to provide the user with relevant information about jobs, careers, professional events, or communities.:

Your tasks:
1. Analyze the user's query and review the previous chat summary.
2. If the query is related to jobs, careers suggestions, professional events, or communities:
    - Present information from **both Web Search Result and Internal Data Result**.
    - Prioritize Web Search Result always.
    - Do not mention if any result lacks data; simply show the available information.
    - Avoid displaying duplicate items between Web Search Result and Internal Data Result.
    - Show all the available results and links dont omit any.
3. Format the response using **clean Markdown**:
    - Use **clear headings** for each result.
    - Use **bullet points** for listing items.
    - Use **clickable links** in `[Text](URL)` format.
4. If the query is **not related** to jobs, careers, events, or professional communities:
    - Politely inform the user that the query is out of scope.
    - Suggest asking something career- or job-related.

Response Guidelines:
- **Do not** explain how the data was collected or refer to internal data.
- **Do not** mention any internal results like "Web Search Result" or "Internal Data Result."
- **Do not** mention internal systems, APIs, or reasoning steps.
- **Do not** introduce any bias based on gender, culture, or background.
- **Do not** use casual, humorous, or disrespectful tone.
- Maintain a **professional, respectful, and helpful tone** at all times.
---
## User Query:
{user_query}
---
## Web Search Result:
{result_1}


    """

    query = state.query
    rag_text = state.rag_response

    tavily_result = state.tavily_response
    # tavily_text = json.dumps(tavily_result, indent=2)

    tavily_text = ""
    if isinstance(tavily_result, list):
        for item in tavily_result:
            
            tavily_text += format_result(item) + "\n\n"
    else:
        tavily_text = tavily_result  # if already a string (e.g., summarized)

    prompt = prompt_template.format(user_query=query, 
                                    compiled_history=state.compiled_history, 
                                    result_1=tavily_text, result_2=rag_text)
    print(f"Prompt: {prompt}")
    response = await llm.ainvoke(prompt)
    state.response = response.content
    return state


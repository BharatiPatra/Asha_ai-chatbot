import json
from langchain_tavily import TavilySearch
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from utils.constants import MODEL_ID
from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory



load_dotenv()

# Initialize Tavily Search Tool
tavily_search_tool = TavilySearch(
    max_results=10,
    topic="general",
    search_depth="advanced",
)

llm = ChatGoogleGenerativeAI(model=MODEL_ID, temperature=0.0)
tools = [tavily_search_tool]
prompt = ChatPromptTemplate.from_messages(
    [
            ("system", """You are a helpful assistant that have search information of user query from  Web Search. You dont need to search anything.
You just need to format the result and summarize them. If results available then list all the available result with their links"""),
            
            ("user", "Web Search Result: {result}"),
            
            ("user", "{user}"),

        ]
    )

async def tavily_search(
    session_id: str,
    user_input: str,
    chat_history: str,
) -> list:
    tavily_out = await tavily_search_tool.ainvoke(
        user_input
    )
    tavily_result = tavily_out.get("results", [])
    tavily_text = json.dumps(tavily_result, indent=2)

    formatted_prompt = prompt.format_prompt(
        user=user_input,
        result=tavily_text,
    )
    out = await llm.ainvoke(
        formatted_prompt,
    )
    

    print("---")
    print(f"tavily output: {out}")
    print("---")
    return out.content
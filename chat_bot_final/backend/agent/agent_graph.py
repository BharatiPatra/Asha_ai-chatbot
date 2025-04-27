from langgraph.graph import StateGraph, END
from agent.agents import AgentState, starting, is_valid, invalid, run_query_rag, run_response_summarize, tavily_search_agent

builder = StateGraph(AgentState)

# Add nodes
builder.add_node("entry", starting)
builder.add_node("invalid", invalid)
builder.add_node("query_rag", run_query_rag)
builder.add_node("tavily", tavily_search_agent)
builder.add_node("response_summarize", run_response_summarize)

# Set up transitions
builder.set_entry_point("entry")
builder.add_conditional_edges(
    "entry", is_valid
)
builder.add_edge("invalid", END)
builder.add_edge("query_rag", "tavily")
builder.add_edge("tavily", "response_summarize")
builder.add_edge("response_summarize", END)

# Step 3: Compile the graph
agent_graph = builder.compile()
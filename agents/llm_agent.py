from dotenv import load_dotenv
import os
from typing_extensions import TypedDict
from typing import Annotated

from langgraph.graph import START, END, StateGraph
from langchain_groq import ChatGroq
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

from agents.tools import install_software

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

# ---- Groq LLM ----
llm = ChatGroq(
    model="qwen/qwen3-32b",
    api_key=groq_api_key
)

tools = [install_software]

# Bind tool
llm_with_tools = llm.bind_tools(tools)

### State Schema
class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

# ---- Node: LLM handles everything ----
def llm_node(state: State):
    """LLM either answers directly or triggers tool"""
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

# ---- Build agent ----
def build_agent():
    graph = StateGraph(State)

    graph.add_node("llm", llm_node)
    graph.add_node("tools", ToolNode(tools))

    graph.set_entry_point("llm")

    # Conditional edge
    def route_llm(state: State):
        last_msg = state["messages"][-1]
        if getattr(last_msg, "tool_calls", None):  # LLM requested a tool
            return "tools"
        return END   # No tool call → stop

    graph.add_conditional_edges("llm", route_llm, {"tools": "tools", END: END})
    graph.add_edge("tools", "llm")   # After tool runs, return to LLM

    return graph.compile()
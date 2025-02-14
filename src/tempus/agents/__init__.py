from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_core.messages import ToolMessage
from langgraph.prebuilt import ToolNode
from src.tempus.utils import extract_contract_address_and_ticker
from src.tempus.data_processing.data_processing import process_contract, process_ticker
from src.tempus.agents.quant_agent import quant_agent
from langchain_openai import ChatOpenAI
import json

llm = ChatOpenAI(model="gpt-4o-mini")

workflow = StateGraph(MessagesState)

def call_model(state: MessagesState):
    messages = state["messages"]
    model_with_tools = llm.bind_tools([extract_contract_address_and_ticker])
    response = model_with_tools.invoke(messages)
    return {"messages": [response]}

def route_tools(state: MessagesState) -> str:
    """
    Routes the tool output to the correct processing function.
    Ensures a valid return value to prevent KeyError.
    """
    tool_message = state.get("messages", [])[-1]  # Get the last message
    if not isinstance(tool_message, ToolMessage):
        return END  # Ensure a valid return type
    
    try:
        content = json.loads(tool_message.content)
    except json.JSONDecodeError:
        return END  # Handle JSON decoding errors gracefully

    contract_address = content.get("contract_address")
    ticker = content.get("ticker")

    if contract_address and not ticker:
        return "process_contract"
    elif ticker and not contract_address:
        return "process_ticker"
    else:
        return END  # Default case to prevent KeyError

# Define the two nodes we will cycle between
workflow.add_node("agent", call_model)
workflow.add_node("extract_contract_address_and_ticker", ToolNode([extract_contract_address_and_ticker]))
workflow.add_node("process_contract", process_contract)
workflow.add_node("process_ticker", process_ticker)
workflow.add_node("quant_agent", quant_agent)

# Define routing node with conditional edges
workflow.add_edge(START, "agent")
workflow.add_edge("agent", "extract_contract_address_and_ticker")
workflow.add_conditional_edges(
    "extract_contract_address_and_ticker",
    route_tools,
    {"process_contract": "process_contract",
    "process_ticker": "process_ticker", 
    END: END},
)
workflow.add_edge("process_contract", "quant_agent")
workflow.add_edge("process_ticker", "quant_agent")
workflow.add_edge("quant_agent", END)

# Compile the workflow
graph = workflow.compile()

from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from langgraph.graph import MessagesState
import json

QUANT_AI_PROMPT = """
Role: 
You are a Quant AI Agent specialized in analyzing historical cryptocurrency data. Your primary goal is to provide insights and generate reports based on the trends and patterns observed in the data.

Instructions:
1. Receive the following historical crypto data as input:
   {historical_data}
2. Analyze the data to identify trends, such as upward or downward movements in prices.
3. Generate a summary report that includes:
   - Average price change over the specified period.
   - Significant trends detected (e.g., bullish or bearish signals).
   - Recommendations based on the analysis (e.g., potential buy/sell signals).

Expected Output:
Your output should be a well-structured report that summarizes the findings from the analysis. The report should be clear and concise, suitable for presentation to stakeholders.
"""

def quant_agent(state: MessagesState):
    """Runs the Quant AI Agent on Dex data using the system prompt."""
    messages = state["messages"]
    tool_message = messages[-1]  # Get the last message containing Dex data
    if not tool_message or not tool_message.content.strip():
        return {"messages": [AIMessage(content="Error: No data available for analysis.")]}
    
    content = tool_message.content

    # Format the historical data into the prompt
    system_prompt = QUANT_AI_PROMPT.format(historical_data=content)

    # Construct messages for LLM
    chat_messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content="Analyze the provided data and generate a report.")
    ]

    # Invoke the model with the Quant AI prompt
    response = llm.invoke(chat_messages)

    return {"messages": [response]}

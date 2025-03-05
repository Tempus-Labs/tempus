"""
Quant Agent for the Tempus framework.
"""
from typing import Dict, Any, List, Optional, Union, Literal, Generator
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.runnables import Runnable, RunnableConfig, RunnableLambda
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from langchain_deepseek import ChatDeepSeek
import uuid
from datetime import datetime

from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime

from ..prompt_templates.quant_ai import *
from ..tools.market_analysis import (
    analyze_contract,
    analyze_ticker,
    analyze_market_trends,
    analyze_meta_market,
    set_llm
)

class QuantAIAgent:
    """
    A chatbot specialized in quantitative analysis of cryptocurrency markets.
    
    Example:
        agent = QuantAIAgent(llm="openai", model_name="gpt-4")
        response = agent.chat("Analyze the BTC market trends")
        print(response)
        
        # Or use streaming
        for chunk in agent.chat_stream("Analyze BTC trends"):
            print(chunk, end="", flush=True)
    """
    
    SUPPORTED_LLMS = {
        "openai": ChatOpenAI,
        "deepseek": ChatDeepSeek
    }
    
    DEFAULT_MODELS = {
        "openai": "gpt-4",
        "deepseek": "deepseek-chat"
    }
    
    def __init__(self, llm_provider: str = "openai", model_name: Optional[str] = None):
        """
        Initialize the Quant AI Agent.
        
        Args:
            llm_provider (str): LLM provider ("openai" or "deepseek")
            model_name (Optional[str]): Name of the model to use. If None, uses the default model for the provider
        """
        if llm_provider not in self.SUPPORTED_LLMS:
            raise ValueError(f"LLM {llm_provider} not supported. Choose from: {list(self.SUPPORTED_LLMS.keys())}")
            
        self.llm_provider = llm_provider
        self.model_name = model_name or self.DEFAULT_MODELS[llm_provider]
        self.thread_id = str(uuid.uuid4())
        self.memory = MemorySaver()
        self.conversation_history = []
        self.config = {
            "configurable": {
                "thread_id": self.thread_id,
            }
        }
        
        # Initialize LLM
        llm_class = self.SUPPORTED_LLMS[llm_provider]
        self.llm = llm_class(
            model=self.model_name
        )
        
        # Set LLM for tools
        set_llm(self.llm)
        
        # Initialize tools
        self.tools = [
            analyze_contract,
            analyze_ticker,
            analyze_market_trends,
            analyze_meta_market
        ]
        
        # Build the graph
        self.graph = self._build_graph()
        
    def _handle_tool_error(state) -> dict:
        error = state.get("error")
        tool_calls = state["messages"][-1].tool_calls
        return {
            "messages": [
                ToolMessage(
                    content=f"Error: {repr(error)}\n please fix your mistakes.",
                    tool_call_id=tc["id"],
                )
                for tc in tool_calls
            ]
        }

    def _create_tool_node_with_fallback(self) -> dict:
        return ToolNode(self.tools).with_fallbacks(
            [RunnableLambda(self._handle_tool_error)], exception_key="error"
        )
        
    def _build_graph(self) -> Runnable:
        """Build the agent's workflow graph."""
        # System prompt for Quant AI Chatbot
        quant_ai_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    QUANT_AI_CHATBOT_PROMPT,
                ),
                ("placeholder", "{messages}"),
            ]
        ).partial(time=datetime.now())

        # Bind tools to the chatbot
        quant_ai_runnable = quant_ai_prompt | self.llm.bind_tools(self.tools)
        workflow = StateGraph(MessagesState)
        
        # Add nodes
        workflow.add_node("agent", Chatbot(quant_ai_runnable))
        workflow.add_node("tools", self._create_tool_node_with_fallback())
        
        # Add edges
        workflow.add_edge(START, "agent")
        workflow.add_conditional_edges(
            "agent",
            tools_condition,
        )
        workflow.add_edge("tools", "agent")
        
        # Add memory checkpointing
        return workflow.compile(checkpointer=self.memory)
        
    def _get_messages_state(self, new_message: str) -> Dict:
        """Get the current conversation state with the new message."""
        messages = self.conversation_history + [HumanMessage(content=new_message)]
        return {
            "messages": messages,
            "configurable": {
                "thread_id": self.thread_id,
                "timestamp": datetime.now().isoformat()
            }
        }
        
    def chat(self, message: str) -> str:
        """
        Send a message to the agent and get a response.
        
        Args:
            message (str): The user's message
            
        Returns:
            str: The agent's response
        """
        
        responses = self.graph.invoke({"messages": ("user", message)}, config=self.config)
        for event in responses['messages']:
            event.pretty_print()
        
        # Extract the latest AI message
        ai_message = None
        for msg in reversed(responses["messages"]):
            if isinstance(msg, AIMessage):
                ai_message = msg
                break
                
        if ai_message:
            # Update conversation history
            self.conversation_history.extend([
                HumanMessage(content=message),
                ai_message
            ])
            return ai_message.content
                
        return "No response generated. Please try again."
        
    def chat_stream(self, user_message: str):
        """
        Send a message to the agent and get a streaming response.
        
        Args:
            message (str): The user's message
            
        Yields:
            str: Chunks of the agent's response
        """
        response_stream = self.graph.stream({"messages": ("user", user_message)}, config=self.config, stream_mode="values")


        current_response = []
        _printed = set()
        for event in response_stream:
            current_state = event.get("dialog_state")
            if current_state:
                print("Currently in: ", current_state[-1])
            message = event.get("messages")
            if message:
                if isinstance(message, list):
                    message = message[-1]
                if message.id not in _printed:
                    current_response.append(message.content)
                    _printed.add(message.id)
                    yield message
        
        # Update conversation history after streaming completes
        if current_response:
            self.conversation_history.extend([
                HumanMessage(content=user_message),
                AIMessage(content="".join(current_response))
            ])
        
    def set_model(self, llm_provider: str, model_name: Optional[str] = None) -> None:
        """
        Change the LLM provider and model.
        
        Args:
            llm (str): LLM provider ("openai" or "deepseek")
            model_name (Optional[str]): Name of the model to use. If None, uses the default model
            
        Raises:
            ValueError: If llm is not supported
        """
        if llm_provider not in self.SUPPORTED_LLMS:
            raise ValueError(f"LLM {llm_provider} not supported. Choose from: {list(self.SUPPORTED_LLMS.keys())}")
            
        self.llm_provider = llm_provider
        self.model_name = model_name or self.DEFAULT_MODELS[llm_provider]
        
        llm_class = self.SUPPORTED_LLMS[llm_provider]
        self.llm = llm_class(
            model=self.model_name
        )
        
        # Update LLM for tools
        set_llm(self.llm)
        
        # Initialize tools
        self.tools = [
            analyze_contract,
            analyze_ticker,
            analyze_market_trends,
            analyze_meta_market
        ]
        
        # Rebuild graph with new tools
        self.graph = self._build_graph()
        
    def clear_history(self) -> None:
        """Clear the conversation history."""
        self.conversation_history = []
        
    @property
    def available_tools(self) -> List[str]:
        """Get list of available tools."""
        return [tool.name for tool in self.tools]

class Chatbot:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    def __call__(self, state, config: RunnableConfig):
        while True:
            result = self.runnable.invoke(state)
            # If the LLM returns an empty response, re-prompt for a real output
            if not result.tool_calls and (
                not result.content
                or isinstance(result.content, list)
                and not result.content[0].get("text")
            ):
                messages = state["messages"] + [("user", "Respond with a real output.")]
                state = {**state, "messages": messages}
            else:
                break
        return {"messages": result}
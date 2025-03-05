"""
Market analysis tools for the Tempus framework.
"""
from typing import Dict, Any
import re
from langchain_core.tools import tool
from ..data.dex_client import DexClient
from ..data.pump_fun_client import PumpFunClient
from ..prompt_templates.quant_ai import *
from langchain.schema import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
import json

# Initialize default LLM
llm = ChatOpenAI(model="gpt-4")

def set_llm(new_llm):
    """Set the LLM instance for all tools."""
    global llm
    llm = new_llm

@tool
def analyze_contract(contract_address: str) -> Dict[str, Any]:
    """
    Analyzes a Solana token contract using DexScreener data.

    Example:
        analyze_contract("GQ82HnTvrWoe1q8AjSJ1dr5vf5GFjDUqcztb9Uyrpump")

    Args:
        contract_address (str): The contract address of the token.

    Returns:
        Dict[str, Any]: Analysis report or an error message if data is unavailable.
    """
    dex = DexClient()
    dex_data = dex.get_token_pairs("solana", contract_address)
    
    if not dex_data:
        return {"error": f"Data for {contract_address} not available on DexScreener"}

    system_prompt = QUANT_AI_PROMPT.format(historical_data=json.dumps(dex_data[0]))

    chat_messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content="Analyze the provided data and generate a report.")
    ]

    response = llm.invoke(chat_messages)
    return {"analysis": response, "dex_data":json.dumps(dex_data[0])}

@tool
def analyze_ticker(ticker: str) -> Dict[str, Any]:
    """
    Analyzes a token based on its ticker symbol using DexScreener data.

    Example:
        analyze_ticker("$BTC")  → Extracts "BTC" and searches for its data.

    Args:
        ticker (str): The token ticker symbol (e.g., "$BTC", "$SOL").

    Returns:
        Dict[str, Any]: Analysis report or an error message if data is unavailable.
    """
    extracted_ticker = re.sub(r'^\$', '', ticker)

    dex = DexClient()
    search_results = dex.search_pairs(extracted_ticker)
    
    dex_data = search_results.get("pairs", [])
    if not dex_data:
        return {"error": f"Data for {extracted_ticker} not available on DexScreener"}
    
    if dex_data[0].get("chainId") != "solana":
        return {"error": f"Data for {extracted_ticker} is not on the Solana chain"}

    system_prompt = QUANT_AI_PROMPT.format(historical_data=json.dumps(dex_data[0]))

    chat_messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content="Analyze the provided data and generate a report.")
    ]

    response = llm.invoke(chat_messages)
    return {"analysis": response, 'dex_data':json.dumps(dex_data[0])}

@tool
def analyze_market_trends(top_n_tokens: int) -> Dict[str, Any]:
    """
    Retrieves and analyzes trending tokens from Pump.fun along with DexScreener data.

    Example:
        analyze_market_trends(5) → Analyzes the top 5 trending tokens.

    Args:
        top_n_tokens (int): Number of top trending tokens to analyze.

    Returns:
        Dict[str, Any]: Market trend analysis report.
    """
    pump_fun = PumpFunClient()
    pump_fun_data = pump_fun.get_trending_tokens(top_n_tokens)
    
    if not pump_fun_data:
        return {"error": "No trending tokens found on Pump.fun"}

    final_data = []
    dex = DexClient()

    for token in pump_fun_data[1:]:  # Skip first element as per original code
        data = {
            'pumpfunData': token,
            'dexscreenerData': dex.get_token_pairs("solana", token['mint'])
        }
        final_data.append(data)

    system_prompt = QUANT_PUMP_FUN_PROMPT.format(historical_data=json.dumps(final_data))

    chat_messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content="Analyze the latest market trends based on provided data.")
    ]

    response = llm.invoke(chat_messages)
    return {"market_analysis": response, 'dex_data':json.dumps(final_data)}

@tool
def analyze_meta_market(top_n_tokens: int=10, meta: str="ai") -> Dict[str, Any]:
    """
    Retrieves and analyzes trending tokens from Pump.fun for a given meta category.

    Example:
        analyze_meta_market(5, "ai") → Analyzes the top 5 trending tokens in AI meta.

    Args:
        top_n_tokens (int): Number of top trending tokens to analyze.
        meta (str): Meta category from Pump.fun (e.g., "ai", "gaming", "meme").

    Returns:
        Dict[str, Any]: Market trend analysis report.
    """
    try:
        pump_fun = PumpFunClient()
        tokens = pump_fun.get_meta_tokens(meta, top_n_tokens)

        if not tokens:
            return {"error": f"No trending tokens found in {meta} meta on Pump.fun"}

        final_data = []
        dex = DexClient()
        
        for token in tokens:
            data = dex.get_token_pairs("solana", token['id'])
            final_data.append(data)

        system_prompt = QUANT_PUMP_FUN_PROMPT.format(historical_data=json.dumps(final_data))

        chat_messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content="Analyze the latest market trends based on provided data.")
        ]

        response = llm.invoke(chat_messages)
        return {"market_analysis": response, 'dex_data':json.dumps(final_data)}
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

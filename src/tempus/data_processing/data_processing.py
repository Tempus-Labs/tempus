from typing import Dict, Any
import json
from langchain_core.messages import AIMessage
from src.tempus.data import DexClient

def process_contract(state: Dict[str, Any]) -> Dict[str, Any]:
    """Processes the contract address."""
    tool_message = state.get("messages", [])[-1]
    content = json.loads(tool_message.content)
    dex = DexClient()
    dex_data = dex.get_token_pairs("solana", content.get('contract_address'))
    if not dex_data:
        return None
    return {"messages": [AIMessage(content=f"Dex Screener Historical Data: {dex_data}")]}

def process_ticker(state: Dict[str, Any]) -> Dict[str, Any]:
    """Processes the ticker."""
    tool_message = state.get("messages", [])[-1]
    content = json.loads(tool_message.content)
    dex = DexClient()
    dex_data = dex.search_pairs(content.get('ticker'))['pairs']
    if not dex_data:
        return None
    elif dex_data[0]["chainId"] != "solana":
        return None
    return {"messages": [AIMessage(content=f"Dex Screener Historical Data: {dex_data[0]}")]}

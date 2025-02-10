import re
from typing import Dict, Any

def extract_contract_address_and_ticker(user_input: str) -> Dict[str, Any]:
    # Define regex patterns
    contract_address_pattern = r'[a-zA-Z0-9]{40,50}'
    ticker_pattern = r'\$\b[A-Z]+\b'

    # Search for contract address and ticker
    contract_address_match = re.search(contract_address_pattern, user_input)
    ticker_match = re.search(ticker_pattern, user_input)

    # Extract values or set to None
    contract_address = contract_address_match.group(0) if contract_address_match else None
    ticker = ticker_match.group(0) if ticker_match else None

    return {
        "contract_address": contract_address,
        "ticker": ticker
    }
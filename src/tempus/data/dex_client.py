from typing import Any, List
import requests

class DexClient:
    def get_token_pairs(self, chain_id: str, token_address: str) -> List[Any]:
        url = f"https://api.dexscreener.com/token-pairs/v1/{chain_id}/{token_address}"
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()

    def search_pairs(self, pair_name: str) -> List[Any]:
        url = "https://api.dexscreener.com/latest/dex/search"
        params = {'q': pair_name}
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()

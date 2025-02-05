from dexscreener import DexscreenerClient
from typing import Any, List

class DexClient:
    def __init__(self):
        self.client = DexscreenerClient()

    def get_token_pair(self, network: str, token_address: str) -> Any:
        return self.client.get_token_pair(network, token_address)

    def get_token_pairs(self, token_address: str) -> List[Any]:
        return self.client.get_token_pairs(token_address)

    def search_pairs(self, pair_name: str) -> List[Any]:
        return self.client.search_pairs(pair_name)

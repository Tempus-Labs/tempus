from .dex_client import DexClient

__all__ = [DexClient]
# from .pump_fun_client import PumpFunClient

# class TempusDataClient:
#     def __init__(self):
#         self.dex_client = DexClient()
#         self.pump_fun_client = PumpFunClient()

#     def get_token_pair(self, network: str, token_address: str):
#         return self.dex_client.get_token_pair(network, token_address)

#     def get_token_pairs(self, token_address: str):
#         return self.dex_client.get_token_pairs(token_address)

#     def search_pairs(self, pair_name: str):
#         return self.dex_client.search_pairs(pair_name)

#     async def subscribe_new_token(self, duration: int):
#         return await self.pump_fun_client.subscribe_new_token(duration)

#     async def subscribe_account_trade(self, keys: list, duration: int):
#         return await self.pump_fun_client.subscribe_account_trade(keys, duration)

#     async def subscribe_token_trade(self, keys: list, duration: int):
#         return await self.pump_fun_client.subscribe_token_trade(keys, duration)



import asyncio
import websockets
import json
import time

class PumpFunClient:
    def __init__(self, uri: str = "wss://pumpportal.fun/api/data"):
        self.uri = uri

    async def subscribe(self, method: str, keys: list, duration: int):
        async with websockets.connect(self.uri) as websocket:
            payload = {
                "method": method,
                "keys": keys
            }
            await websocket.send(json.dumps(payload))
            end_time = time.time() + duration
            collected_data = []

            while time.time() < end_time:
                message = await websocket.recv()
                collected_data.append(json.loads(message))

            return collected_data

    async def subscribe_new_token(self, duration: int):
        return await self.subscribe("subscribeNewToken", [], duration)

    async def subscribe_account_trade(self, keys: list, duration: int):
        return await self.subscribe("subscribeAccountTrade", keys, duration)

    async def subscribe_token_trade(self, keys: list, duration: int):
        return await self.subscribe("subscribeTokenTrade", keys, duration)

# To run a specific subscription, you can use:
# data = asyncio.get_event_loop().run_until_complete(PumpFunClient().subscribe_new_token(10))
# print(data)

import asyncio
import websocket
import json
import time

class PumpFunClient:
    def __init__(self, uri: str = "wss://pumpportal.fun/api/data", max_coin: int=5):
        self.uri = uri
        self.max_coin = max_coin

    def get_pump_fun_data(self):
        uri = "wss://pumpportal.fun/api/data"
        coins = []
        
        # Establish WebSocket connection
        ws = websocket.create_connection(uri)
        
        # Subscribing to token creation events
        payload = {
            "method": "subscribeNewToken",
        }
        ws.send(json.dumps(payload))
        
        while True:
            message = ws.recv()
            data = json.loads(message)
            coins.append(data)
            
            if len(coins) == self.max_coin+1:
                print(coins)  # Print last 5 messages
                ws.close()
                return coins

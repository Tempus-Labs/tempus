"""
Client for interacting with Pump.fun data sources.
"""
import asyncio
import websocket
import json
import time
from typing import List, Dict, Optional
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

class PumpFunClient:
    """
    Client for interacting with Pump.fun data sources.
    Supports both websocket streaming for real-time data and web scraping for meta data.
    """
    
    def __init__(self, uri: str = "wss://pumpportal.fun/api/data", max_coin: int = 5):
        """
        Initialize PumpFun client.
        
        Args:
            uri (str): WebSocket URI for real-time data
            max_coin (int): Maximum number of coins to track
        """
        self.uri = uri
        self.max_coin = max_coin
        
    def get_trending_tokens(self, limit: int = 5) -> List[Dict]:
        """
        Get trending tokens via WebSocket connection.
        
        Args:
            limit (int): Number of tokens to retrieve
            
        Returns:
            List[Dict]: List of token data
        """
        coins = []
        
        # Establish WebSocket connection
        ws = websocket.create_connection(self.uri)
        
        # Subscribe to token creation events
        payload = {
            "method": "subscribeNewToken",
        }
        ws.send(json.dumps(payload))
        
        try:
            while True:
                message = ws.recv()
                data = json.loads(message)
                coins.append(data)
                
                if len(coins) == limit + 1:  # +1 for initial connection message
                    return coins
        finally:
            ws.close()
            
    def get_meta_tokens(self, meta: str, limit: int = 10) -> Optional[List[Dict]]:
        """
        Get tokens for a specific meta category via web scraping.
        
        Args:
            meta (str): Meta category (e.g., "ai", "gaming", "meme")
            limit (int): Maximum number of tokens to retrieve
            
        Returns:
            Optional[List[Dict]]: List of token data or None if scraping fails
        """
        try:
            # Configure headless Chrome
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            
            # Load the webpage
            url = f"https://pump.fun/board?meta={meta}&show_animations=false"
            driver.get(url)
            
            # Wait for JavaScript to render
            time.sleep(5)
            
            # Parse HTML
            soup = BeautifulSoup(driver.page_source, "html.parser")
            div_elements = soup.find_all("div", id=True)
            
            # Extract token data
            tokens = []
            for div in div_elements[:limit]:
                token_id = div.get('id')
                if token_id:
                    tokens.append({
                        'id': token_id,
                        'meta': meta
                    })
                    
            return tokens
            
        except Exception as e:
            print(f"Error scraping meta tokens: {str(e)}")
            return None
            
        finally:
            if 'driver' in locals():
                driver.quit()

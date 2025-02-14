import json
import unittest
from src.tempus.utils import extract_contract_address_and_ticker
from src.tempus.data_processing.data_processing import process_contract, process_ticker
from src.tempus.agents.quant_agent import quant_agent
from langchain_core.messages import AIMessage

class TestTempusFunctions(unittest.TestCase):

    def test_extract_contract_address_and_ticker(self):
        user_message = "Check out this contract: 0x1234567890abcdef1234567890abcdef12345678 and the ticker $BTC."
        result = extract_contract_address_and_ticker(user_message)
        self.assertEqual(result['contract_address'], '0x1234567890abcdef1234567890abcdef12345678')
        self.assertEqual(result['ticker'], 'BTC')

    def test_process_contract(self):
        state = {
            "messages": [AIMessage(content=json.dumps({"contract_address": "0x1234567890abcdef1234567890abcdef12345678"}))]
        }
        result = process_contract(state)
        self.assertIsNotNone(result)
        self.assertIn("messages", result)

    def test_process_ticker(self):
        state = {
            "messages": [AIMessage(content=json.dumps({"ticker": "BTC"}))]
        }
        result = process_ticker(state)
        self.assertIsNotNone(result)
        self.assertIn("messages", result)

    def test_quant_agent(self):
        state = {
            "messages": [AIMessage(content='{"historical_data": "Sample data"}')]
        }
        result = quant_agent(state)
        self.assertIsNotNone(result)
        self.assertIn("messages", result)

if __name__ == '__main__':
    unittest.main()

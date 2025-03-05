<html>
    <h1 align="center">
        Tempus Labs
    </h1>
    <h3 align="center">
        Your Gateway to Smarter Solana Market Intelligence
    </h3>

<div align="center">

[![Static Badge](https://img.shields.io/badge/tempus-documentation-red?style=flat)](https://tempuslabs.gitbook.io/tempus)
</div>

</html>

Tempus is a Quant AI Agent Framework designed for the Solana ecosystem, providing users with the tools to build, deploy, and customize AI-driven quantitative analysis models. By leveraging modular architecture and AI-powered analytics, Tempus enhances decision-making in crypto markets, offering deep insights into:
- Token performance
- Portfolio management
- Market trends

---

## Overview

<div align="center">
  <img src="./img/tempus-workflow.png" alt="Tempus Workflow" width="100%" />
</div>

## Features

| **Feature**                              | **Description**                                                                                                                                                             |
| ---------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Quant AI Agent Framework**             | Tempus enables users to create and deploy their own **QUANT AI Agents**, allowing for automated quantitative modeling, strategy backtesting, and real-time market insights. |
| **Modular & Extensible Design**          | A **plug-and-play architecture** allows users to integrate **custom modules** and adapt Tempus to specific **analytical and trading strategies**.                           |
| **AI-Powered Market Insights**           | Advanced **reasoning models** analyze **token metrics**, **liquidity trends**, and **trading volumes** to help users identify market opportunities.                         |
| **Portfolio Analysis via Solana Wallet** | Tempus connects with **Solana wallets**, enabling **automated tracking of holdings**, **transaction histories**, and **risk assessments**.                                  |
| **Python-Based Flexibility**             | Built on **Python**, Tempus provides an **accessible development environment** for **implementing and refining quantitative strategies**.                                   |
| **Real-Time On-Chain Data Analysis**     | Tempus **seamlessly retrieves and processes** Solana blockchain data, including **token listings**, **price action**, and **transaction flows**.                            |
| **Secure & Transparent**                 | Tempus ensures **data integrity**, **security compliance with blockchain best practices**, and an **open and adaptable framework**.                                         |

## Quick Start Guide

### Prerequisites

- [Python 3.10+](https://www.python.org/)
- LLM API Key(OpenAI, Deepseek)
- [Chromedriver](https://developer.chrome.com/docs/chromedriver/downloads)

---

### Installation

1. **Install Tempus**:

   ```python
   pip install tempus-labs==1.0.0
   ```

2. **Create the Environment File**:
   Set up a `.env` file to store your API key securely:
   ```bash
   OPENAI_API_KEY=your_api_key # Fill if you are using OpenAI
   DEEPSEEK_API_KEY=your_api_key # Fill if you are using Deepseek
   ```

3. **Basic usage**:

   ```python
   from tempus.agents import QuantAIAgent

    # Initialize with default settings (OpenAI)
    agent = QuantAIAgent()
    
    # Basic analysis
    response = agent.chat("Analyze BTC market trends")
    print(response)
    
    # Streaming responses
    for chunk in agent.chat_stream("What's happening with ETH?"):
    chunk.pretty_print()
   ```
---

## Congratulations!

You're now ready to explore the power of Tempus Labs for AI-driven quantitative insights on the Solana ecosystem!

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Support

For questions or issues, visit our [GitHub repository](https://github.com/Tempus-Labs/tempus) or open an issue.

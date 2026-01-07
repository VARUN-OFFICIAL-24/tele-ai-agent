
### AI-Powered Telegram Assistant with Tool Integration

**tele-ai-agent** is an LLM-powered Telegram assistant designed to support **stateful conversations** and **real-time tool integration** such as weather and stock data.  
It demonstrates how large language models can be combined with external APIs to build a practical, user-facing conversational AI system.

---

## 🎯 Project Overview

Modern chatbots become significantly more useful when they can:
- Maintain conversation context
- Reason over user queries
- Interact with external tools and APIs

This project implements a Telegram-based AI assistant that does exactly that, serving as a practical example of **applied LLM systems** rather than a simple chatbot demo.

---

## ✨ Key Features

- LLM-powered conversational responses
- Stateful conversations with per-user context
- Tool integration for real-time data:
  - Weather information
  - Stock price lookup
- Asynchronous Telegram bot architecture
- Clean separation between conversation logic and tool execution

---

## 🧠 System Design (High-Level)

1. User sends a message via Telegram  
2. Message context is retrieved or initialized  
3. The LLM processes the query with conversation history  
4. If required, external tools (weather, stocks, APIs) are invoked  
5. The final response is generated and sent back to the user  

This design allows the assistant to behave like a **tool-using AI agent**, not just a text responder.

---

## 🧩 Technology Stack

- Python
- Telegram Bot API
- Large Language Models (via local or API-based inference)
- External APIs (Weather, Stocks)
- Async programming (for responsiveness)

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-username/tele-ai-agent.git
cd tele-ai-agent
```

### 2. Install dependencies
```bash
pip install -r requirements.txt

```


### 3. Environment configuration
Create a `.env` file (do not upload this to GitHub):

```bash
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
WEATHER_API_KEY=your_weather_api_key
STOCK_API_KEY=your_stock_api_key
LLM_API_KEY=your_llm_api_key

```
---

### 🚀 Running the Bot
```bash
python main.py

```
Once running:
- Open Telegram
- Start a chat with your bot
- Interact using natural language queries such as:
    - Weather in a city
    - Stock price checks
    - General conversational questions
 ---

 ## 📌 Example Use Cases

- AI-powered personal Telegram assistant
- Tool-augmented conversational agents
- Demonstration of LLM + API integration
- Learning reference for applied AI systems

---

## ⚠️ Limitations

- Designed for educational and experimental use
- Not optimized for large-scale production deployment
- Accuracy depends on external APIs and model quality

---

## 🔮 Future Improvements

- More tools (news, calendars, reminders)
- Improved memory management
- User-level personalization
- Deployment with containerization
- Rate-limiting and monitoring

---




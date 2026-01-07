import os
import logging
from typing import Dict

from dotenv import load_dotenv
import requests

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)

from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage

# ---------------------------------------------------------------------
# Environment & Logging
# ---------------------------------------------------------------------

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# ---------------------------------------------------------------------
# LLM Setup
# ---------------------------------------------------------------------

llm = ChatOllama(model="llama3.2", temperature=0.4)

SYSTEM_PROMPT = (
    "You are an intelligent Telegram assistant. "
    "You can hold conversations, answer questions, "
    "and use tools like weather and stock lookup when relevant. "
    "Be concise and helpful."
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        ("human", "{input}"),
    ]
)

# ---------------------------------------------------------------------
# In-Memory Conversation Store (Per User)
# ---------------------------------------------------------------------

conversation_memory: Dict[int, list] = {}

MAX_HISTORY = 6  # keep memory bounded

# ---------------------------------------------------------------------
# Tool Functions
# ---------------------------------------------------------------------

def get_weather(city: str) -> str:
    """Fetch current weather for a city."""
    if not WEATHER_API_KEY:
        return "Weather API key not configured."

    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={WEATHER_API_KEY}&units=metric"
    )

    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        data = res.json()

        desc = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]

        return (
            f"Weather in {city}:\n"
            f"- Condition: {desc}\n"
            f"- Temperature: {temp}°C\n"
            f"- Humidity: {humidity}%"
        )

    except Exception:
        return "Unable to fetch weather data right now."

def get_stock_price(symbol: str) -> str:
    """Mock stock lookup (replace with real API if needed)."""
    return f"Stock lookup for '{symbol.upper()}' is not configured yet."

# ---------------------------------------------------------------------
# Command Handlers
# ---------------------------------------------------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    conversation_memory[user_id] = []

    await update.message.reply_text(
        "Hi! I’m your AI assistant 🤖\n"
        "You can chat with me or ask things like:\n"
        "- Weather in London\n"
        "- Stock price of AAPL"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Available commands:\n"
        "/start – Reset conversation\n"
        "/help – Show help\n\n"
        "You can also ask natural language questions."
    )

# ---------------------------------------------------------------------
# Message Handler
# ---------------------------------------------------------------------

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_input = update.message.text.strip()

    if user_id not in conversation_memory:
        conversation_memory[user_id] = []

    # Simple tool routing
    lowered = user_input.lower()

    if lowered.startswith("weather in"):
        city = user_input.replace("weather in", "").strip()
        reply = get_weather(city)
        await update.message.reply_text(reply)
        return

    if lowered.startswith("stock"):
        symbol = user_input.split()[-1]
        reply = get_stock_price(symbol)
        await update.message.reply_text(reply)
        return

    # LLM response
    history = conversation_memory[user_id][-MAX_HISTORY:]

    messages = []
    for msg in history:
        messages.append(msg)

    chain = prompt | llm

    response = chain.invoke({"input": user_input}).content

    # Update memory
    conversation_memory[user_id].append(HumanMessage(content=user_input))
    conversation_memory[user_id].append(AIMessage(content=response))

    conversation_memory[user_id] = conversation_memory[user_id][-MAX_HISTORY:]

    await update.message.reply_text(response)

# ---------------------------------------------------------------------
# Main Application
# ---------------------------------------------------------------------

def main():
    if not TELEGRAM_BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not set")

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logging.info("tele-ai-agent is running...")
    app.run_polling()

if __name__ == "__main__":
    main()

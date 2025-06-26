import asyncio
import json
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from collections import defaultdict

TOKEN = os.getenv("TOKEN")  # Безопасно берём токен из переменной окружения

DATA_FILE = "trash.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return defaultdict(int, json.load(f))
    return defaultdict(int)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

trash_counts = load_data()

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Привет! Пиши /trash, когда вынес мусор. /stats покажет счёт.")

@dp.message(Command("trash"))
async def handle_trash(message: Message):
    user = message.from_user.first_name
    trash_counts[user] += 1
    save_data(trash_counts)
    await message.answer(f"{user}, ты вынес мусор {trash_counts[user]} раз(а)!")

@dp.message(Command("stats"))
async def stats(message: Message):
    if not trash_counts:
        await message.answer("Ещё никто не выносил мусор.")
        return
    stats_text = "📊 Статистика выноса мусора:\n"
    for user, count in sorted(trash_counts.items(), key=lambda x: -x[1]):
        stats_text += f"• {user}: {count}\n"
    await message.answer(stats_text)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

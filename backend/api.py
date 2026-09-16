import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from starlette.staticfiles import StaticFiles
from backend.schemas import ActionsSchema
from aiogram import Bot
from dotenv import load_dotenv


load_dotenv()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_headers=['*'],
    allow_credentials=True,
    allow_methods=['*'],
)
bot = Bot(os.getenv('BOT_TOKEN'))

BASE_DIR = Path(__file__).resolve().parent
app.mount('/static', StaticFiles(directory=BASE_DIR / 'static'), name='static')

counters = {
    "coffee": 0,
    "hug": 0,
    "praise": 0,
    "sweet": 0,
    "music": 0,
    "miss": 0,
    "custom": 0
}
mood_emojis = {1: "😭", 2: "🌧️", 3: "😐", 4: "😊", 5: "🥰"}

@app.get('/')
async def main():
    file_path = BASE_DIR / "static" / "index.html"
    return FileResponse(path=file_path)

@app.post('/api/v1/actions/')
async def main_actions(body_text: ActionsSchema):
    action_type = body_text.action_type
    if action_type in counters:
        counters[action_type] += 1

    action_descriptions = {
        "sweet": "🍫 Запросила вкусняшку!",
        "hug": "🤗 Запросила срочные обнимашки!",
        "miss": "🥺 Нажала «Я скучаю» — срочный вызов!",
        "call": "📱 Просит позвонить!",
        "work": "💻 Напомнила, что пора отдохнуть от работы!",
        "movie": "🍿 Предлагает выбрать фильм на вечер!",
        "love_answer": "💘 Ответила «Конечно!» на главный вопрос!",
        "mega_explosion": "🚨 АПОКАЛИПСИС! Нажала кнопку «Нет»!",
        "custom": f"💬 Кастомное сообщение: **{body_text.message}**",
        "mood_update": "✨ Обновила настроение!"
    }

    time = body_text.timestamp
    time = time.replace('T', ' ')[:19:]

    current_emoji = mood_emojis[body_text.mood]
    if body_text.action_type == 'mood_update':
        desc = f'Обновила настроение: {current_emoji}'
    else:
        desc = f'Действие: {action_descriptions.get(action_type)}'

    tg_text = (
        f"💖 **Новый сигнал с дэшборда!**\n\n"
        f"• **Действие:** {desc}\n"
        f"• **Время:** {time}\n"
        f"• **Счетчик:** {counters.get(action_type, 'N/A')}"
    )
    try:
        await bot.send_message(
            chat_id=os.getenv('ADMIN_ID'),
            text=tg_text,
            parse_mode='Markdown',
        )
    except Exception as e:
        raise e

    return {'status': 'success', 'updated_counters': counters}

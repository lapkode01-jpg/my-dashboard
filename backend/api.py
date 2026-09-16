import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from schemas import ActionsSchema
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


counters = {
    "coffee": 0,
    "hug": 0,
    "praise": 0,
    "sweet": 0,
    "music": 0,
    "miss": 0,
    "custom": 0
}


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
        "custom": f"💬 Кастомное сообщение: **{body_text.message}**"
    }

    desc = action_descriptions.get(action_type)
    time = body_text.timestamp
    time = time.replace('T', ' ')[:19:]

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

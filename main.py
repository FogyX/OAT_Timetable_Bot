from telebot.async_telebot import AsyncTeleBot
from telebot.util import quick_markup
from telebot.types import Message, CallbackQuery
import asyncio
from config import *
from query_handler import get_timetable

bot = AsyncTeleBot(TOKEN)

menu_markup = quick_markup({
    "На сегодня": {"callback_data": "today"},
    "На завтра": {"callback_data": "tomorrow"}
}, row_width=1)

return_markup = quick_markup({
    "Назад": {"callback_data": "return"}
}, row_width=1)


@bot.message_handler(commands=["start"])
async def start(message: Message):
    await bot.send_message(message.chat.id, "Здравствуй! На когда ты хочешь узнать расписание?",
                           reply_markup=menu_markup)


async def return_to_menu(message: Message):
    await bot.edit_message_text("На какой день ты хочешь узнать расписание?", chat_id=message.chat.id,
                                message_id=message.id, reply_markup=menu_markup)


async def set_loading_message(message: Message):
    await bot.edit_message_text("Загрузка...", chat_id=message.chat.id, message_id=message.id)


@bot.callback_query_handler(func=lambda query: True)
async def handle_callback(query: CallbackQuery):
    await set_loading_message(query.message)
    if query.data == "today":
        date = datetime.datetime.today()
        timetable = await get_timetable(date)
        await bot.edit_message_text(f"Расписание на сегодня:\n\n{timetable}", query.message.chat.id, query.message.id,
                                    reply_markup=return_markup, parse_mode="HTML")
    elif query.data == "tomorrow":
        date = datetime.datetime.today() + datetime.timedelta(days=1)
        timetable = await get_timetable(date)
        await bot.edit_message_text(f"Расписание на завтра:\n\n{timetable}", query.message.chat.id, query.message.id,
                                    reply_markup=return_markup, parse_mode="HTML")
    elif query.data == "return":
        await return_to_menu(query.message)


asyncio.run(bot.polling())

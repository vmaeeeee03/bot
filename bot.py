import json
from aiogram import Bot, Dispatcher, types
import logging
import asyncio  # Модуль для работы с асинхронным кодом
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command


API_TOKEN = ""

logging.basicConfig(level=logging.INFO)
# Создаем объект диспетчера, который управляет входящими сообщениями и командами
dp = Dispatcher()

kb = [
    [
        KeyboardButton(text="О компании"), # Кнопка для запроса информации о боте
        KeyboardButton(text="Связаться с оператором")  # Кнопка для получения справки
    ]
]

# Создаём объект клавиатуры с кнопками
keyboard = ReplyKeyboardMarkup(
    keyboard=kb, # Передаём список кнопок
    resize_keyboard=True, # Уменьшаем клавиатуру под размер экрана
    input_field_placeholder="Выберите действие" # Текст-подсказка в поле ввода
    )

ans = {
    "цены": "цены, стоимость",
    "часы работы": "часы работает, время работы, доступность",
    "доставка": "доставка, сроки доставки, стоимость доставки",
    "возврат": "возврата, обмен, возврат товара, гарантия",
    "контакты": "связаться, телефон, email",
    "адрес" : "находитесь, адрес",
    "заказ" : "отследить, отслеживание",
    "оплата" : "оплаты, оплатить"
}

@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("С чем вам помочь?", reply_markup=keyboard)

@dp.message(lambda message: message.text == "О компании")
async def about_bot(message: types.Message):
    await message.answer("Наша компания занимается доставкой товаров по всей стране.")

# Обрабатываем нажатие кнопки "Помощь"
@dp.message(lambda message: message.text == "Связаться с оператором")
async def about_bot(message: types.Message):
    await message.answer("Перевожу на оператора...")

# Декоратор @dp.message() указывает, что функция будет обрабатывать входящие сообщения
@dp.message()
async def answer_faq(message: types.Message):
    with open('faq.json', encoding='utf-8') as f:
        data = json.load(f)
    text = message.text.lower()

    response = "NO"
    for category, keywords in ans.items():
        if any(keyword in text for keyword in keywords.split(", ")):
            for faq_item in data['faq']:
                if category in faq_item["category"].lower():
                    response = faq_item["answer"]
                    break
            break

    await message.answer(response)

async def main():
    bot = Bot(token=API_TOKEN)
    await dp.start_polling(bot)

# Проверяем, запущен ли скрипт напрямую (не импортирован в другой файл)
if __name__ == "__main__":
    asyncio.run(main())


from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def rating_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⭐️⭐️⭐️⭐️⭐️ Отлично"),
             KeyboardButton(text="⭐️⭐️⭐️⭐️ Хорошо")],
            [KeyboardButton(text="⭐️⭐️⭐️ Средне"),
             KeyboardButton(text="⭐️⭐️ Плохо")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Выберите оценку"
    )

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from ..keyboards.reply import rating_kb
from ..db.models import save_feedback, create_promo
from ..db.promo import gen_code
from ..texts.ru import ASK_RATING, ASK_COMMENT, THANKS_POSITIVE, THANKS_NEUTRAL, THANKS_NEGATIVE
from ..settings import MANAGERS_CHAT_ID
from ..services.notifier import notify_manager
from datetime import datetime, timedelta

router = Router()

class FB(StatesGroup):
    waiting_rating = State()
    waiting_comment = State()

@router.message(F.text.in_({"/start","/feedback"}))
async def start_feedback(message: Message, state: FSMContext):
    await message.answer(ASK_RATING, reply_markup=rating_kb())
    await state.set_state(FB.waiting_rating)

@router.message(FB.waiting_rating)
async def got_rating(message: Message, state: FSMContext):
    mapping = {
        "⭐️⭐️⭐️⭐️⭐️ Отлично": 5,
        "⭐️⭐️⭐️⭐️ Хорошо": 4,
        "⭐️⭐️⭐️ Средне": 3,
        "⭐️⭐️ Плохо": 2
    }
    rating = mapping.get(message.text)
    if not rating:
        return await message.answer("Выберите один из вариантов на клавиатуре 🙏")
    await state.update_data(rating=rating)
    await message.answer(ASK_COMMENT)
    await state.set_state(FB.waiting_comment)

@router.message(FB.waiting_comment)
async def got_comment(message: Message, state: FSMContext, bot):
    data = await state.get_data()
    rating = data["rating"]
    comment = None if message.text.lower() in {"нет","no","ne","yo'q","yok"} else message.text

    save_feedback(message.from_user.id, message.from_user.username, rating, comment)

    if rating >= 4:
        code = gen_code()
        create_promo(code, message.from_user.id, discount=10)
        expires = (datetime.utcnow() + timedelta(days=30)).strftime("%d.%m.%Y")
        await message.answer(THANKS_POSITIVE.format(code=code, expires=expires))
    elif rating == 3:
        await message.answer(THANKS_NEUTRAL)
    else:
        await message.answer(THANKS_NEGATIVE)
        txt = ("⚠️ Негативный отзыв\n"
               f"Оценка: {rating}\n"
               f"От: @{message.from_user.username or message.from_user.id}\n"
               f"Текст: {comment or '-'}")
        await notify_manager(bot, MANAGERS_CHAT_ID, txt)
    await state.clear()

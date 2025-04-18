from aiogram import Router, html, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy import insert

from bot.button.button import promo_button, link_video_button
from bot.db.models import session, User, Promo
from bot.pro.state import PromoState

start_router = Router()


@start_router.message(CommandStart())
async def start_bot(message: Message, state: FSMContext):
    try:
        user = session.query(User.id).filter(User.user_id == message.from_user.id).first()

        if user is None:
            new_user = insert(User).values(
                user_id=message.from_user.id,
                full_name=message.from_user.full_name,
                last_name=message.from_user.last_name,
                username=message.from_user.username,
            )
            session.execute(new_user)
            session.commit()

        await message.answer(html.bold(f"<i>{message.from_user.full_name}</i>"), reply_markup=promo_button())

        await state.set_state(PromoState.start)
    except Exception as e:
        await message.answer('Error')


@start_router.message(PromoState.start)
async def start_promo(message: Message, state: FSMContext):
    try:
        promo = session.query(Promo).filter(Promo.title == message.text).first()
        if promo:
            text = (
                f"<b>        {promo.title}        </b>\n"  # "Yandex" so'zi italikda
                f"<b>💸  Promokod:</b> <code>{promo.code}</code>\n\n"  # Promo kodini monospace formatda ko'rsatish
                f"<i>📜 {promo.dictionary}</i>"  # Promo ta'rifini italikda ko'rsatish
            )
            await message.answer(html.bold(text), reply_markup=link_video_button(promo.title))
            await state.update_data({'title': message.text})
        else:
            await message.answer("Bunday promo mavjud emas.")
    except Exception as e:
        await message.answer('Error')


@start_router.callback_query(F.data == 'video')
async def start_promo(callback: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        if data['title']:
            promo = session.query(Promo).filter(Promo.title == data['title']).first()
            if promo:
                await callback.message.answer_video(promo.video)
            else:
                await callback.message.answer('Error')
            await state.set_state(PromoState.start)
    except Exception as e:
        await callback.message.answer('Error')

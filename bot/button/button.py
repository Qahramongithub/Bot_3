from aiogram.types import InlineKeyboardButton, KeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from sqlalchemy import select

from bot.db.models import session, Promo


def promo_button():
    rkb = ReplyKeyboardBuilder()
    result = session.execute(select(Promo.title))
    promos = [row[0] for row in result.all()]
    if promos:
        rkb.add(*[KeyboardButton(text=title) for title in promos])

    rkb.add(*[
        KeyboardButton(text="Instagram 🔊",
                       web_app=WebAppInfo(url='https://www.instagram.com/pramokod_uz?igsh=MXJscmd0bTVkMzkwOA=='))
    ])
    rkb.adjust(2, repeat=True)
    return rkb.as_markup(resize_keyboard=True)


def link_video_button(title):
    rkb = InlineKeyboardBuilder()

    link_result = session.execute(select(Promo.link).where(Promo.title == title)).scalars().all()
    video_result = session.execute(select(Promo.video).where(Promo.title == title)).scalars().all()

    for url in link_result:
        if url:
            rkb.add(InlineKeyboardButton(text='🚀 Link', url=url))

    for video_url in video_result:
        if video_url:
            rkb.add(InlineKeyboardButton(text='📽 Video', callback_data='video'))

    rkb.adjust(1)
    return rkb.as_markup()

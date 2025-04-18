from bot.pro.cod import start_router
from aiogram import Dispatcher

dp = Dispatcher()
dp.include_routers(
    start_router,
)

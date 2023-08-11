from multiprocessing.pool import ThreadPool
from functools import lru_cache
from aiogram import Bot, Dispatcher, types

API_TOKEN = '6638915745:AAGq0uADziYm6PB8IgsIk9_DjlIBsqHb4ik'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@lru_cache(maxsize=None)
def partial_factorial(start, end):
    result = 1
    for i in range(start, end + 1):
        result *= i
    return result


def factorial(n):
    if n == 0 or n == 1:
        return 1
    mid = n // 2
    first_half = 0
    second_half = 0

    pool = ThreadPool(processes=2)

    first_half = pool.apply_async(partial_factorial, args=(1, mid))
    second_half = pool.apply_async(partial_factorial, args=(mid + 1, n))

    return first_half.get() * second_half.get()


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Send a number and I'll compute its factorial!")

@dp.message_handler()
async def handle_message(message: types.Message):
    try:
        num = int(message.text)
        if abs(num) > 1000:
            result = factorial(abs(num))
            await message.answer(str(result)[:5])
        else:
            await message.answer(str(factorial(num)))
    except ValueError:
        await message.answer("Please enter a valid number!")

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)

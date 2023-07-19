from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.web_app_info import WebAppInfo


bot = Bot('6311110068:AAExrIkczMZsS9qdMbuchSlyx3GnrPkgGz0')

dp = Dispatcher(bot)



@dp.message_handler(commands = ['start'])
async def start(message : types.Message):
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton('Открыть игру', web_app=WebAppInfo(url = 'https://edpiat.github.io/')))
    await message.answer('Привет, играй тут', reply_markup= markup)



executor.start_polling(dp)
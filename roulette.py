from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.web_app_info import WebAppInfo
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import sqlite3
import string
import secrets
import datetime


bot = Bot('6311110068:AAExrIkczMZsS9qdMbuchSlyx3GnrPkgGz0')

dp = Dispatcher(bot)




@dp.message_handler(commands = ['admin'])
async def admin_panel_initiate(message : types.Message):
    conn = sqlite3.connect('SilaevRoulette.sql')

    #object that lets us perform commands with database
    cur = conn.cursor()

    #creating a table with fields if not created yet
    cur.execute('CREATE TABLE IF NOT EXISTS users (id integer primary key, tokenname varchar(50), tokendate smalldatetime , tgusername varchar(50), rolldate smalldatetime, win varchar(50), spin_amount int default (1))')

    #we need to commit the table to a database
    conn.commit()

    #closing the connection with table and database
    cur.close()
    conn.close()
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Сгенерировать токен', callback_data='generate'))
    markup.add(types.InlineKeyboardButton('Посмотреть список созданных токенов', callback_data='alltokens'))
    markup.add(types.InlineKeyboardButton('Отозвать токен', callback_data='revoketoken'))
    await message.answer('выбери что хочешь сделать', reply_markup= markup)
    dp.register_callback_query_handler(admin_callback)






@dp.callback_query_handler(lambda callback: callback.data)
async def admin_callback(call: types.CallbackQuery):


    if call.data == "generate" or call.data == "one_more_token":
        alphabet = string.ascii_letters + string.digits
        password = ''.join(secrets.choice(alphabet) for i in range(12))
        token = str(password)

        current_time = datetime.datetime.now()




        conn = sqlite3.connect('SilaevRoulette.sql')
        #object that lets us perform commands with database
        cur = conn.cursor()

        #creating a table with fields if not created yet
        cur.execute(f"INSERT INTO users (tokenname, tokendate) VALUES ('{token}', '{current_time}')")

        #we need to commit the table to a database
        conn.commit()

        #closing the connection with table and database
        cur.close()
        conn.close()




        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text="Выйти", callback_data="exit"))
        markup.add(types.InlineKeyboardButton(text="Сгенерировать еще один токен", callback_data="one_more_token"))
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = f'{token}', reply_markup=markup)





    elif call.data == "alltokens":

        conn = sqlite3.connect('SilaevRoulette.sql')
        #object that lets us perform commands with database
        cur = conn.cursor()

        #creating a table with fields if not created yet
        users = cur.execute('SELECT * FROM users')
        info = ''
        for record in users:
            info += f'ID: {record[0]}, Token :{record[1]},Дата создания :{record[2]}, Какой Юзер использовал :{record[3]}, Когда юзер использовал :{record[4]}, Выигрышь :{record[5]},\n\n '
        #we need this func to retrieve all data from a table
        cur.fetchall()

        #closing the connection with table and database
        cur.close()
        conn.close()



        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text="Выйти", callback_data="exit"))
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = f'{info}', reply_markup=markup)






    elif call.data == "exit":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Сгенерировать токен', callback_data='generate'))
        markup.add(types.InlineKeyboardButton('Посмотреть список созданных токенов', callback_data='alltokens'))
        markup.add(types.InlineKeyboardButton('Отозвать токен', callback_data='revoketoken'))
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = "выбери что хочешь сделать", reply_markup=markup)


@dp.message_handler(commands = ['start'])
async def start(message : types.Message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Открыть игру', web_app=WebAppInfo(url = 'https://edpiat.github.io/')))
    await message.answer('Привет, играй тут', reply_markup= markup)



executor.start_polling(dp)
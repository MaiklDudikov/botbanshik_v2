import logging
from aiogram import Bot, Dispatcher, executor, types
from banshiki import SQbanshik
import random

API_TOKEN = '5119965890:AAGlVxqvhTB9gNCxU8YMixjlSUqByrzI0zc'
# log level
logging.basicConfig(level=logging.INFO)
# bot init
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

db = SQbanshik('database.db')


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer(f"Привет 😉 {message.from_user.full_name} !\nТвой ID : "
                         f"{message.from_user.id}")

    if not db.banshik_exists(message.from_user.id):
        db.add_human(message.from_user.id, message.from_user.full_name)
        await message.answer("Вы добавлены в базу данных !")
    else:
        await message.answer("Такой пользователь уже существует !")

    await message.answer("Помощь /help")


@dp.message_handler(commands=['info'])
async def info(message: types.Message):
    await message.answer(
        "/баня\nТы идешь сегодня в баню ?\n\n"
        "/how_much_today\nСколько сдал сегодня в кубышку ?\n\n"
        "/total_go_people\nКто идет сегодня в баню ?\n\n"
        "/total_many_people\nКто, сколько сдал сегодня в кубышку ?\n\n"
        "/update_all\nОбновить у всех, после похода в баню, ИЛЬЯ ОБЯЗАТЕЛЬНО !\n\n"
        "/кубышка\nСколько всего в кубышке ?\n\n"
    )


@dp.message_handler(commands=['help'])
async def help_me(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item1 = types.KeyboardButton('/баня 🍻')
    item2 = types.KeyboardButton('/total_go_people 🏃')
    item3 = types.KeyboardButton('/how_much_today ❓')
    item4 = types.KeyboardButton('/total_many_people')
    item5 = types.KeyboardButton('/info ℹ')
    item6 = types.KeyboardButton('/кубышка 💵')
    item7 = types.KeyboardButton('/help 🆘')
    item8 = types.KeyboardButton('/веники 🥬')
    item9 = types.KeyboardButton('/рандом 🎲 от 0 до 15 🍺 пивная лотерея ')
    markup.add(item1, item2, item3, item4, item5, item6, item7, item8, item9)
    await message.answer("Выбери одну из функций", reply_markup=markup)


@dp.message_handler(commands=['рандом'])
async def randomize(message: types.Message):
    await bot.send_message(message.chat.id, "Выиграл номер : {0}".format(random.randint(0, 15)))


@dp.message_handler(commands=['баня'])
async def go_bath_house(message: types.Message):
    await message.answer("Пойдёшь сегодня в баню ? /yes   /no")


@dp.message_handler(commands=['yes'])
async def yes_bath(message: types.Message):
    await message.answer("Записал 😉")
    db.update_bath('да', message.from_user.id)


@dp.message_handler(commands=['no'])
async def no_bath(message: types.Message):
    await message.answer("Записал 😉")
    db.update_bath('нет', message.from_user.id)


@dp.message_handler(commands=['update_all_bath_house'])
async def update_all_bath_house(message: types.Message):
    await message.answer("Обновил !")
    db.update_everyone_bath_house('?')


@dp.message_handler(commands=['how_much_today'])
async def how_much_today(message: types.Message):
    await message.answer("Сколько сдал сегодня в кубышку ?\n /0   /50   /100   /150")


@dp.message_handler(commands=['0'])
async def zero(message: types.Message):
    await message.answer("Записал 😉")
    db.update_amount(0, message.from_user.id)
    db.add_kubyshka(0)


@dp.message_handler(commands=['50'])
async def fifty(message: types.Message):
    await message.answer("Записал 😉")
    db.update_amount(50, message.from_user.id)
    db.add_kubyshka(50)


@dp.message_handler(commands=['100'])
async def hundred(message: types.Message):
    await message.answer("Записал 😉")
    db.update_amount(100, message.from_user.id)
    db.add_kubyshka(100)


@dp.message_handler(commands=['150'])
async def one_hundred_fifty(message: types.Message):
    await message.answer("Записал 😉")
    db.update_amount(150, message.from_user.id)
    db.add_kubyshka(150)


@dp.message_handler(commands=['веники'])
async def brooms(message: types.Message):
    await message.answer("Сколько взяли на веники ?\n /_100   /_150   /_300")


@dp.message_handler(commands=['_100'])
async def minus_hundred(message: types.Message):
    await message.answer("Записал 😉")
    db.delete_kubyshka(100)


@dp.message_handler(commands=['_150'])
async def minus_one_hundred_fifty(message: types.Message):
    await message.answer("Записал 😉")
    db.delete_kubyshka(150)


@dp.message_handler(commands=['_300'])
async def minus_three_hundred(message: types.Message):
    await message.answer("Записал 😉")
    db.delete_kubyshka(300)


@dp.message_handler(commands=['update_all_amount'])
async def update_all_amount(message: types.Message):
    await message.answer("Обновил !")
    db.update_everyone_amount(0)


@dp.message_handler(commands=['total_go_people'])
async def total_go_people(message: types.Message):
    await message.answer(f"Вот кто идет сегодня в баню :\n\n {db.get_bath()}")


@dp.message_handler(commands=['total_many_people'])
async def total_many_people(message: types.Message):
    await message.answer(f"Сегодня сдали :\n\n {db.get_amount()}")


@dp.message_handler(commands=['кубышка'])
async def total_kubyshka(message: types.Message):
    await message.answer(f"Всего в кубышке :\n {db.get_kubyshka()} монеток")


# run long-polling # False, если важные данные
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

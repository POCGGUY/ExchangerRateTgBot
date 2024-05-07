from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(keyboard = [[KeyboardButton(text='Задать границы курса')],
                                       [KeyboardButton(text='Вкл./Выкл. сообщения от бота')]], resize_keyboard = 'true')
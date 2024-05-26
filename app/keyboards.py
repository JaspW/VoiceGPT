from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Chat')]
], 
                           resize_keyboard=True,
                           input_field_placeholder='Выберите пункт меню')
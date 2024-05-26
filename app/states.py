from aiogram.fsm.state import State, StatesGroup


class Chat(StatesGroup):
    text = State()
    process = State()
    
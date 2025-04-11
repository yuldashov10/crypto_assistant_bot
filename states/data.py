from aiogram.fsm.state import State, StatesGroup


class ClearData(StatesGroup):
    confirm = State()

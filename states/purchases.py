from aiogram.fsm.state import State, StatesGroup


class AddPurchase(StatesGroup):
    asset = State()
    price = State()
    amount = State()
    confirm = State()


class DeletePurchase(StatesGroup):
    select_asset = State()
    select_purchase = State()
    confirm = State()

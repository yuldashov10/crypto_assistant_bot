import csv
import os

from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    FSInputFile,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from core import messages
from core.utils import create_paginated_keyboard
from data.manager import DataManager
from data.storage import SUPPORTED_CRYPTOS
from states.data import ClearData
from states.purchases import AddPurchase, DeletePurchase

router = Router()


def setup_handlers(data_manager: DataManager) -> Router:  # skip: noqa
    """Настройка хендлеров с передачей DataManager."""

    @router.message(Command("start"))
    async def cmd_start(msg: Message, bot: Bot) -> None:
        first_name: str = msg.from_user.first_name
        last_name: str = msg.from_user.last_name
        await msg.answer(
            messages.WELCOME.format(name=first_name or last_name or "Пришелец")
        )

    @router.message(Command("help"))
    async def cmd_help(msg: Message, bot: Bot) -> None:
        await msg.answer(messages.HELP)

    @router.message(Command("add"))
    async def cmd_add(msg: Message, state: FSMContext) -> None:
        assets = list(SUPPORTED_CRYPTOS.keys())
        keyboard, total_pages = create_paginated_keyboard(
            assets, "add_asset", items_per_page=5, page=0
        )
        await state.update_data(page=0, total_pages=total_pages)
        await msg.reply(messages.SELECT_ASSET, reply_markup=keyboard)
        await state.set_state(AddPurchase.asset)

    @router.callback_query(AddPurchase.asset, F.data.startswith("add_asset"))
    async def process_asset_selection(
        callback: CallbackQuery, state: FSMContext
    ) -> None:
        data = await state.get_data()
        page = data.get("page", 0)
        total_pages = data.get("total_pages", 1)
        action, value, *_ = callback.data.split(":")

        assets = list(SUPPORTED_CRYPTOS.keys())
        if value == "prev" and page > 0:
            page -= 1
            keyboard, _ = create_paginated_keyboard(
                assets, "add_asset", items_per_page=5, page=page
            )
            await state.update_data(page=page)
            await callback.message.edit_reply_markup(reply_markup=keyboard)
        elif value == "next" and page < total_pages - 1:
            page += 1
            keyboard, _ = create_paginated_keyboard(
                assets, "add_asset", items_per_page=5, page=page
            )
            await state.update_data(page=page)
            await callback.message.edit_reply_markup(reply_markup=keyboard)
        else:
            asset = value
            await state.update_data(asset=asset)
            await callback.message.edit_text("Введите цену покупки")
            await state.set_state(AddPurchase.price)
        await callback.answer()

    @router.message(AddPurchase.price)
    async def process_price(msg: Message, state: FSMContext) -> None:
        try:
            price = float(msg.text.strip())
            if price <= 0:
                raise ValueError("Цена должна быть положительной")
        except ValueError:
            await msg.reply(
                "Цена должна быть числом больше 0. Попробуйте снова"
            )
        else:
            await state.update_data(price=price)
            await msg.reply("Введите количество монет (например, 2.5)")
            await state.set_state(AddPurchase.amount)

    @router.message(AddPurchase.amount)
    async def process_amount(msg: Message, state: FSMContext) -> None:
        try:
            amount = float(msg.text.strip())
            if amount <= 0:
                raise ValueError("Количество должно быть положительным")
            await state.update_data(amount=amount)
            data = await state.get_data()
            output = messages.PURCHASE_INPUT_DATA.format(
                asset=data["asset"],
                price=data["price"],
                amount=data["amount"],
            )

            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="Подтвердить", callback_data="confirm_add"
                        ),
                        InlineKeyboardButton(
                            text="Отменить", callback_data="cancel_add"
                        ),
                    ]
                ]
            )
            await msg.answer(
                f"🏁 Все верно?\n{output}\n\n{messages.CONFIRM_ACTION}",
                reply_markup=keyboard,
            )
            await state.set_state(AddPurchase.confirm)
        except ValueError:
            await msg.reply(
                "Количество должно быть числом больше 0. Попробуйте снова"
            )

    @router.callback_query(
        AddPurchase.confirm, F.data.startswith("confirm_add")
    )
    async def process_confirm_add(
        callback: CallbackQuery, state: FSMContext
    ) -> None:
        data = await state.get_data()
        user_id = callback.from_user.id
        asset = data["asset"]
        price = data["price"]
        amount = data["amount"]

        data_manager.add_purchase(user_id, asset, price, amount)
        avg_price, total_amount, total_cost = data_manager.get_stats(
            user_id, asset
        )

        await callback.message.edit_text(
            messages.ADDED_PURCHASE_INFO.format(
                asset=asset,
                price=price,
                amount=amount,
                avg_price=avg_price,
                total_amount=total_amount,
                total_cost=total_cost,
            )
        )
        await state.clear()
        await callback.answer()

    @router.callback_query(
        AddPurchase.confirm, F.data.startswith("cancel_add")
    )
    async def process_cancel_add(
        callback: CallbackQuery, state: FSMContext
    ) -> None:
        await callback.message.edit_text(messages.ACTION_CANCELLED)
        await state.clear()
        await callback.answer()

    @router.message(Command("view"))
    async def cmd_view(msg: Message) -> None:
        user_id = msg.from_user.id
        assets = data_manager.get_user_assets(user_id)
        if not assets:
            await msg.reply(messages.NO_PURCHASES)
            return

        output_data: str = ""
        for asset in assets:
            avg_price, total_amount, total_cost = data_manager.get_stats(
                user_id,
                asset,
            )
            output_data += (
                messages.AVG_PRICE_INFO.format(
                    asset=asset,
                    avg_price=avg_price,
                    total_amount=total_amount,
                    total_cost=total_cost,
                )
                + "\n"
            )

        await msg.reply(output_data)

    @router.message(Command("clear"))
    async def cmd_clear(msg: Message, state: FSMContext) -> None:
        user_id = msg.from_user.id
        assets = data_manager.get_user_assets(user_id)

        if not assets:
            await msg.reply(messages.NO_PURCHASES_TO_CLEAR)
            return

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Подтвердить",
                        callback_data="confirm_clear",
                    ),
                    InlineKeyboardButton(
                        text="Отменить",
                        callback_data="cancel_clear",
                    ),
                ]
            ]
        )
        await msg.reply(messages.CONFIRM_ACTION, reply_markup=keyboard)
        await state.set_state(ClearData.confirm)

    @router.callback_query(
        ClearData.confirm, F.data.startswith("confirm_clear")
    )
    async def process_confirm_clear(
        callback: CallbackQuery, state: FSMContext
    ) -> None:
        user_id = callback.from_user.id
        data_manager.clear(user_id)
        await callback.message.edit_text(messages.DATA_CLEARED)
        await state.clear()
        await callback.answer()

    @router.callback_query(
        ClearData.confirm, F.data.startswith("cancel_clear")
    )
    async def process_cancel_clear(
        callback: CallbackQuery, state: FSMContext
    ) -> None:
        await callback.message.edit_text(messages.ACTION_CANCELLED)
        await state.clear()
        await callback.answer()

    @router.message(Command("list"))
    async def cmd_list(msg: Message) -> None:
        crypto_list = [
            messages.CRYPTO_ITEM.format(index=i + 1, name=name, ticker=ticker)
            for i, (ticker, name) in enumerate(SUPPORTED_CRYPTOS.items())
        ]
        await msg.reply(
            messages.SUPPORTED_CRYPTOS.format(
                currencies="\n".join(crypto_list)
            ),
        )

    @router.message(Command("delete"))
    async def cmd_delete(msg: Message, state: FSMContext) -> None:
        user_id = msg.from_user.id
        assets = data_manager.get_user_assets(user_id)

        if not assets:
            await msg.reply(messages.NO_PURCHASES_TO_DELETE)
            return

        keyboard, total_pages = create_paginated_keyboard(
            assets,
            "delete_asset",
            items_per_page=5,
        )
        await state.update_data(page=0, total_pages=total_pages)
        await msg.reply(messages.SELECT_ASSET, reply_markup=keyboard)
        await state.set_state(DeletePurchase.select_asset)

    @router.callback_query(
        DeletePurchase.select_asset, F.data.startswith("delete_asset")
    )
    async def process_delete_asset_selection(
        callback: CallbackQuery, state: FSMContext
    ) -> None:
        data = await state.get_data()
        page = data.get("page", 0)
        total_pages = data.get("total_pages", 1)
        action, value, *_ = callback.data.split(":")

        user_id = callback.from_user.id
        assets = data_manager.get_user_assets(user_id)

        if value == "prev" and page > 0:
            page -= 1
            keyboard, _ = create_paginated_keyboard(
                assets,
                "delete_asset",
                items_per_page=5,
                page=page,
            )
            await state.update_data(page=page)
            await callback.message.edit_reply_markup(reply_markup=keyboard)
        elif value == "next" and page < total_pages - 1:
            page += 1
            keyboard, _ = create_paginated_keyboard(
                assets,
                "delete_asset",
                items_per_page=5,
                page=page,
            )
            await state.update_data(page=page)
            await callback.message.edit_reply_markup(reply_markup=keyboard)
        else:
            asset = value
            await state.update_data(asset=asset)
            purchases = data_manager.get_purchases(user_id, asset)
            if not purchases:
                await callback.message.edit_text(
                    messages.NO_PURCHASES_FOR_ASSET
                )
                await state.clear()
                await callback.answer()
                return

            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text=messages.PURCHASE_INFO.format(
                                index=i + 1,
                                price=p["price"],
                                amount=p["amount"],
                            ),
                            callback_data=f"delete_purchase_{i}",
                        )
                    ]
                    for i, p in enumerate(purchases)
                ]
            )
            await callback.message.edit_text(
                messages.SELECT_PURCHASE, reply_markup=keyboard
            )
            await state.set_state(DeletePurchase.select_purchase)
        await callback.answer()

    @router.callback_query(
        DeletePurchase.select_purchase, F.data.startswith("delete_purchase")
    )
    async def process_delete_purchase_selection(
        callback: CallbackQuery, state: FSMContext
    ) -> None:
        purchase_index = int(callback.data.split("_")[-1])
        await state.update_data(purchase_index=purchase_index)

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Подтвердить", callback_data="confirm_delete"
                    ),
                    InlineKeyboardButton(
                        text="Отменить", callback_data="cancel_delete"
                    ),
                ]
            ]
        )
        await callback.message.edit_text(
            messages.CONFIRM_ACTION, reply_markup=keyboard
        )
        await state.set_state(DeletePurchase.confirm)
        await callback.answer()

    @router.callback_query(
        DeletePurchase.confirm, F.data.startswith("confirm_delete")
    )
    async def process_confirm_delete(
        callback: CallbackQuery, state: FSMContext
    ) -> None:
        data = await state.get_data()
        user_id = callback.from_user.id
        asset = data["asset"]
        purchase_index = data["purchase_index"]

        data_manager.delete_purchase(user_id, asset, purchase_index)
        await callback.message.edit_text(messages.DELETED_PURCHASE)
        await state.clear()
        await callback.answer()

    @router.callback_query(
        DeletePurchase.confirm, F.data.startswith("cancel_delete")
    )
    async def process_cancel_delete(
        callback: CallbackQuery, state: FSMContext
    ) -> None:
        await callback.message.edit_text(messages.ACTION_CANCELLED)
        await state.clear()
        await callback.answer()

    @router.message(Command("export"))
    async def cmd_export(msg: Message) -> None:
        user_id: int = msg.from_user.id
        rows: list[dict[str, str]] = data_manager.export_to_csv(user_id)

        if not rows:
            await msg.reply(messages.NO_DATA_TO_EXPORT)
            return

        csv_file: str = f"purchases_{user_id}.csv"
        with open(csv_file, "w", newline="", encoding="UTF-8") as file:
            writer = csv.DictWriter(
                file, fieldnames=["user_id", "asset", "price", "amount"]
            )
            writer.writeheader()
            writer.writerows(rows)

        await msg.reply_document(FSInputFile(csv_file))
        os.remove(csv_file)

    return router

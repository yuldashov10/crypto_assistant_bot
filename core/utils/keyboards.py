from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def create_paginated_keyboard(
    items: list[str],
    callback_prefix: str,
    items_per_page: int = 5,
    page: int = 0,
) -> tuple[InlineKeyboardMarkup, int]:
    """
    Создает инлайн-клавиатуру с пагинацией.

    :param items: Список элементов для отображения.
    :param callback_prefix: Префикс для callback_data.
    :param items_per_page: Количество элементов на странице.
    :param page: Текущая страница.
    :return: Клавиатура и общее количество страниц.
    """
    total_items: int = len(items)
    total_pages: int = (total_items + items_per_page - 1) // items_per_page

    if total_pages == 0:
        total_pages = 1

    page: int = max(0, min(page, total_pages - 1))
    start_idx: int = page * items_per_page
    end_idx: int = min(start_idx + items_per_page, total_items)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=items[idx],
                    callback_data=f"{callback_prefix}:{items[idx]}:{page}",
                )
            ]
            for idx in range(start_idx, end_idx)
        ],
        row_width=5,
    )

    nav_buttons = []
    if page > 0:
        nav_buttons.append(
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data=f"{callback_prefix}:prev:{page}",
            )
        )
    if page < total_pages - 1:
        nav_buttons.append(
            InlineKeyboardButton(
                text="Вперед ➡️",
                callback_data=f"{callback_prefix}:next:{page}",
            )
        )
    if nav_buttons:
        keyboard.row(*nav_buttons)

    return keyboard, total_pages

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def start() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Добавить задачу")
    kb.button(text="Показать список задач")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


def add_task() -> InlineKeyboardBuilder:
    kb = InlineKeyboardBuilder()
    return kb.as_markup()


def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)

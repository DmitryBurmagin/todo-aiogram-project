from aiogram import types
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def start() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Добавить задачу")
    kb.button(text="Показать список задач")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


def add_task() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    return builder.as_markup()


def task_list_kb() -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text='Актуальные задачи',
        callback_data='show_current_tasks'
    ))
    builder.row(types.InlineKeyboardButton(
        text='Выполненые задачи',
        callback_data='show_completed_tasks'
    ))
    return builder.as_markup()


def show_task_kb(task_id: int) -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Удалить",
        callback_data=f"drop_task {task_id}")
    )
    return builder.as_markup()


def create_task_kb(task_id: int) -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text='Отметить выполненой',
        callback_data=f'complite {task_id}')
        )
    builder.add(types.InlineKeyboardButton(
        text='Удалить запись',
        callback_data=f'drop_task {task_id}')
        )
    return builder.as_markup()

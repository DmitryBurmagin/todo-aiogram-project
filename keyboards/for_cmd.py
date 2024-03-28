from aiogram import types
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def start_kb() -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text='Добавить задачу',
        callback_data='add_task')
                )
    builder.add(types.InlineKeyboardButton(
        text='Показать список задач',
        callback_data='task_list')
                )
    return builder.as_markup()


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
        text="Выполнено",
        callback_data=f"complite {task_id}")
    )
    builder.add(types.InlineKeyboardButton(
        text="Удалить",
        callback_data=f"drop_task {task_id}")
    )
    return builder.as_markup()


def create_task_kb(task_id: int) -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text='Выполнено',
        callback_data=f'complite {task_id}')
        )
    builder.add(types.InlineKeyboardButton(
        text='Изменить',
        callback_data=f'update {task_id}')
        )
    builder.add(types.InlineKeyboardButton(
        text='Удалить',
        callback_data=f'drop_task {task_id}')
        )
    builder.add(types.InlineKeyboardButton(
        text='Добавить новую задачу',
        callback_data='add_task')
        )
    builder.add(types.InlineKeyboardButton(
        text='Список задач',
        callback_data='task_list')
        )
    builder.adjust(3)
    return builder.as_markup()

from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards.for_cmd import start, task_list_kb, show_task_kb, create_task_kb
from models.services import delete_task, create_task, task_list


router = Router()


@router.message(Command('start'))
async def cmd_start(message: Message):
    await message.answer('Выберите действие', reply_markup=start())


@router.message(F.text.lower() == 'показать список задач')
async def task_list_choice(message: types.Message):
    await message.answer('Выберите задачи: ', reply_markup=task_list_kb())


@router.callback_query(F.data == 'show_current_tasks')
async def show_current_task(callback: types.CallbackQuery):
    telegram_id = callback.from_user.id
    tasks = await task_list(telegram_id)
    if tasks:
        for task in tasks:
            if not task.completed:
                task_id = show_task_kb(task.id)
                await callback.message.answer(
                    f'Задача {task.id}: {task}',
                    reply_markup=task_id
                )
                await callback.answer('')
    else:
        await callback.answer(
            text='У вас нету добавленых задач',
            show_alert=True)


@router.callback_query(F.data == 'show_completed_tasks')
async def show_completed_tasks(callback: types.CallbackQuery):
    telegram_id = callback.from_user.id
    tasks = await task_list(telegram_id)
    if tasks:
        for task in tasks:
            if task.completed:
                task_id = show_task_kb(task.id)
                await callback.message.answer(
                    f'Задача {task.id}: {task}',
                    reply_markup=task_id
                )
                await callback.answer('')
            else:
                await callback.answer(
                    text='У вас нет выполненых задач',
                    show_alert=True)


class Form(StatesGroup):
    task_one_step = State()
    task_two_step = State()


@router.message(F.text.lower() == 'добавить задачу')
async def enter_task(message: Message, state: FSMContext):
    await message.answer("Введите задачу: ")
    await state.set_state(Form.task_one_step.state)


@router.message(Form.task_one_step)
async def add_task(message: Message, state: FSMContext):
    task_text = message.text.strip()
    telegram_id = message.from_user.id
    task_id = await create_task(task_text, telegram_id)
    keyboard = create_task_kb(task_id)
    await state.clear()
    await message.answer(
        text=f'Задача {task_text} добавлена.',
        reply_markup=keyboard
    )


@router.callback_query(F.data.startswith('drop_task'))
async def drop_task(callback: types.CallbackQuery):
    _, task_id = callback.data.split()
    task_id = int(task_id)
    await delete_task(task_id)
    await callback.answer(
        text='Задача удалена',
        show_alert=True)

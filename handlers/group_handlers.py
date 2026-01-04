from aiogram import F, Router, types, Bot
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message, CallbackQuery
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import FSInputFile
from datetime import datetime
import asyncio

from keyboards import start_kb
import Text
import database.requests as rq
import function.create_session as CreateSes
from main import bot
import pandas as pd
import Media

router = Router()

class Delit_Group(StatesGroup):
    group = State()

class Add_Group(StatesGroup):
    url = State()
    minuts = State()
    message = State()


async def create_text_groups():
    links_link = await rq.get_data_all_groups()
    text = ""
    for link in links_link:
        link = link.__dict__
        text = text + f"{link["url"]}\n"
    if len(text) > 1:
        return text[1:]
    else:
        return "Группы не добавлены ❌"
    


@router.callback_query(F.data == 'redact_group')
async def add_account(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    data = await rq.get_data_group()
    data = data.__dict__
    if data["work_type"]:
        status_start = "Работает ✅"
        reply_keybord = start_kb.grop_redackt_1
    else:
        status_start = "Остановлена ❌"
        reply_keybord = start_kb.grop_redackt
    links_list = await create_text_groups()
    await callback.message.answer(text=Text.redact_group.format(
        status_start, data["count_minuts"], links_list, data["message"]
    ), reply_markup=reply_keybord)

@router.callback_query(F.data == 'downl_base')
async def add_account(callback: CallbackQuery, state: FSMContext):
    data = await rq.get_data_all_groups()
    data_end = []
    for t in data:
        info = {'ID': t.id, 'Ссылка': t.url, 'Интервал между сообщениями': t.count_minuts, 'Текст рассылки': t.message}
        data_end.append(info)
    df = pd.DataFrame(data_end)
    df.to_excel("exel_base.xlsx", index=False)
    document = FSInputFile('exel_base.xlsx')
    await callback.message.answer_document(document=document)

#@router.callback_query(F.data == 'del_chat')
#async def add_account(callback: CallbackQuery, state: FSMContext):
#    await state.set_state(Delit_Group.group)
#    await callback.message.answer(text=Text.delit_group, reply_markup=start_kb.back_menu)

@router.callback_query(F.data == 'add_chat')
async def add_account(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Add_Group.url)
    await callback.message.answer(text=Text.add_group, reply_markup=start_kb.back_menu)

@router.callback_query(F.data == 'redact_message')
async def add_account(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Add_Group.message)
    await callback.message.answer(text=Text.add_group_2, reply_markup=start_kb.back_menu)

@router.callback_query(F.data == 'redact_period')
async def add_account(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Add_Group.minuts)
    await callback.message.answer(text=Text.add_group_1, reply_markup=start_kb.back_menu)


@router.callback_query(F.data == 'start_work')
async def add_account(callback: CallbackQuery, state: FSMContext):
    data = await rq.get_data_all_groups()
    for x in range(len(data)):
        await rq.redact_data_group(x+1, "work_type", True)
        date_now = datetime.now()
        await rq.redact_data_group(x+1, "next_message", date_now)
    await callback.message.answer(text=Text.start_spam_text)

@router.callback_query(F.data == 'stop_work')
async def add_account(callback: CallbackQuery, state: FSMContext):
    data = await rq.get_data_all_groups()
    for x in range(len(data)):
        await rq.redact_data_group(x+1, "work_type", False)
    await callback.message.answer(text=Text.stop_text)


@router.message(Add_Group.url)
async def get_name(message: Message, state: FSMContext):
    data = await rq.get_data_group()
    data = data.__dict__
    await rq.set_account_group(message.text, data["count_minuts"], data["message"])
    await message.answer(text=Text.add_group_3)
    await state.clear()

@router.message(Add_Group.minuts)
async def get_name(message: Message, state: FSMContext):
    data = await rq.get_data_all_groups()
    for x in range(len(data)):
        await rq.redact_data_group(x+1, "count_minuts", int(message.text))
    await state.clear()
    await message.answer(text=Text.time_redact_text)


@router.message(Add_Group.message)
async def get_name(message: Message, state: FSMContext):
    data = await rq.get_data_all_groups()
    for x in range(len(data)):
        await rq.redact_data_group(x+1, "message", message.html_text)
    await state.clear()
    await message.answer(text=Text.add_group_4)



@router.message(Delit_Group.group)
async def get_name(message: Message, state: FSMContext):
    groups=message.text
    data = await rq.get_data_all_groups()
    for t in data:
        if t.url == groups: # Перебираем все ссылки в группах для поиска необходимой
            await rq.delete_one_group(groups)
            await message.answer(Text.delit_group_step_1.format(groups))
            await state.clear()
            return
    await message.answer(Text.delit_group_step_2.format(groups))
    await state.clear()
from aiogram import F, Router, types, Bot
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message, CallbackQuery
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from datetime import datetime
import asyncio
from pyrogram import Client

from keyboards import start_kb
import Text
import database.requests as rq
import function.create_session as CreateSes
from main import bot
import Media
from main import admin_id
from datetime import timedelta

router = Router()

class Add_account(StatesGroup):
    name = State()
    phone_number = State()
    api_id = State()
    api_hash = State()

class Activate_account(StatesGroup):
    code = State()
    code_hash = State()
    client = State()

async def cheack_account():
    try:
        acc_data = await rq.get_data_acconts()
        acc_data = acc_data.__dict__
        text = f"""
Имя - {acc_data["name"]}
Номер телефона - {acc_data["phone_number"]}
API id - {acc_data["api_id"]}
API Hash - {acc_data['api_hash']}
"""
        return text
    except:
        text = "Аккаунт не добавлен ❌"
        return text


async def create_text_links():
    links_link = await rq.get_data_all_groups()
    text = ""
    for link in links_link:
        link = link.__dict__
        text = text + f"\n{link["url"]} - {link["count_minuts"]}"
    if len(text) > 1:
        return text
    else:
        return "Группы не добавлены ❌"
    
@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()
    await rq.set_user(message.from_user.id, message.from_user.username)
    admin = await rq.admin_cheak(message.from_user.id)
    if admin:
        data_account = await cheack_account()
        links = await create_text_links()
        if data_account == "Аккаунт не добавлен ❌":
            await message.answer(Text.start_text.format(data_account, links), reply_markup=start_kb.start_kb)
        else:
            acc_data = await rq.get_data_acconts()
            acc_data = acc_data.__dict__
            if acc_data["activated"]:
                await message.answer(Text.start_text.format(data_account, links), reply_markup=start_kb.start_kb_with_activated_acc)
            else:
                await message.answer(Text.start_text.format(data_account, links), reply_markup=start_kb.start_kb_with_not_activated_acc)

@router.callback_query(F.data == 'main_back')
async def add_account(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await rq.set_user(callback.message.from_user.id, callback.message.from_user.username)
    admin = await rq.admin_cheak(callback.message.from_user.id)
    if admin:
        data_account = await cheack_account()
        links = await create_text_links()
        if data_account == "Аккаунт не добавлен ❌":
            await callback.message.answer(Text.start_text.format(data_account, links), reply_markup=start_kb.start_kb)
        else:
            acc_data = await rq.get_data_acconts()
            acc_data = acc_data.__dict__
            if acc_data["activated"]:
                await callback.message.answer(Text.start_text.format(data_account, links), reply_markup=start_kb.start_kb_with_activated_acc)
            else:
                await callback.message.answer(Text.start_text.format(data_account, links), reply_markup=start_kb.start_kb_with_not_activated_acc)
    
@router.callback_query(F.data == 'add_account')
async def add_account(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Add_account.name)
    await callback.message.answer(text=Text.write_name)

@router.callback_query(F.data == 'activate_account')
async def add_account(callback: CallbackQuery, state: FSMContext):
    acc_data = await rq.get_data_acconts()
    acc_data = acc_data.__dict__
    client = CreateSes.get_pyro_client(str(acc_data["id"]), acc_data["phone_number"], acc_data["api_id"], acc_data["api_hash"])
    send_code = await CreateSes.send_code(client, acc_data["phone_number"])

    await state.set_state(Activate_account.client)
    await state.update_data(client = client)
    await state.set_state(Activate_account.code_hash)
    await state.update_data(code_hash = send_code.phone_code_hash)
    await state.set_state(Activate_account.code)
    await callback.message.answer(text=Text.request_code)

# Функционал активации аккаунта
@router.message(Activate_account.code)
async def get_code(message: Message, state: FSMContext):
    await state.update_data(code=message.text)
    data = await state.get_data()

    acc_data = await rq.get_data_acconts()
    acc_data = acc_data.__dict__

    client = data["client"]
    phone = acc_data["phone_number"]
    code=data["code"].strip()
    phone_code_hash=data["code_hash"]
    try:
        await CreateSes.sign_in(
            client=client,
            phone=phone,
            code=code,
            phone_code_hash=phone_code_hash
        )
    except Exception as e:
        await message.answer(f"Ошибка авторизации: {e}")
        return

    await message.answer("Аккаунт успешно активирован.")
    await rq.redact_data_user("activated", True)
    await state.clear()

# Функционал добавления нового аккаунта
@router.message(Add_account.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Add_account.phone_number)
    await message.answer(text=Text.write_phone)

@router.message(Add_account.phone_number)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    await state.set_state(Add_account.api_id)
    await message.answer(text=Text.api_id)

@router.message(Add_account.api_id)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(api_id=message.text)
    await state.set_state(Add_account.api_hash)
    await message.answer(text=Text.api_hash)

@router.message(Add_account.api_hash)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(api_hash=message.text)
    data_states = await state.get_data()
    await rq.set_account(data_states["name"], data_states["phone_number"], data_states["api_id"], data_states["api_hash"])
    await message.answer(text=Text.new_account)
        
#@router.message(F.photo)
#async def get_data_message(message: Message):
#    print(message.photo[-1].file_id)
#
#@router.message()
#async def get_data_message(message: Message):
#    print(message)

async def message_push_user():
    groups = await rq.get_data_all_groups()
    for grop in groups:
        grop = grop.__dict__
        start_data = datetime.now()
        if grop["next_message"] < start_data:
            if grop["work_type"]:
                next_message = datetime.now() + timedelta(minutes=int(grop["count_minuts"]))
                await rq.redact_data_group(grop["id"], "next_message", next_message)

                acc_data = await rq.get_data_acconts()
                acc_data = acc_data.__dict__
                userbot = Client(name=str(acc_data["id"]),
                         api_id=acc_data["api_id"],
                         api_hash=acc_data["api_hash"],
                         phone_number=acc_data["phone_number"])

                await userbot.start()
                try:
                    await userbot.send_message(chat_id=grop["url"], text=grop["message"])
                    await bot.send_message(admin_id, Text.send_suksess.format(grop["url"], grop["message"]))
                except Exception as e:
                    print(f"Возникла ошибка: {e}")
                await userbot.stop()
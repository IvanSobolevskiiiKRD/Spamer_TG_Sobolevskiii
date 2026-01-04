from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
import database.requests as rq
import math

start_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Добавить аккаунт', callback_data="add_account")],
    [InlineKeyboardButton(text='Редактировать группы', callback_data="redact_group")]
])

back_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='❌ Отменить❌ ', callback_data="main_back")]
])

start_kb_with_not_activated_acc = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Активировать аккаунт', callback_data="activate_account")],
    [InlineKeyboardButton(text='Редактировать группы', callback_data="redact_group")]
])

start_kb_with_activated_acc = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Редактировать группы', callback_data="redact_group")]
])

grop_redackt = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Изменить сообщение', callback_data="redact_message")],
    [InlineKeyboardButton(text='Изменить периуд', callback_data="redact_period")],
    [InlineKeyboardButton(text='Добавить группу', callback_data="add_chat")],
    [InlineKeyboardButton(text='Запустить рассылку ✅', callback_data="start_work")]
])

grop_redackt_1 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Изменить сообщение', callback_data="redact_message")],
    [InlineKeyboardButton(text='Изменить периуд', callback_data="redact_period")],
    [InlineKeyboardButton(text='Добавить группу', callback_data="add_chat")],
    [InlineKeyboardButton(text='Остановить рассылку ❌', callback_data="stop_work")],
])
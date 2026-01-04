from database.models import async_session
from database.models import User, Account, Group
from sqlalchemy import select, update, delete
from datetime import datetime
from datetime import timedelta

async def set_user(telegram_id, username):
    async with async_session() as session:
        start_data = datetime.now()
        user = await session.scalar(select(User).where(User.tg_id == telegram_id))

        if not user:
            session.add(User(tg_id=telegram_id, admin=False, username=username))
            await session.commit()
            return True
        else:
            return False
        
async def set_prob_zanatia(telegram_id):
    async with async_session() as session:
        await session.execute(update(User).where(User.tg_id == telegram_id).values({"prob_zanatia": True}))
        await session.commit()

async def admin_cheak(telegram_id):
    async with async_session() as session:
        return await session.scalar(select(User.admin).where(User.tg_id == telegram_id))
    
async def set_admin(telegram_id):
    async with async_session() as session:
        await session.execute(update(User).where(User.tg_id == telegram_id).values({"admin": True}))
        await session.commit()

async def get_data_all_user():
    async with async_session() as session:
        res =  await session.execute(select(User))
        return res.scalars().all()
    
async def get_data_one_user(telegram_id):
    async with async_session() as session:
        return await session.scalar(select(User).where(User.tg_id == telegram_id))
    
async def redact_data_user(tg_id, col, new_data):
    async with async_session() as session:
        await session.execute(update(User).where(User.tg_id == tg_id).values(**{col: new_data}))
        await session.commit()

async def get_data_acconts():
    async with async_session() as session:
        return await session.scalar(select(Account).where(Account.id == 1))
    
async def redact_data_user(col, new_data):
    async with async_session() as session:
        await session.execute(update(Account).where(Account.id == 1).values(**{col: new_data}))
        await session.commit()

async def set_account(name, phone, api_id, api_hash):
    async with async_session() as session:
        session.add(Account(name=name, phone_number=phone, api_id=api_id, api_hash=api_hash, activated=False))
        await session.commit()

async def get_data_all_groups():
    async with async_session() as session:
        res =  await session.execute(select(Group))
        return res.scalars().all()

async def get_data_group():
    async with async_session() as session:
        return await session.scalar(select(Group).where(Group.id == 1))

async def set_account_group(url, count_minuts, message):
    async with async_session() as session:
        next_message = datetime.now() + timedelta(minutes=int(count_minuts))
        session.add(Group(url=url, count_minuts=count_minuts, message=message, next_message=next_message, work_type=False))
        await session.commit()
    
async def redact_data_group(id, col, new_data):
    async with async_session() as session:
        await session.execute(update(Group).where(Group.id == id).values(**{col: new_data}))
        await session.commit()

async def delete_one_group(url):
    async with async_session() as session:
        await session.execute(delete(Group).where(Group.url == url))
        await session.commit()
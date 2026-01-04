from pyrogram import Client

def get_pyro_client(session_name, phone, api_id, api_hash):
    return Client(
        name=session_name,
        phone_number=phone,
        api_id=api_id,
        api_hash=api_hash
    )

async def send_code(client: Client, phone: str):
    await client.connect()
    sent_code = await client.send_code(phone)
    return sent_code

async def sign_in(client: Client, phone: str, code: str, phone_code_hash: str):
    await client.sign_in(
        phone_number=phone,
        phone_code=code,
        phone_code_hash=phone_code_hash
    )
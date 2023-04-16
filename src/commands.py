from api import api
from uuid import UUID
from api import db

import asyncio
UUID_VERSION = 4

def is_valid_key(uuid_to_test:str):
    try:
        uuid_obj = UUID(uuid_to_test, version=UUID_VERSION)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test and api.is_valid_wanikani_api(uuid_to_test)


async def handle_user_cmd(message):
    strings = message.content.split(" ")
    if len(strings)  < 3:
        api.get_request_headers_for_user()
    if len(strings == 1):
        if db.is_user_registered(message.author.name):
            user_information = api.request_user_information(message.author.name)
        else:
            user_not_registered_message = "You're not registered with the bot! Use the command !register in order to send commands to the bot."
            await message.channel.send(user_not_registered_message)
    elif len(strings == 2):
        user_to_check = strings[1]
        if db.is_user_registered(message.author.name):
            user_information = api.request_user_information(user_to_check)
        else:
            await message.channel.send(f"Error: User '{user_to_check}' is not registered with the bot.")
    else:
        await message.channel.send("Error: Too many arguments added.Use the command with !user or !user {user_name}.")


async def register_user(bot,author):
    registration_message = f"Hi {author.name}! Please send your Wanikani API Key to register yourself with the Kamesama bot."
    author.send(registration_message)
    def check(m):
        return is_valid_key(m.content)
    try:
        response = await bot.wait_for("message",check=check)
    except asyncio.TimeoutError:
        await author.send('👎. The message sent is not a valid Wanikani API key.')
    else:
        db.register_user(author.name,response)
        await author.send("👍. You are now registered with Kamesama. Enjoy!")

    

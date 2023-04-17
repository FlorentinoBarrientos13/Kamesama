import profile
from api  import api
from uuid import UUID
from api import db
import pprint

import asyncio
UUID_VERSION = 4

def is_valid_key(uuid_to_test:str):
    try:
        uuid_obj = UUID(uuid_to_test, version=UUID_VERSION)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test and api.is_valid_api_key(uuid_to_test)


async def handle_user_cmd(ctx,user):
    is_self =  user == "self"
    username = ctx.author.name if user == "self" else user
    if db.is_user_registered(ctx.author.name):
        user_information = api.request_user_information(username)
        print(user_information)
    else:
        user_not_registered_message = "You're not registered with the bot! Use the command ?register in order to send commands to the bot."
        not_registered_user = f"Error: User '{user}' is not registered with the bot."
        await ctx.channel.send(user_not_registered_message if is_self else not_registered_user)


async def register_user(bot,author):
    if db.is_user_registered(author.name):
        await author.send("You're already registered with Kamesama.")
        return

    registration_message = f"Hi {author.name}! Please send your Wanikani API Key to register yourself with the Kamesama bot."
    await author.send(registration_message)
    def check(m):
        return is_valid_key(m.content)
    try:
        response = await bot.wait_for("message",check=check)
    except asyncio.TimeoutError:
        await author.send('👎. The message sent is not a valid Wanikani API key or timed out waiting for message.')
    else:
        db.register_user(author.name,response.content.strip())
        await author.send("👍. You are now registered with Kamesama. Enjoy!")

    
async def handle_streaks(ctx,user):
    is_self =  user == "self"
    username = ctx.author.name if user == "self" else user
    if db.is_user_registered(ctx.author.name):
        print(api.get_user_streaks(username))
    else:
        user_not_registered_message = "You're not registered with the bot! Use the command ?register in order to send commands to the bot."
        not_registered_user = f"Error: User '{user}' is not registered with the bot."
        await ctx.channel.send(user_not_registered_message if is_self else not_registered_user)

def handle_server_levels():
    profiles =  api.get_server_levels_leaderboard()
    [print(str(i)) for i in profiles]
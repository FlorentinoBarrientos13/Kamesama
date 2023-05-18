from api  import api
from uuid import UUID
from api import db
from tabulate import tabulate
import discord

import asyncio
UUID_VERSION = 4

def is_valid_key(uuid_to_test:str):
    try:
        uuid_obj = UUID(uuid_to_test, version=UUID_VERSION)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test and api.is_valid_api_key(uuid_to_test)


async def handle_user_cmd(interaction:discord.Interaction,user:str):
    is_self =  user == ""
    username = interaction.user.name if is_self else user
    if db.is_user_registered(interaction.user.name):
        user_information = api.request_user_information(username)
        await interaction.response.send_message(user_information)
    else:
        user_not_registered_message = "You're not registered with the bot! Use the command ?register in order to send commands to the bot."
        not_registered_user = f"Error: User '{user}' is not registered with the bot."
        await interaction.response.send_message(user_not_registered_message if is_self else not_registered_user)

async def deregister(bot,author):
    if db.is_user_registered(author.name):
        db.deregister_user(author.name)
        

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
    except Exception as e:
        await author.send('👎. The message sent is not a valid Wanikani API key or timed out waiting for message.')
    else:
        db.register_user(author.name,response.content.strip())
        await author.send("👍. You are now registered with Kamesama. Enjoy!")

    
async def handle_streaks(interaction:discord.Interaction):
    if db.is_user_registered(interaction.user.name):
        api.get_user_streaks(interaction.user.name)
    else:
        user_not_registered_message = "You're not registered with the bot! Use the command '/register' to register yourself with the bot."
        not_registered_user = f"Error: User '{interaction.user.name}' is not registered with the bot."
        await interaction.response.send_message(user_not_registered_message )

async def handle_server_levels(interaction:discord.Interaction):
    profiles  =  api.get_server_levels_leaderboard()
    table = []
    table.append(["Username", "Level"])
    [table.append([i.username, i.level]) for i in profiles]
    tabulate_string =  "```" + tabulate(table, headers='firstrow', tablefmt='grid')+ "```"
    await interaction.response.send_message(tabulate_string)

async def get_server_available_items(interaction:discord.Interaction, choice:str):
    reviews =  choice == "reviews" 
    users = db.get_registered_users()
    table_items = list(map(lambda x:(x, api.get_user_available_reviews_and_lessons(x)[0] if reviews else api.get_user_available_reviews_and_lessons(x)[1]) , users))
    table_items.sort(reverse=True, key=lambda x : x[1])
    table = []
    table.append(["Username", "Reviews" if reviews else "Lessons"])
    [table.append([i[0],i[1]]) for i in table_items]
    tabulate_string =  "```" + tabulate(table, headers='firstrow', tablefmt='grid')+ "```"
    await interaction.response.send_message(tabulate_string)



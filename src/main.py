from typing import Union
from api import api
from api import db
from dotenv import load_dotenv
import discord
from discord.ext import commands
import api.commands as user_commands
import os

load_dotenv()
TOKEN = os.getenv('TOKEN')
intents = discord.Intents.default()
#pylint: disable=assigning-non-slot
intents.message_content = True
bot = discord.ext.commands.Bot(command_prefix=commands.when_mentioned_or('?'),intents = intents)    


@bot.command(name='register')
async def register(ctx):
    await user_commands.register_user(bot, ctx.author)

@bot.command(name='user')
async def show_user(ctx,arg :Union[discord.User ,str]):
    await user_commands.handle_user_cmd(ctx,arg)

@bot.command(name='streaks')
async def handle_streaks(ctx,arg :Union[discord.User ,str]):
    if arg == "server":
        user_commands.handle_server_levels()
    else:
        await user_commands.handle_streaks(ctx,arg)


    

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


if __name__ == "__main__":    
    print(TOKEN)
    bot.run(TOKEN)
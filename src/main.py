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
intents.message_content = True
bot = discord.ext.commands.Bot(command_prefix=commands.when_mentioned_or('?'),intents = intents)    


@bot.command(name='register')
async def register(ctx):
    await user_commands.register_user(bot, ctx.author)

@bot.command(name='user')
async def show_user(ctx,arg):
    await user_commands.handle_user_cmd(ctx,arg)


    

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


if __name__ == "__main__":    
    print(TOKEN)
    bot.run(TOKEN)
from api import api
from api import db
from dotenv import load_dotenv
from discord.ext import commands


import commands
import os

load_dotenv()
TOKEN = os.getenv('TOKEN')

bot = commands.Bot(command_prefix="!")    


@bot.event
async def on_message(message):
    if message.author == bot.user: 
        return
    if message.content.startswith("register"):
        commands.register_user(message)
    elif message.content.startswith("user"):
        commands.handle_user_cmd(message)
    elif message.content.startswith("streaks"):
        commands.handle_streaks
        pass
    elif message.content.startswith("test"):
        content = 'Bot is up and running!'
        await message.channel.send(content)

    await bot.process_commands(message)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


if __name__ == "__main__":    
    bot.run(TOKEN)
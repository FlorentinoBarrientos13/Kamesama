from typing import Union
from dotenv import load_dotenv
import discord
from discord import app_commands
from discord.ext import commands
import api.commands as api
import os

load_dotenv()
TOKEN = os.getenv('TOKEN')
intents = discord.Intents.default()
# pylint: disable=assigning-non-slot
intents.message_content = True
bot = commands.Bot(command_prefix="", intents = intents)    



@bot.tree.command(name = "register", description = "Registers the user with Kamesama with your Wanikani API token.") 
async def register(interaction: discord.Interaction):
    await interaction.response.send_message(f"A message with instructions to register yourself has been sent to your DMs!")
    await api.register_user(bot, interaction.user)

@bot.tree.command(name = "streaks", description = "Caculates the users current streak.") 
async def show_streaks(interaction: discord.Interaction):
    await api.handle_streaks(interaction)


@bot.tree.command(name = "deregister", description = "Removes the user from Kamesama active users.") 
async def deregister(interaction: discord.Interaction):
    await api.deregister(bot, interaction.user)
    await interaction.response.send_message(f"{interaction.user} successfully removed from Kamesama")

@bot.tree.command(name = "levels", description = "Shows the leaderboard of levels") 
async def show_levels(interaction: discord.Interaction):
    await api.handle_server_levels(interaction)


@bot.tree.command(name = "user", description = "Shows the current user stats") 
@app_commands.describe(user = "The user to show the stats ")
async def show_user(interaction: discord.Interaction,user:str=''):
    await api.handle_user_cmd(interaction,user)


@bot.tree.command(name = "lessons", description = "Shows the number of lessons each member has within the server.") 
async def show_lessons(interaction: discord.Interaction,):
    await api.get_server_available_items(interaction,"lessons")

@bot.tree.command(name = "reviews", description = "Shows the number of reviews each member has within the server.") 
async def show_reviews(interaction: discord.Interaction,):
    await api.get_server_available_items(interaction,"reviews")


    

@bot.event
async def on_ready():
    
    print(f'{bot.user} has connected to Discord!')
    try:
        sync = await bot.tree.sync()
        print("commands synched")
    except Exception  as e:
        print(e)


if __name__ == "__main__":    
    print(TOKEN)
    bot.run(TOKEN)
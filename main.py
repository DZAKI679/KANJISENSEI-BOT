import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import requests
import random

# Load environment variables from .env file
load_dotenv()

# Get the Discord token from the environment variables
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Handler for logging
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Create a bot instance with the specified command prefix and intents
bot = commands.Bot(command_prefix='/', intents=intents)


# Event handler for when the bot is ready
@bot.event
async def on_ready():

    print(f'全部準備できたら {bot.user} としてログインしました！')

@bot.event
async def setup_hook():
    await bot.tree.sync()  # Sync the command tree with Discord

#===============|コマンド|===============＃







#pingコマンド
@bot.tree.command(name="ping",
                description="Ping the bot to check if it's responsive."
                )

async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")


#latencyコマンド
@bot.tree.command(name="latency",
                  description="Check the bot's Latency."
                  )
async def latency(interaction: discord.Interaction):
    Latency = round(bot.latency * 1000)
    await interaction.response.send_message(f"Botのレイテンシーは {Latency} ms です。")


#tagコマンド
@bot.tree.command(name="tag",
                  description="To Tag a user with a message."
                  )
async def tag(interaction: discord.Interaction, user: discord.Member, message: str):
    await interaction.response.send_message(f"{user.mention} {message}")


#spamtagコマンド
@bot.tree.command(name="spamtag",
                  description="To Tag a user with a message multiple times, You can only tag up to 10 times."
                  )
async def spamtag(interaction: discord.Interaction, user: discord.Member, message: str, times: int):
    if times > 10:
        await interaction.response.send_message("You can only tag a user up to 10 times.")
        return
    if times < 1:
        await interaction.response.send_message("You must tag a user at least once.")
        return

    await interaction.response.send_message(f"Tagging {user.mention} {times} times with the message: {message}")
    times = times + 1  # Increment times by 1 to include the initial message
    for _ in range(times):
        await interaction.channel.send(f"{user.mention} {message}")


#漢字generateコマンド
@bot.tree.command(
    name="kanji_n5",
    description="Generate a random Kanji character."
)
async def kanji_n5(interaction: discord.Interaction):
    try:
        
        # Ambil daftar kanji Grade 1
        random_response = requests.get("https://kanjiapi.dev/v1/kanji/grade-1")
        random_response.raise_for_status()

        kanji_list = random_response.json()
        kanji = random.choice(kanji_list)

        # Ambil detail kanji
        detail_response = requests.get(f"https://kanjiapi.dev/v1/kanji/{kanji}")
        detail_response.raise_for_status()
        data = detail_response.json()

        embed = discord.Embed(
            title=f"Random Kanji: {data['kanji']}",
            color=discord.Color.blue()
        )

        embed.add_field(
            name="📖 On Readings",
            value=", ".join(data["on_readings"]) or "None",
            inline=False
        )

        embed.add_field(
            name="📚 Kun Readings",
            value=", ".join(data["kun_readings"]) or "None",
            inline=False
        )

        embed.add_field(
            name="💡 Meanings",
            value=", ".join(data["meanings"]) or "None",
            inline=False
        )

        await interaction.response.send_message(embed=embed)

    except Exception as e:
        await interaction.response.send_message(
            f"❌ Failed to fetch kanji.\n```{e}```",
            ephemeral=True
        )








#=======================================#




# run the bot with the specified token
bot.run(DISCORD_TOKEN, log_handler=handler, log_level=logging.DEBUG)

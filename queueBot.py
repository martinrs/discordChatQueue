import os

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.command(name='call', help='The equivalent of raising your hand. Optional: Type a question, topic or comment to help your teacher, e.g.: "!call Struggling with rocket science" or "!call None of you understand. I’m not locked up in here with you. You’re locked up in here with me!"')

async def call(ctx, content):
    pass

@bot.command(name='nvm', help='Never mind. The equivalent of lowering a raied hand')

async def nvm(ctx):
    pass

@bot command(name='next', help='Teachers only. Get the next question or comment in the queue')

async def next(ctx):
    pass

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

bot.run(token)

import os, json, discord.utils
from discord.ext import commands
from dotenv import load_dotenv

separator = '------------------------------------------------------------------'

bot = commands.Bot(command_prefix='!')

dataFile = 'queueData.json'
data = {'queue':[]}

def saveToJson(filename, jsonDict):
    try:
        file = open(filename, 'w')
        file.write(json.dumps(jsonDict))
        file.close()
    except Exception as e:
        print('Unable to write data to file because: {}'.format(e))
        raise

def loadFromJson(filename):
    content = None
    try:
        file = open(filename, 'r')
        content = json.loads(file.read())
        file.close()
    except Exception as e:
        print('Unable to read data because: {} ({})'.format(e, type(e).__name__))
        content = {}
        raise
    return content

def printQueue():
    global separator
    print(separator)
    if len(data['queue']) > 0:
        for i in range(len(data['queue'])):
            call = data['queue'][i]
            print(i, call['server'], call['name'], call['message'])
    else:
        print('Queue empty')
    print(separator)

def addToQueue(caller, server, message):
    data['queue'].append({'name': caller.name, 'server': server.name, 'message': message})

def saveState():
    saveToJson(dataFile, data)
    printQueue()

def isQueued(caller):
    for call in data['queue']:
        if caller.name == call['name']:
            return True
    return False

@bot.command(name='call', help='The equivalent of raising your hand. Optional: Type a question, topic or comment to help your teacher, e.g.: "!call Struggling with rocket science" or "!call None of you understand. I’m not locked up in here with you. You’re locked up in here with me!"')
async def call(ctx, message=''):
    if isQueued(ctx.author):
        await ctx.send('You are already queueing. Patience please.')
    elif ctx.valid:
        addToQueue(ctx.author, ctx.guild, message)
        if len(data['queue']) > 1:
            await ctx.send('Noted {}. {} queueing in front of you.'.format(ctx.author, len(data['queue'])-1))
        else:
            await ctx.send('Noted. {} is next up.'.format(ctx.author))
        await ctx.guild.owner.send('{} calls in queue'.format(len(data['queue'])))
        saveState()
    else:
        print('Something went wrong in call()')

@bot.command(name='nvm', help='Never mind. The equivalent of lowering a raied hand')
async def nvm(ctx):
    for i in range(len(data['queue'])):
        if data['queue'][i]['name'] == ctx.author:
            data['queue'].pop(i)
            ctx.send('{} removed from queue'.format(ctx.author))

@bot.command(name='next', help='Teachers only. Get the next question or comment in the queue.')
async def next(ctx):
    if len(data['queue']) > 0 and ctx.author == ctx.guild.owner:
        call = data['queue'][0]
        caller = discord.utils.get(ctx.guild.members, name=call['name'])
        await ctx.send('Next up: {}'.format(call['name']))
        await ctx.guild.owner.send('Next up: {} {} {}'.format(call['server'], call['name'], call['message']))
        await caller.send('You are up!')
        data['queue'].pop(0)
    await ctx.send('{} queueing'.format(len(data['queue'])))
    saveState()

@bot.command(name='clear', help='Teachers only. Clears the queue.')
async def clear(ctx):
    data['queue'] = []
    saveState()

@bot.event
async def on_ready():
    global separator
    print('\n{} online in:'.format(bot.user.name))
    for guild in bot.guilds:
        print(guild.name)
        guild.text_channels[0].send('Qbot is online for your queueing pleasure')
    print('\n')
    printQueue()

@bot.event
async def on_member_join(member):
    await member.send("Hi! I'm Qbot. I help {} keep track of whose turn it is.\nI know these commands:\n!call\n!nvm\n!next")

def main():
    global data
    print('Setting up')
    load_dotenv()
    print('\nLoading data')
    try:
        data = loadFromJson(dataFile)
    except FileNotFoundError:
        print('No saved data found. Creating data file.')
        saveToJson(dataFile, data)

    print('\nRunning bot.\nAdd the bot to servers with this link:\n{}'.format(os.getenv('BOT_LINK')))
    bot.run(os.getenv('DISCORD_TOKEN'))

main()

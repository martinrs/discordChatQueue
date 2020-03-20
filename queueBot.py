import os, json, discord.utils, pprint
from discord.ext import commands
from dotenv import load_dotenv

separator = '------------------------------------------------------------------'

bot = commands.Bot(command_prefix='!')

dataFile = 'queueData.json'
data = {}

def saveToJson(filename, jsonDict):
    if not os.path.exists('./data'):
        os.mkdir('./data')
    try:
        file = open('./data/{}.json'.format(filename), 'w')
        file.write(json.dumps(jsonDict))
        file.close()
    except Exception as e:
        print('Unable to write data to file because: {}'.format(e))
        raise

def loadFromJson(filename):
    content = None
    try:
        file = open('./data/{}.json'.format(filename), 'r')
        content = json.loads(file.read())
        file.close()
    except Exception as e:
        print('Unable to read data because: {} ({})'.format(e, type(e).__name__))
        content = {}
        raise
    return content

async def printQueue(ctx):
    global separator
    print(separator)
    if len(data[ctx.guild.id]['queue']) > 0:
        queuestring = ''
        print('{}\n'.format(ctx.guild.name))
        for i in range(len(data[ctx.guild.id]['queue'])):
            call = data[ctx.guild.id]['queue'][i]
            callername = discord.utils.get(ctx.guild.members, id=call['id']).display_name
            print(i, callername, call['message'])
            queuestring += '{}:\t{}\n'.format(i, callername)
        await ctx.send(queuestring)
    else:
        print('Queue empty')
    print(separator)

def addToQueue(caller, server, message):
    data[server.id]['queue'].append({'id': caller.id, 'server': server.name, 'message': message})

async def saveState(ctx):
    saveToJson(ctx.guild.id, data[ctx.guild.id])
    await printQueue(ctx)

def isQueued(caller):
    for call in data[caller.guild.id]['queue']:
        if caller.id == call['id']:
            return True
    return False

@bot.command(name='call', help='The equivalent of raising your hand. Optional: Type a question, topic or comment to help your teacher, e.g.: "!call Struggling with rocket science" or "!call None of you understand. I’m not locked up in here with you. You’re locked up in here with me!"')
async def call(ctx, message=''):
    if isQueued(ctx.author):
        await ctx.send('You are already queueing. Patience please.')
    else:
        addToQueue(ctx.author, ctx.guild, message)
        if len(data[ctx.guild.id]['queue']) > 1:
            await ctx.send('Noted {}. {} queueing in front of you.'.format(ctx.author.display_name, len(data[ctx.guild.id]['queue'])-1))
        else:
            await ctx.send('Noted. {} is next up.'.format(ctx.author.display_name))
        await ctx.send('{} in queue for you {}'.format(len(data[ctx.guild.id]['queue']), guild.owner.mention))
        await saveState(ctx)

@bot.command(name='nvm', help='Never mind. The equivalent of lowering a raied hand')
async def nvm(ctx):
    for i in range(len(data[ctx.guild.id]['queue'])):
        if data[ctx.guild.id]['queue'][i]['id'] == ctx.author.id:
            data[ctx.guild.id]['queue'].pop(i)
            ctx.send('{} removed from queue'.format(ctx.author.display_name))

@bot.command(name='next', help='Teachers only. Get the next question or comment in the queue.')
async def next(ctx):
    if len(data[ctx.guild.id]['queue']) > 0 and ctx.author == ctx.guild.owner:
        call = data[ctx.guild.id]['queue'][0]
        caller = discord.utils.get(ctx.guild.members, id=call['id'])
        await ctx.send('You are up {}!'.format(caller.mention))
        await ctx.guild.owner.send('Next up: {} {}'.format(caller.display_name, call['message']))
        data[ctx.guild.id]['queue'].pop(0)
        await saveState(ctx)
        #if caller.voice.channel:
        #    await ctx.guild.owner.move_to(caller.voice.channel)
        #https://discordpy.readthedocs.io/en/latest/api.html?highlight=move%20member#discord.Member.move_to
    await ctx.send('{} queueing'.format(len(data[ctx.guild.id]['queue'])))

@bot.command(name='clear', help='Teachers only. Clears the queue.')
async def clear(ctx):
    if ctx.author == ctx.guild.owner:
        data[ctx.guild.id]['queue'] = []
        await saveState(ctx)

@bot.event
async def on_ready():
    global separator, data
    for guild in bot.guilds:
        print('\n{} online in {}:'.format(bot.user.name, guild.name))
        print('Loading data')
        try:
            data[guild.id] = loadFromJson(guild.id)
        except FileNotFoundError:
            print('No saved data found. Creating data file.')
            data[guild.id] = {'serverID':guild.id, 'servername':guild.name, 'queue':[]}
            saveToJson(guild.id, data[guild.id])
        for channel in guild.text_channels:
            print(channel.name)
            #await channel.send('Qbot is online for your queueing pleasure')
    pprint.pprint(data)

@bot.event
async def on_member_join(member):
    await member.send("Hi! I'm Qbot. I help {} keep track of whose turn it is.\nI know these commands:\n!call\n!nvm\n!next")

def main():
    global data
    print('Setting up')
    load_dotenv()
    print('\nRunning bot.\nAdd the bot to servers with this link:\n{}'.format(os.getenv('BOT_LINK')))
    bot.run(os.getenv('DISCORD_TOKEN'))

main()

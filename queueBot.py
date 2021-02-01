import os, sys, json, discord.utils, datetime, socket, time
from discord.ext import commands
from discord.permissions import Permissions
from discord.colour import Colour
from dotenv import load_dotenv

separator = '------------------------------------------------------------------'
print('Using discord.py verison: {}'.format(discord.__version__))
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

data = {}

def makeFileName(guild):
    return '{}.{}'.format(guild.name, guild.id)

def saveToJson(guild, jsonDict):
    if not os.path.exists('./data'):
        os.mkdir('./data')
    try:
        filename = makeFileName(guild)
        file = open('./data/{}.json'.format(filename), 'w')
        file.write(json.dumps(jsonDict))
        file.close()
    except Exception as e:
        print('Unable to write data to file because: {}'.format(e))
        raise

def loadFromJson(guild):
    content = None
    try:
        filename = makeFileName(guild)
        file = open('./data/{}.json'.format(filename), 'r')
        content = json.loads(file.read())
        file.close()
        if not 'config' in content.keys():
            content['config'] = {'autofollow': True}
    except Exception as e:
        print('Unable to read data because: {} ({})'.format(e, type(e).__name__))
        content = {}
        raise
    return content

def printQueue(ctx):
    global separator
    print(separator)
    print(ctx.guild.name)
    print(makeQueueString(ctx))
    print(separator)

def addToQueue(caller, server, message):
    data[server.id]['queue'].append({'id': caller.id, 'server': server.name, 'message': message})

async def saveState(ctx):
    saveToJson(ctx.guild, data[ctx.guild.id])
    printQueue(ctx)

def isQueued(caller):
    for call in data[caller.guild.id]['queue']:
        if caller.id == call['id']:
            return True
    return False

def hasRole(member, roleName):
    if member.guild.owner == member:
        return True
    for role in member.roles:
        if role.name == roleName:
            return true
    return False

def queueManagerPresent(guild):
    for member in guild.members:
        if member.status == discord.Status.online and member.voice and hasRole(member, 'Queue Manager'):
            return True
    return False

def makeQueueString(ctx):
    queuestring = 'Queue is empty'
    if len(data[ctx.guild.id]['queue']) > 0:
        queuestring = ''
        for i in range(len(data[ctx.guild.id]['queue'])):
            call = data[ctx.guild.id]['queue'][i]
            callername = discord.utils.get(ctx.guild.members, id=call['id']).display_name
            queuestring += '{}:\t{}\n'.format(i, callername)
    return queuestring

def makeQueueManagerString(ctx):
    qmlist = list(filter(lambda m: hasRole(m, 'Queue Manager') and m.status == discord.Status.online, ctx.guild.members))
    if bot.user in qmlist:
        qmlist.remove(bot.user)
    out = ''
    if len(qmlist) >= 1:
        out += qmlist[0].mention
    if len(qmlist) >= 2:
        for i in range(1, len(qmlist)):
            if i == len(qmlist)-1:
                out += ' & {}'.format(qmlist[i].mention)
            else:
                out += ', {}'.format(qmlist[i].mention)
    return out

@bot.command(name='call', help='The equivalent of raising your hand. Optional: Type a question, topic or comment to help your teacher, e.g.: "!call Struggling with rocket science" or "!call I have information regarding item two on the agenda"')
async def call(ctx, *message):
    if isQueued(ctx.author):
        await ctx.send('You are already queueing. Patience please.')
    else:
        if message != None:
            message = ' '.join(message)
        addToQueue(ctx.author, ctx.guild, message)
        if len(data[ctx.guild.id]['queue']) > 1:
            await ctx.send('Noted {}. {} queueing in front of you.\n{} in queue for you {}'.format(ctx.author.display_name, len(data[ctx.guild.id]['queue'])-1, len(data[ctx.guild.id]['queue']), ctx.guild.owner.mention, len(data[ctx.guild.id]['queue']), makeQueueManagerString(ctx)))
        else:
            await ctx.send('Noted. {} is next up.\n{} in queue for you {}'.format(ctx.author.display_name, len(data[ctx.guild.id]['queue']), makeQueueManagerString(ctx)))
        await saveState(ctx)

@bot.command(name='nvm', help='Never mind. The equivalent of lowering a raised hand')
async def nvm(ctx):
    for i in range(len(data[ctx.guild.id]['queue'])):
        if data[ctx.guild.id]['queue'][i]['id'] == ctx.author.id:
            data[ctx.guild.id]['queue'].pop(i)
            await ctx.send('{} removed from queue'.format(ctx.author.display_name))
        await saveState(ctx)

@bot.command(name='next', help='See the current queue. Server owner advances the queue as well.')
async def next(ctx):
    global data
    mentionString = ''
    if len(data[ctx.guild.id]['queue']) > 0 and hasRole(ctx.author, 'Queue Manager'):
        call = data[ctx.guild.id]['queue'][0]
        caller = discord.utils.get(ctx.guild.members, id=call['id'])
        data[ctx.guild.id]['queue'].pop(0)
        mentionString = 'You are up {}!'.format(caller.mention)
        if call['message'] != '':
            await ctx.author.send('Message from {}: {}'.format(caller.display_name, call['message']))
        await saveState(ctx)
        if caller.voice and ctx.author.voice:
            if caller.voice.channel and ctx.author.voice.channel and data[ctx.guild.id]['config']['autofollow']:
                await ctx.author.move_to(caller.voice.channel)
    await ctx.send('{}\n{}'.format(mentionString, makeQueueString(ctx)))

@bot.command(name='clear', help='Queue Managers only. Clears the queue.')
async def clear(ctx):
    if ctx.author == ctx.guild.owner:
        data[ctx.guild.id]['queue'] = []
        await ctx.send('Queue is empty')
        await saveState(ctx)

@bot.command(name='config', help='Queue Managers only. Updates the chosen setting to the supplied configuration. The following settings are available:\nautofollow (True/False)\nChannel owner moved to callers voice chat on !next command if set to True')
async def config(ctx, *args):
    if hasRole(ctx.author, 'Queue Manager') and len(args) == 2:
        if args[0].lower() in data[ctx.guild.id]['config'].keys() and args[1].capitalize() in ('True', 'False'):
            data[ctx.guild.id]['config'][args[0].lower()] = eval(args[1].capitalize())
            await ctx.send('{} is now set to {}'.format(args[0].capitalize(), data[ctx.guild.id]['config'][args[0]]))
            await saveState(ctx)
        else:
            await ctx.send('Invalid config command. Use "!help config" for instructions.')
    else:
        ctx.send('You do not have permission to configure me.')

@bot.command(name='plenum', help='Queue Managers only. Moves every member of the server, who is connected to a voice channel, into the current voice channel of the server owner after a 10 second delay. Specify another delay using e.g. "!plenum 30" for a 30 second delay.')
async def plenum(ctx, delay=10):
    if hasRole(ctx.author, 'Queue Manager'):
        await ctx.send('Moving @everyone to plenum in {} seconds'.format(delay))
        delta = datetime.timedelta(seconds=delay)
        await discord.utils.sleep_until(datetime.datetime.utcnow() + delta, result='Time to meet')
        for member in ctx.guild.members:
            if member.voice:
                await member.move_to(ctx.author.voice.channel)

@bot.command(name='specs')
async def specs(ctx):
    await ctx.send('Python version: {}\ndiscord.py verison: {}'.format(sys.version, discord.__version__))

@bot.command(name='mute', help='Queue Managers only. Mutes all non-Queue Managers in the same voice channel as the Queue Manager who issued the command.')
async def mute(ctx):
    if ctx.author.voice and hasRole(ctx.author, 'Queue Manager'):
        await ctx.send('{} says: Quiet please'.format(ctx.author.display_name))
        for member in ctx.guild.members:
            if member.voice:
                if member.voice.channel == ctx.author.voice.channel and not hasRole(member, 'Queue Manager'):
                    await member.edit(mute=True)

@bot.command(name='unmute', help='Queue Managers only. Mutes all non-Queue Managers in the same voice channel as the Queue Manager who issued the command.')
async def unmute(ctx):
        if ctx.author.voice and hasRole(ctx.author, 'Queue Manager'):
            await ctx.send('{} says: You may speak'.format(ctx.author.display_name))
            for member in ctx.guild.members:
                if member.voice:
                    if member.voice.channel == ctx.author.voice.channel and not hasRole(member, 'Queue Manager'):
                        await member.edit(mute=False)

@bot.event
async def on_ready():
    global separator, data
    for guild in bot.guilds:
        await on_guild_join(guild)
    print('\nBot ready')

@bot.event
async def on_guild_join(guild):
    global separator, data
    QMrole = discord.utils.find(lambda r: r.name == 'Queue Manager', guild.roles)
    if not QMrole:
        QMrole = await guild.create_role(name='Queue Manager', permissions=Permissions(285346816), colour=Colour.dark_green(), hoist=True)
    try:
        await guild.owner.add_roles(QMrole)
    except discord.errors.Forbidden:
        print('Bot does not have "Manage Role" Permissions')

    print('\n{} online in {} (id: {}):'.format(bot.user.name, guild.name, guild.id))
    print('Loading data')
    try:
        data[guild.id] = loadFromJson(guild)
    except FileNotFoundError:
        print('No saved data found. Creating data file.')
        data[guild.id] = {'serverID':guild.id, 'servername':guild.name, 'queue':[], 'config': {'autofollow': True}}
    saveToJson(guild, data[guild.id])
    for channel in guild.text_channels:
        #print(channel.name)
        if queueManagerPresent(guild):
            await channel.send('{} is online for your queueing pleasure'.format(bot.user.display_name))

@bot.event
async def on_member_join(member):
    await member.send("Hi! I'm {}. I help keep track of whose turn it is.\nI know these commands:\n!call\n!nvm\n!next\n\nUse '!help to learn more.'".format(bot.user.display_name))

def main():
    global data
    print('Setting up')
    load_dotenv()
    print('\nRunning bot.\nAdd the bot to servers with this link:\n{}'.format(os.getenv('BOT_LINK')))
    bot.run(os.getenv('DISCORD_TOKEN'))

def internetIsAvailable():
    try:
        socket.create_connection(('1.1.1.1', 53))
        return True
    except:
        return False

while True:
    if internetIsAvailable():
        print('Internet Connection Available.\nStarting Bot.')
        break
    else:
        print('Connection not available.\nRetrying in 10 seconds.')
        time.sleep(10)
main()

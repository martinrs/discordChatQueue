# discordQueueBot

This is a lightweight queueing system for managing questions and discussions when teaching or meeting through Discord. The bot lets members of a Discord guild/server queue for something and enables the owner of the guild/server keep track of the queue and configure the bot's behavior.

The project was born out of a need to help teach high schoolers during the Covid-19 pandemic.

## Getting Started

To run the bot, you need to do these relatively simple steps:
1. Download code
1. Configure stuff
2. Install stuff
3. Install more stuff
1. Run bot
4. Use bot

Everything is described in detail below.

### Download the project

Simply download the project (the green button above) and unzip it in a folder of your choice.

If you know git, use git :)

### Setting up the bot application

Once you have cloned or downloaded the project, you will need to create a file in the same directory named `.env`. The file contents must be the following:
```
# .env Testbot
DISCORD_TOKEN=Your bot token goes here
BOT_LINK=Your bot link goes here
```

To complete this step we need to go to the [Discord Developer Portal](https://discordapp.com/developers/applications/) and:
1. Make a new application and name it (only you will see this name)
2. Go to **Bot** in the menu
3. Make a new bot and name it (this will be the default name when connected)
4. Copy the bot token to `DISCORD_TOKEN=` in the `.env` file
5. Go to **OAuth2** in the menu
6. Configure the bot scope to bot
7. Give the bot the following permissions
    - View Channels
    - Send Messages
    - Mention Everyone
    - Move Members
8. Copy the resulting bot link to `BOT_LINK=` in the `.env` file
9. Save and close

### Python

This bot is powered by [Python 3.6.4](https://www.python.org/downloads/) or newer. It should work with the latest version for your OS.

### Required libraries

The bot requires the following three libraries to run.

#### Install discord library
Install the library using pip. Usually like below.
```
pip install discord.py
```
Detailed instructions are found [here](https://pypi.org/project/discord.py/) if you encounter problems.

#### Install dotenv library
Install the library using pip. Usually like below.
```
pip install python-dotenv
```
Detailed instructions are found [here](https://pypi.org/project/python-dotenv/) if you encounter problems.

#### Install pprint library
Install the library using pip. Usually like below.
```
pip install pprint
```
There are no detailed instructions for this library, but you should have the hang of this now.

## Running the bot

Simply run `queueBot.py`. Run by executing the file via double click or via Command Prompt (windows) or terminal on Mac or Linux.

```
python queueBot.py
```

If the bot does not run, one or more steps from above was not performed correctly. Go back and try again please.

## Using the bot

First, the bot must be a member of the server, you want to use it on. Use the `BOT_LINK` from the `.env` file and follow the instructions on the screen. The bot can handle being a member of multiple servers.

By default the owner of the server will be given the role of **Queue Manager** and privileges to manage the queue (see commands below). The server owner (and anybody else with the **Queue Manager** role) has privileges to assign the role to others.

The bot responds to the following commands in any text channel on a server it is a member of. They are:
Command | Function
------------ | -------------
`!call` | The equivalent of raising your hand. Optional: Type a question, topic or comment to help your teacher, e.g.: "!call Struggling with rocket science" or "!call I have information regarding item two on the agenda".
`!nvm` | Never mind. The equivalent of lowering a raised hand.
`!next` | See the current queue. Queue Managers advances the queue as well.
`!plenum` | Queue Managers only. Moves every member of the server, who is connected to a voice channel, into the current voice channel of the server owner after a 10 second delay. Specify another delay using e.g. "!plenum 30" for a 30 second delay.
`!clear` | Queue Managers only. Clears the queue.
`!config` | Queue Managers only. Updates the chosen setting to the supplied configuration.
The following settings are available: autofollow (True/False)
Queue Managers moved to callers voice chat on !next command if set to True.

As stated in the introduction, the owner of the guild/server is the only one with full privileges to use `!next` and `!clear`.

## Roadmap

The following features are planned and prioritized as listed
1. Mute and Unmute all other members than owner (and possibly other exempted roles)

If you have suggestions for new features, please request it as an [issue](https://github.com/martinrs/discordQueueBot/issues).

## Contributing

If you want to help improve this tool, please get in touch!

## Authors

This bot was developed hastily by Martin Sørensen [@martinrs](https://github.com/martinrs)

## License

This project is licensed under Creative Commons Zero v1.0 Universal - see the [LICENSE](LICENSE) file for details

## Acknowledgments
Big up to my patient students for tolerating the quirks and bugs during the hasty development.

Shoutout to **Billie Thompson** [@PurpleBooth](https://github.com/PurpleBooth) for making the [template](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2) that this readme is based on.

# discordQueueBot

This is a lightweight queueing system for managing questions and discussions when teaching or meeting through Discord. The bot lets members of a Discord guild/server queue for something and enables the owner of the guild/server keep track of the queue.

The project was born out of a need to help teach high schoolers during the Covid-19 pandemic.

## Getting Started

To run the bot, you need to do these relatively simple steps:
1. Configure stuff
2. Install stuff
3. Install more stuff
4. Use bot

Everything is described in detail below.

### Setting up the bot application

Once you have cloned or downloaded the project, you will need to create a file in the same directory named '.env'. The file contents must be the following:
```
# .env Testbot
DISCORD_TOKEN=Your bot token goes here
BOT_LINK=Your bot link goes here
```

To complete this step we need to go to the [Discord Developer Portal](https://discordapp.com/developers/applications/) and:
1. Make a new application and name it (only you will see this name)
2. Go to 'Bot' in the menu
3. Make a new bot and name it (this will be the default name when connected)
4. Copy the bot token to 'DISCORD_TOKEN' in the '.env' file
5. Go to 'OAuth2' in the menu
6. Configure the bot scope to bot
7. Give the bot the following permissions
    - View Channels
    - Send Messages
    - Mention Everyone
    - Move Members
8. Copy the resulting bot link to BOT_LINK' in the '.env' file
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

Simply run 'queueBot.py'. Run by executing the file via double click or via Command Prompt (windows) or terminal on Mac or Linux.

```
python queueBot.py
```

If the bot does not run, one or more steps from above was not performed correctly. Go back and try again please.

## Using the bot

The bot responds to four commands in any text channel on a server it is a member of. They are:
Command | Function
------------ | -------------
'!call' | The equivalent of raising your hand. Optional: Type a question, topic or comment to help your teacher, e.g.: "!call Struggling with rocket science" or "!call I have information regarding item two on the agenda".
'!nvm' | Never mind. The equivalent of lowering a raied hand.
'!next' | See the current queue. Channel owner advances the queue as well.
'!clear' | Channel owner only. Clears the queue.

As stated in the introduction, the owner of the guild/server is the only one with priveleges to use '!next' and '!clear'.

## Roadmap

The following features are planned and prioritized as listed
1. Move channel owner to callers voice channel when owner uses '!next'
2. Move all members to channel owner's voice chat on command '!plenum' with optional time delay parameter

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

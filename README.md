
# DeepThonk: A Python bot for Twitch

An open-source Python bot framework for Twitch - *currently in development*. In it's current version, it's a rewrite of the "OG" version we build on-stream in 2018. Some features are missing until we can port them over to the rewrite.

Deepthonk was [Live Coded on Twitch](http://bit.ly/nb9kTwitch), with the help of an amazing community!

## Feature Overview

### In Production
- A simple call & response command system
- Text-to-speech (TTS) system
- SFX/hooks commands system (using browser source in OBS)
- Shoutouts to subscribers & team members (chat & tts)
- Basic event reactions (raids)

### In Development
- Random sound effects based on trigger words in chat
- OBS scene & source control (done but not ported)
- Philips HUE integration (done but not ported)

## Integrations
<!-- elaborate on these later.. -->
- Twitch IRC chat & API
- Streamlabs alerts _(partial functionality, still working on remaining alerts)_

## App Organization & Structure

<!-- DIRSTRUCTURE_START_MARKER -->
<pre>
deepthonk/
├─ bot/ ..................... App that integrates with Twitch chat
│  ├─ commands.py ........... Chat commands live here
│  ├─ content.py ............ (moving to JSON soon)
│  ├─ debug-example.py ...... Rename to debug.py for command testing
│  ├─ deepthonk.py .......... Starts the chat bot
│  ├─ events.py ............. Handles chat & bot events
│  ├─ server_interface.py ... Interfaces with API/WS server
│  ├─ config/ ............... Imports secrets from env vars
│  ├─ integrations/
│  │  ├─ streamlabs/ ........ WS wrapper
│  │  └─ twitch/ ............ API wrapper
│  ├─ utils/ ................ Logger, etc
│  └─ .env-example/ .......... Rename to .env & add secrets
└─ server/ .................. App that creates a local API/WS server for the bot
   ├─ conf.py ............... Imports secrets
   ├─ server.py ............. Starts the local server
   ├─ sfx.py ................ Generates sfx commands from files
   ├─ static/
   │  ├─ sfx/
   │  │  ├─ hooks/ .......... Put SFX files here!
   │  │  └─ other/ ..........
   │  │     ├─ raid.mp3 ..... Plays when a raid occurs
   │  │     └─ chirp.mp3 .... Plays before tts messages
   ├─ templates/
   │  ├─ home.html
   │  └─ obs-source.html .... Browser source html template
   ├─ utils/ ................ Logger, etc.
   └─ .env-example/ .......... Rename to .env & add secrets
</pre>
<!-- DIRSTRUCTURE_END_MARKER -->

## Configure the bot

To run the bot, you need to run both the local server and the bot application simultaniously. The bot app handles integration with the chat, and the server handles generating the OBS Browser Source for the sound effects and other critical functionality.


### Prerequisites
- Python 3.6 or 3.7 -- [Windows](https://www.python.org/downloads/release/python-375/) // [Linux](https://www.python.org/downloads/release/python-375/) // [OS X](https://www.python.org/downloads/release/python-375/)
- PIPENV ->`pip install pipenv` or `python -m pip install pipenv` (sometimes python3)
- An `oauth token` & `client-id` for a Twitch account for your bot
  - This [Twitch Bot Tutorial](https://dev.to/ninjabunny9000/let-s-make-a-twitch-bot-with-python-2nd8) I made on [dev.to](https://dev.to/ninjabunny9000) explains how to obtain your tokens and ID


### Create a cozy home for the bot to live in

Virtual environments require a couple extra steps to set up but make developing Python apps a breeze. I suggest using [PIPENV](https://github.com/pypa/pipenv) which marries pip and venv into a single package.

>You'll need to do the following steps for both the bot and the server directories

- In the console, navigate to your working directory
- Then run ⇒ `pipenv install`

**Repeat this for both `/bot/` and `/server/` directories**

## Adding secrets & settings

Rename the `.env-example` files to `.env` in the `/bot/` and `/server/` directories.

Your secrets will live inside these files and imported into the venv when you start the apps. Add the oauth token and client-id from above go after the `=` in the files. Fill in the other variables as well.

```bash
# /server/
SECRET_KEY= # make up your own key here
```

```bash
# /bot/
TWITCH_BOT_NICK=
TWITCH_TOKEN=oauth:
TWITCH_CLIENT_ID=
TWITCH_PREFIX=! # default is !
TWITCH_CHANNEL=
TWITCH_TEAM=
STREAMLABS_KEY=
BOT_SERVER_KEY=  # use key from /server/.env
```

## Booting up the bot

**Start the server:**
- Navigate to the server's working directory (`/server/`)
- In the console, run ⇒ `pipenv run python server.py`

**Start the bot:**
- Navigate to the server's working directory (`/bot/`)
- In the console, run ⇒ `pipenv run python deepthonk.py`

Once the bot goes online, it should greet you in both console and the configured channel's chat.

![i'm back baby](https://i.imgur.com/vBDGlOT.png)

### Test command

The bot comes pre-loaded with a `!test` command, if you want to try it in chat.

![test passed!](https://i.imgur.com/Y9pEHZs.png)

## Adding custom commands

Create new commands at the top of `commands.py`. Any command you make needs to follow this format when defining them..

- Decorated with `@bot.command(name='whatever')`
- Be asynchronous functions with names that match the `name` variable in the decorator
- Pass the message context in through the function

How the function works and what it does is all up to you. For this example, we'll create a command called `!test` that says `test passed!` in chat when we call it.

```python
# bot.py, below event_message function
@bot.command(name='test')
async def test(ctx):
    await ctx.send('test passed!')
``` 

One key ingredient to making any command work is for them to be handled in the `event_message` function. If you accidently delete the following line, and commands don't work anymore, that's what's up.


```python
# events.py, inside event_message
await bot.handle_commands(ctx)
```

## Adding SFX

Place SFX inside `server/static/hooks/`.

Mp3s, WAVs, and Ogg files inside that folder are loaded as sfx commands when the server starts.

### Setting up in OBS

Inside OBS, create a new browser source with the url of `http://localhost:6969/obs-source/`. You should be able to hear sfx now.

If you make any changes to the server and add or remove SFX, you'll need to refresh the browser source's cache.


## Events

There are 2 events that are used in the code right now.. `on_ready` and `on_event`.

### on_ready
This executes when the bot comes online, and will print out to the console.
```python
@bot.event
async def event_ready():
    print(f'Ready | {bot.nick}')
```

### event_message
This function executes once per event (or message) sent. You can make it handle input from chat that *aren't* necesarily commands, and fun stuff like that.

```python
@bot.event
async def event_message(message):
    print(message.content)
    await bot.handle_commands(message)
```
You can find more info in [TwitchIO's official documentation](https://twitchio.readthedocs.io/en/rewrite/twitchio.html).


## Advanced topics

I'm working on a blog and tutorial series going over more advanced topics in Python Twitch bot building and the TwitchIO library on [dev.to](http://bit.ly/nb9kdevto)

[Let's make a Twitch bot with Python!](http://bit.ly/twitchbot101)


### Follow Along & Contribute!
Watch & help develop the bot during live streams on [Twitch](https://twitch.tv/ninjabunny9000)! PR's are welcome but you're encouraged to at least spend a little time on stream to get an idea about Deepthonk's "personality" and the direction we're taking the bot first.

If you have any questions or just wanna brainstorm some neat ideas, [live-streams](https://twitch.tv/ninjabunny9000) are the best time for that!


## Trouble-shooting

I'm still working on building out this section of the docs. If you have any questions or issues, you have a couple of options to get in touch with me...

- [Create an issue](https://github.com/NinjaBunny9000/DeepThonk/issues/new) in the repo (slow but well-documented)
- [Twitter](http://bit.ly/nb9kTwitter) (pretty fast)
- [Discord](https://discord.gg/UEUFAUV), in the `#dev` channel (faster)
- [Twitch Streams](http://bit.ly/nb9kTwitch), (schedule pinned on Twitter) (fastest)

## Contributors & Licenses

[NinjaBunny9000](https://github.com/NinjaBunny9000) - _Author, Project Manager_ - [Twitch](https://twitch.tv/ninjabunny9000) //  [Twitter](https://twitter.com/ninjabunny9000)

[![ko-fi](https://www.ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/Y8Y013678)

### Special Thanks
Literally everyone that's helped even the smallest bit during streams. Thank you so much, y'all!

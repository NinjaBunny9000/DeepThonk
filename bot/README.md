# DeepThonk

>**This README is a wip!**

Deepthonk is a Twitch chat bot, written in Python, that provides supplementary features such as sound effects, unique moderation tools, OBS scene & source **control**, Philips HUE integration, & stream-event reactions.

_** Now with added sass! **_

## Getting Started

Right now the Master branch only contains the basic template for starting a Twitch chat bot in Python, but some still might find it useful if they want to follow along. :D

### Prerequisites
- [Python 3.6](https://www.python.org/downloads/release/python-368/)
- PIPENV -> `python -m pip install pipenv`
- oauth token & client-id for a Twitch account for your bot

### Installing
1. Clone the repo, unzip it somewhere
2. Open up a console window and navigate to the directory you unzipped it in
3. Install requirements with `pipenv install`
4. Copy & rename `integrations-example.yaml` to `integrations.yaml`
5. Pop in all your secrets into the respective areas in `integrations.yaml`
6. Back to the console, `pipenv run python deepthonk.py` to start the bot
7. Type `!test` in the chatroom to test the bot's working

**You just installed a basic chat bot for Twitch!** Have fun expanding the bot with more commands!! :D

## Bot Interaction
We're still porting over functions from the rewrite, so this section will be fairly under-developed for a while. There will be functionality you see on stream that isn't part of this rewrite, but it will be soon - promise! Let Bun know if you have any questions about those.

### Getting Help
*help command documentation coming soon*


### Stream-event Reactions
In development, the bot's currently integrating with both streamelabs and streamelements for event reacts, altho streamlabs' websockets were better documented, so there's a bit more functionality with that service. These integrations will be ported over to the rewrite very soon.

#### Raid Battle [WIP]
Raids trigger a sequences of timed-responses from DeepThonk and challenges the raiding and defending "teams" to spam emotes in order to "deal damage" to the other team. Emotes drain "hp".

The raid game is still very much a work in progress and I'm very frequently working on & improving the RAID system during Twitch streams. It's definitely one of the more unique features of the bot.. But more of that soon!! :3 (it's a surprise.. sorta???)

### Sound Effects
To create and use sound effects in your stream, drop `.ogg` files into the `/hooks/` dir. Any `.ogg` files in this directory will be initialized as commands when you start the bot.

### Integrations
Deepthonk's integrates with Philips HUE, Strawpoll, & OBS (via websockets) in its' development branch. We're slowly porting those features over and updating the documentation as it happens. _Keep posted here for more info._

### Lists & Counters
_Coming soon!_


### Having a conversation with Deepthonk
_More info coming soon! eeeeeep!_


## Progress & Development Info

### The Master (release™) Branch
The master branch includes the latest functional(?) release of Deepthonk. Future features will be rolled into this branch once they're cleaned up and tested.

If you see a feature on stream that you'd love to see in the Master, mention it! It helps to know what features people are looking forward to next. ^_^

### Rewrite Branch
Current development branch is `rewrite`. Deepthonk was originally written around a twitch irc lib that was pretty jank, so we're rewriting it in a way that's more friendly for folks to follow along with, use themselves, or even contribute.

### Follow Along & Contribute!
Watch & help develop the bot during live streams on [Twitch](https://twitch.tv/ninjabunny9000)! PR's are welcome, but you're encouraged to at least spend a little time on stream to get an idea about Deepthonk's "personality" and the direction we're taking the bot, to make sure you're not providing features that clash with it (or worse, are already features in other prominant and readily-avilable bots - meaning you spent precious dev time on potentially redundant functionality).

If you have any questions or just wanna brainstorm some neat ideas, [live-streams](https://twitch.tv/ninjabunny9000) are the best time for that!

## Contributors & Licenses

[NinjaBunny9000](https://github.com/NinjaBunny9000) - _Author, Project Manager_ - [Twitch](https://twitch.tv/ninjabunny9000) //  [Twitter](https://twitter.com/ninjabunny9000)

### Special Thanks
Literally everyone that's helped even the smallest bit during streams. Thank you so much, y'all!
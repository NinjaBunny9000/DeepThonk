# DeepThonk

**README Coming Soon!!**  

A Python bot and web interface for Streamers using Discord, Twitch, & StreamElements. (Now with added sass!)


## Development Branch
Current development branch is `dev`. All feature branches extend from here.

## Bot Interaction
- getting help
- directly adressing the bot
- asking it a question
- yelling at it
- maybe it needs to take a nap

## Bot reactions & automation

- Raid game


## Commands

### Command Types

- Control
  - `stahp` or `!quit` Stops the bot.

- FAQ
  - `!theme` `!editor` `git` `toolset` `steam` `font` `branch` `repo` `kanban` `portfolio` `bmo`

- Dynamically generated responses
  - `!cah`
- Sound Effects
  - Basic SFX
  - Random SFX
  - LED/Light-Reactive SFX
- Quotes & Lists
  - Totally awesome band names
- Silly stuff & keywords
  - Sentient. sentient? sentient! sentient
  - Links (NSFW!)
  - `i have a question`
  - `oi`
  - `howdy`
  - `love me` `love you` `love u`
  - `guy` `buddy` `friend` circular argument
  - `say goodnight <deepthonk> `


!task
!randomtask
!cah
!hye
!reward
!shoutout


## Games

### RAIDs *[WIP]*

Raids trigger a sequences of timed-responses from DeepThonk and challenges the raiding and defending "teams" to spam emotes in order to "deal damage" to the other team. Emotes drain "hp".

None of this is displayed on screen right now, just in chat. Still very much a work in progress and I will be very frequently working on & improving the RAID system during Twitch streams.


### EarWorm Roulette *[WIP]*



## OBS Scene Control

Changing scenes in OBS works by writing the name of a scene to a file.. (`data/scene_next.txt` and OBS uses the plugin "Advanced Scene Switcher" to read from a file (`data/scene_current.txt`) to get the scene it should switch to.

You'll need to download and install the plugin, tick `Enable switching of scenes based on the file input` under the `Write To File / Read From File` tab in the plugin settings popup window. Point the fields above and below the tick-box to the proper files (listed above) then use any of the `obs<scene>` commands with the bot.

`obsscene` returns the current scene.

You can modify scene names in `obs_ctrl.py`. Scene names are case-sensitive.

## Response features

DeepThonk combines & randomly orders a lot of it's responses. For instance, if a message triggered multiple keyword responses, and any of them were random or static, it would compile the static and a random choice response in a list and then randomly order those responses in a single-message response.

## Integrations

So far, I've only been able to implement minimal integrations between just Twitch and StreamElements (since they are what I use the most of). Integrations will definitely get expanded after a refactor.


### Twitch

### StreamElements

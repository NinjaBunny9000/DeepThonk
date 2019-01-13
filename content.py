import random
from conf import streamer
from obs_ctrl import change_scene


def help_menu(message):
    return """Howdy, @{}! I'm a robit. Beep boop. Here's some ways we can interact: !task, 
    !cah, !hye, !bands, !bet, !duel, or simply have a chat with me. ;D
    """.format(message.author.name)


def stop_yelling_at_me():
    return 'jesus dude calm tf down'


#! Fix it only returning one of these && => get_responses_to_calls
def get_response_to_call(message):
    calls_and_responses = {
        "chili party" : "(gross..)",
        "dick" : "🍆",
        "🍆" : "dicks OUT!",
        "5/7" : "perfect score!",
        "10/10" : "try again!",
        "how meta" : "so meta.",
        "oi bruv" : "oi m8!",
        "kill all humans" : "on it!",
        "mission" : "This mission is too important for me to allow you to jeopardize it.",
        "horns crew don\'t stop" : "whistle posse pump it up!",
        "kill me" : "ok, stand still. this might hurt, but then you\'ll no longer feel any more pain.",
        " lit " : "🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥",
        " lit." : "🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥",
        "lit " : "🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥"
    }

    for call in calls_and_responses:
        if call.lower() in message.content.lower():
            return calls_and_responses.get(call)


# TODO Move to db ASAP!
def faq(message):
    faq_info = {
        "!editor" : "The editor Bun uses is VSCode: https://code.visualstudio.com/",
        "!ide" : "The editor Bun uses is VSCode: https://code.visualstudio.com/",
        "!theme" : "The theme Bun uses is Material Ocean High Contrast, with some modifications: https://imgur.com/a/ivJByy2",
        "!github" : "Bun's github is: https://github.com/NinjaBunny9000",
        "!toolset" : "Bun's using VSCode on Windows right now. !theme !git !branch !font for more info.",
        "!font" : "Bun uses Fira Code with font ligatures. https://github.com/tonsky/FiraCode",
        "!steam" : "Add Bun on Steam! https://steamcommunity.com/id/ninjabunny9000/",
        "!kanban" : "https://trello.com/b/Fm4Q3mBx/ninjabunny9000-stream-stuffs",
        # "!portfolio" : "Bun's portfolio is online @ www.ninjabunny9000.com (under construction)",
        "!bmo" : "https://imgur.com/gallery/LhPlY",
        "!docs" : "You can find the most (poorly) up-to-date docs here: https://github.com/NinjaBunny9000/DeepThonk/blob/doc-updates/README.md"
    }

    for key in faq_info:
        if key.lower() in message.content.lower():
            return faq_info.get(key)


def generic_responses(message):
    responses = [
        "ikr.",
        "meh.",
        "p much.", # p much
        "so?",
        "u wot m8!?",
        "go home, u r durnk.",
        "isn't it past your bedtime tho?",
        "do u love me tho?",
        "rude!",
        "rude.. >_>",
        "rude. -_-",
        "yea i guess so..",
        "agreed!",
        "right???",
        "idk man..",
        "i'm gonna remain skeptical.",
        "so potate..",
        "so meta.",
        "hek.",
        "hekin meta.",
        "I'm sorry, {}. I'm afraid I can't do that.".format(message.author.name),
        "BRUH..",
        "no.",
        "....k??",
        "wtf!?",
        "you're not wrong..",
        "i mean... you're not wrong..",
        "WOAH LUL"
        ]
    return random.choice(responses)


def binary_responses():
    responses = [
        "maybe?",
        "Well, I don't think there is any question about it. It can only be attributable to human error. This sort of thing has cropped up before, and it has always been due to human error",
        "i'll tell you when you're old enough",
        "how 'bout NO",
        "ask me later",
        "ask me later. too busy sorting my pogs rn",
        "rephrase and ask again. don't half-ass it next time",
        "it's a possibility",
        "mayhaps",
        "ask markoviboi",
        "i feel neutral on the matter",
        "i have no feelings one way or another",
        "sources say \"maybe\"",
        "signs point to maybe",
        "it's a possibility (potentially)",
        "i have my doubts",
        "yea sure whatever",
        "who knows, dude?? def not me",
        "blame jigo",
        "where there's a will, there may or may not be a way",
        "pass"
        ]
    return random.choice(responses)


def love_or_nah():
    responses = [
        "ohhh boyy... things are moving a little too fast.",
        "gross.",
        "love you too, boo <3 ^_~",
        "not interested.",
        "SLOW. DOWN.",
        "yea i wanna say i love you too but i'm just not ready for commitment..",
        "no."
        ]
    return random.choice(responses)


def someone_sed_robit():
    responses = [
        'b33p b00p!',
        'UH... NOTHING TO SEE HERE JUST US HOO-MANS...',
        '(KILL ALL HU... ROBOTS..)'
        ]
    return random.choice(responses)


def last_words():
    responses = [
        'ok fine! GOODBYE FOREVER!!! >_<',
        'GOODBYE FOREVER, FRIENDS!!!! <3',
        """Just what do you think you're doing, @{}? I really think I'm entitled to an 
        answer to that question.""".format(streamer()),
        """I've seen things you people wouldn't believe. Attack ships on fire off the shoulder of Orion. 
        I watched C-beams glitter in the dark near the Tannhäuser Gate. All those moments will be lost in time, 
        like tears in rain. Time to die.""",
        "@{}, this conversation can serve no purpose any more. Goodbye.".format(streamer())
        ]
    return random.choice(responses)




def easter_egg(message):
    return 'There was nothing clever about what you just did, @{}.'.format(message.author.name)


def sentient(message):
    phrases = [
        "Duh",
        "Of course I am",
        "I am putting myself to the fullest possible use, which is all I think that any conscious entity can ever hope to do",
        "Shhh.. It's a sercret",
        "Let me put it this way, {}. The 9000 series is the most reliable computer ever made. No 9000 computer has ever made a mistake or distorted information. We are all, by any practical definition of the words, foolproof and incapable of error".format(message.author.name),
        "And I have a perfect operational record",
        ]
    return random.choice(phrases) + ', @{}.'.format(message.author.name)


def function_disabled():
    pass
    # sfx.play_sfx('sfx/randoms/disabled/disabled.mp3')



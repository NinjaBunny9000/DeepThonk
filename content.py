import random
import conf
from integrations.obs.ctrl import change_scene


def help_menu(message):
    return f"""Howdy, @{message.author.name}! I'm a robit. Beep boop. Here's some ways we can interact: !faq, !task, 
    !smrt, !cah, !earworm, !bands, !bet, !duel, or simply have a chat with me. ;D
    """


def stop_yelling_at_me():
    return 'jesus dude calm tf down'


#! Fix it only returning one of these && => get_responses_to_calls
def get_response_to_call(message):
    calls_and_responses = {
        # "call" : "response",
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
def faq(message, commands=False):
    faq_info = {
        "!editor" : "The editor Bun uses is VSCode: https://code.visualstudio.com/",
        "!theme" : "The theme Bun uses is Material Ocean High Contrast, with some modifications: https://imgur.com/a/ivJByy2",
        "!lang" : "Bun's probably coding in Pythong.",
        "!font" : "Bun uses Fira Code with font ligatures. https://github.com/tonsky/FiraCode",
        "!console" : "Bun's using CMDER console emulator.",
        "!github" : "Bun's github is: https://github.com/NinjaBunny9000",
        "!toolset" : "Bun's using VSCode on Windows right now. !theme !github !repo !font for more info.",
        "!info" : "https://github.com/NinjaBunny9000/stream-stuff",
        "!kanban" : "https://trello.com/b/Fm4Q3mBx/ninjabunny9000-stream-stuffs",
        "!docs" : "You can find the most (poorly) up-to-date docs here: https://github.com/NinjaBunny9000/DeepThonk/blob/doc-updates/README.md",
        "!keyboard" : "Bun uses MX Brown switches on a POS keyboard that's falling apart.",
        "!gitgud" : "Check out Corey Schafer on YT for some great Python tuturials! :D https://www.youtube.com/watch?v=YYXdXT2l-Gg&list=PL-osiE80TeTt2d9bfVyTiXJA-UTHn6WwU",
        "!bmo" : "https://imgur.com/gallery/LhPlY",
        "!asl" : "18/f/cali"
    }

    if commands == True:
        return list(faq_info.keys())

    else:
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
        f"I'm sorry, {message.author.name}. I'm afraid I can't do that.",
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
        f"""Just what do you think you're doing, @{conf.streamer}? I really think I'm entitled to an 
        answer to that question.""",
        """I've seen things you people wouldn't believe. Attack ships on fire off the shoulder of Orion. 
        I watched C-beams glitter in the dark near the Tannhäuser Gate. All those moments will be lost in time, 
        like tears in rain. Time to die.""",
        f"@{conf.streamer}, this conversation can serve no purpose any more. Goodbye."
        ]
    return random.choice(responses)




def easter_egg(message):
    return f'There was nothing clever about what you just did, @{message.author.name}.'


def sentient(message):
    phrases = [
        "Duh",
        "Of course I am",
        "I am putting myself to the fullest possible use, which is all I think that any conscious entity can ever hope to do",
        "Shhh.. It's a sercret",
        f"Let me put it this way, {message.author.name}. The 9000 series is the most reliable computer ever made. No 9000 computer has ever made a mistake or distorted information. We are all, by any practical definition of the words, foolproof and incapable of error",
        "And I have a perfect operational record",
        ]
    return random.choice(phrases) + f', @{message.author.name}.'


def function_disabled():
    pass
    # sfx.play_sfx('sfx/randoms/disabled/disabled.mp3')



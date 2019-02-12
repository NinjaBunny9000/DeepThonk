import integrations.twitch.irc_wrapper
import conf
import os

'Import all the bot Modules'
# TODO may not need deez? importing via __init_.py's p sure...
import integrations
import lists
import games
import moderation
import sfx
import economy
if conf.debug:
    import debug


twitch_bot = conf.twitch_instance

def start_twitch():
    # pull in the config var for ze bot!
    print('Starting the Twitch bot...')
    twitch_bot.start()

def main():
    start_twitch()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nInterrupted via terminal. Shutting down...')
        twitch_bot.stop(exit=True)
        os._exit(0)   
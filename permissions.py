from conf import bot_list, streamer

def is_mod(message):
    if (message.author.mod or message.author.name.lower() == streamer().lower()):
        return True
    else:
        return False

 
def is_bot(message):
    if (message.author.name.lower() in str(bot_list).lower()):
        return True
    else:
        return False
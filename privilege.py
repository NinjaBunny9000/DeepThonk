import conf

def is_mod(message):
    if (message.author.mod or message.author.name.lower() == conf.streamer.lower()):
        return True
    else:
        return False

 
def is_bot(message):
    if (message.author.name.lower() in str(conf.bot_list).lower()):
        return True
    else:
        return False
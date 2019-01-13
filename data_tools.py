import random


# SECTION Parsy stuffs ™

def parse_commands(message, parts): 
    message_parts = message.content.split(' ', parts)
    return message_parts

def shuffle_msg(msg_list):
    """
    Takes a list of responses (if more than one) and shuffles them and combines them
    so that they can all be sent in one message. ex: Oi deepthonk! Do you like dicks?
    """
    random.shuffle(msg_list)
    return ' '.join(msg_list)


def tokenize(message, parts=0, lower_case=True):
    if lower_case:
        if parts == 0:
                return message.content.lower().split(' ') # TOKENIZE™
        else: 
                return message.content.lower().split(' ', parts) # TOKENIZE™
    else:
        if parts == 0:
            return message.content.split(' ') # TOKENIZE™
        else: 
            return message.content.split(' ', parts) # TOKENIZE™
                


def stringify_list(stupid_list, prefix_char=''):
    'Takes a list and concats into a string, separated by commas, with (or without) prefix arg.'
    addy_part = ', {}'.format(prefix_char)
    stringificated_listymajig =  '[%s]' % addy_part.join(map(str, stupid_list))
    stringificated_listymajig = stringificated_listymajig.strip('[]')
    stringificated_listymajig = prefix_char + stringificated_listymajig
    return stringificated_listymajig

# !SECTION 


# SECTION .txt File Operations

def check_for_duplicates():
    # TODO check for duplicates in string or list
    pass

def list_to_txt(file_path, file_name, listyboi):
    with open(file_path + file_name, 'w+') as f:
        for item in listyboi:
            f.write('{}\n'.format(item))


def txt_to_list(file_path, file_name):
    listyboi = list()
    with open(file_path + file_name, 'r+') as f:
        for line in f:
            listyboi.append(line)
    return listyboi
    

def add_to_txt(file_path, file_name, list_item:str, lower_case=True):
    with open(file_path + file_name, 'a') as f:
        if lower_case:
            f.write('{}\n'.format(list_item))
        else:
            f.write('{}\n'.format(list_item))
    


def score_to_txt(defense_hp, raider_hp):
    with open('data/raid_score.txt', 'w+') as f:
        msg = "RAIDERS : {}/500 hp   ||   DEFENDERS : {}/500 hp".format(raider_hp, defense_hp)
        f.write(msg)


def clear_txt(file_path, file_name):
    open(file_path + file_name, 'w').close()


def rem_from_txt(list_item:str):
    pass

# !SECTION 
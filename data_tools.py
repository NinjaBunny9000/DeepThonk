import random
import conf


# SECTION Parsy stuffs ™

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
    addy_part = f', {prefix_char}'
    stringificated_listymajig =  '[%s]' % addy_part.join(map(str, stupid_list))
    stringificated_listymajig = stringificated_listymajig.strip('[]')
    stringificated_listymajig = prefix_char + stringificated_listymajig
    return stringificated_listymajig


def ats_or_nah(user):
    if user.startswith('@'):
        return user[1:]
    else:
        return user

# !SECTION 


# SECTION .txt File Operations

def check_for_duplicates():
    # TODO check for duplicates in string or list
    pass


def list_to_txt(file_path, file_name, listyboi):
    with open(file_path + file_name, 'w+') as f:
        for item in listyboi:
            f.write(f'{item}\n')


def txt_to_list(file_path, file_name):
    listyboi = list()
    with open(file_path + file_name, 'r+') as f:
        for line in f:
            listyboi.append(line)
    return listyboi


def string_to_txt(file_path, file_name, stringyboi, lower_case=True):
    with open(file_path + file_name, 'w+') as f:
        f.write(f'{stringyboi}')
    

def txt_to_string(file_path, file_name):
    with open(file_path + file_name, 'r+') as f:
        stringyboi = f.read()
    return stringyboi


def add_to_txt(file_path, file_name, stringyboi:str, lower_case=True):
    with open(file_path + file_name, 'a') as f:
        if lower_case:
            f.write(f'{stringyboi}\n'.lower())
        else:
            f.write(f'{stringyboi}\n')
    

def score_to_txt(defense_hp, raider_hp):
    with open('data/raid_score.txt', 'w+') as f:
        home_team_name = conf.raid['home_team_name'].upper()
        away_team_name = conf.raid['away_team_name'].upper()
        max_hp = conf.raid['max_hp']
        msg = f"{away_team_name} : {raider_hp}/{max_hp} hp   ||   {home_team_name} : {defense_hp}/{max_hp} hp"
        f.write(msg)


def clear_txt(file_path, file_name):
    open(file_path + file_name, 'w').close()


def rem_from_txt(list_item:str):
    pass

# !SECTION 
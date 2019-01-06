
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
    

def add_to_txt(file_path, file_name, list_item:str):
    with open(file_path + file_name, 'a') as f:
        f.write('{}\n'.format(list_item))


def clear_txt(file_path, file_name):
    open(file_path + file_name, 'w').close()


def rem_from_txt(list_item:str):
    pass

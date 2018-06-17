import base64
import discord
import json
import os
import requests

#toggles '-' in given uuid
def convert_uuid(uuid):
    if '-' in uuid:
        return uuid.split('.json', 1)[0].translate({ ord(i): None for i in '-' })
    else:
        return uuid[:8] + '-' + uuid[8:12] + '-' + uuid[12:16] + '-' + uuid[16:20] + '-' + uuid[20:]

#returns the total size of all files in given location
def get_size(start_path):
    total_size = 0

    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    
    return total_size

#returns all names in the namehistory of a uuid without duplicates or the current name
def get_name_history(uuid):
    url = "https://api.mojang.com/user/profiles/" + uuid + "/names"

    response = requests.get(url)
    response.raise_for_status
    response = json.loads(response.text)
    
    current_name = response[-1]['name']
    
    del response[-1]
    
    if response != []:
        for name in response:
            if name['name'] == current_name:
                del response[response.index(name)]
    return response

def get_name_from_uuid(uuid):
    try:
        url = "https://sessionserver.mojang.com/session/minecraft/profile/" + uuid

        response = requests.get(url)
        response.raise_for_status
        response = json.loads(response.text)
        response = json.loads(base64.b64decode(response['properties'][0]['value']))

        return response['profileName']
    except: return None

def generate_embed_table(discord, columns_lines):
    em = discord.Embed(
        description = '',
        colour = 0x003763)

    for column in columns_lines:
        em.add_field(
            name = column,
            inline = True,
            value = '\n'.join(column_lines[column]))

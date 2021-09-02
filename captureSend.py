import requests
import sys
import discord
from discord.ext import commands
import json
import time
import asyncio
import random
import math
from rich.console import Console
# initialize the Console() class
console = Console()

class discordConnect:

    def __init__(self, token, client):
        self.token = token
        self.client_id = client
        self.headers = {'Authorization': token}

    def _get_channel_id(self, client_id):
        """ create message and return tokens list of messages """
        res = requests.post('https://discordapp.com/api/v9/users/@me/channels',
                            headers=self.headers, json={'recipient_id': self.client_id})
        return res.json().get('id')

    def execute(self, message):
        """ send message to client """
        channel_id = self._get_channel_id(self.client_id)
        return requests.post(f'https://discordapp.com/api/v9/channels/{channel_id}/messages', headers=self.headers, json={'content': message})

def websocketMessage(id, token):
        
    client_id = id

    sendComp = discordConnect(token, client_id)

    message = f"""Enter your formatted message here it should return exactly what you type..."""	


    sendComp.execute(message)
    

token = "TOKEN_HERE"

def log_id(id):
    with open("ids.json", "r") as file:
        data = json.load(file)

    if id not in data:
        data.append(id)
        websocketMessage(id, token)
        
        with open("ids.json", "w") as file:
            json.dump(data, file)

        print(" In Vicinty to Message:", id, " Total Users This Session:", len(data))
        time.sleep(random.randint(50, 62))

bot = commands.Bot(command_prefix='?')


@bot.event
async def on_ready():
    print(' [!] Started logging ids\n')
    
@bot.event
async def on_message(message):
    if not message.author.bot:
        log_id(message.author.id)

@bot.event
async def on_raw_reaction_add(payload):
    if not payload.member.bot:
        log_id(payload.member.id)

@bot.event
async def on_member_join(member):
    if not member.bot:
        log_id(member.id)

@bot.event
async def on_member_update(before, after):
    if not after.member.bot:
        log_id(after.member.id)

@bot.event
async def on_voice_state_update(member, before, after):
    if not member.bot:
        log_id(member.id)


bot.run(token, bot = False)

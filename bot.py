# A discord cross-guild chatbot

import discord
import aiohttp
import dotenv
import os
import re

dotenv.load_dotenv()
token = str(os.getenv("TOKEN"))

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Bot(intents = intents)

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

@bot.slash_command(name = "Hi", description = "Hi")
async def hello(self):
    await self.respond("Hey")
    print(self.author)

def loopholes(message):
    """
    Checking for infinite loops & mass pings
    """
    if (
        re.search("@everyone", message.content) or re.search("@here", message.content) or
         message.author.id == bot.user.id or isinstance(message.author, discord.Webhook)
         or re.search(".*#0000", str(message.author))
         ):
        return False
    else:
        return True

class stream_webhook_data:
    def __init__(self):
        self.webhook_dict = {
            
            # ---- to be improved ------

            # fill it with channel id and webhook links ... the bot sends msg to every link mentioned here ... ( --- to be improved ---)
            
            # ---- to be improved ------

            }   # {channel_id : webhook_link}        
    
    def fetch(self, message):
        if message.channel.id in self.webhook_dict:
            return True
        else:
            return False

    def fetch_link(self, message):
        """
        assuming the key-value pair exists
        """
        for key, value in self.webhook_dict.items():
            if key != message.channel.id:
                yield value

@bot.event
async def on_message(message):
    if loopholes(message):
        nexus = stream_webhook_data()       # super random name go brrrrr
        if nexus.fetch(message):
            async with aiohttp.ClientSession() as session:
                for webhook_link in nexus.fetch_link(message):
                    webhook = discord.Webhook.from_url(webhook_link, session = session)  
                    await webhook.send(f"{message.content}", username=f'[{message.guild.name}]  {message.author.name}', avatar_url=message.author.avatar)

bot.run(os.getenv("TOKEN"))
import logging
from time import sleep
import discord
import os
import creds
import search
from dotenv import load_dotenv
import asyncio
from discord.ext import tasks
from discord.ext import commands


# Use python-dotenv pakcage to get variables stored in .env file of your project
load_dotenv('.env.txt')
client = commands.Bot(command_prefix="$")

hello_message = '''@everyone Hello there! I\'m the fidgeting bot from RunPee. Sorry but I really need to go to the bathroom... 
Please read my manual by typing $help or $commands while I\'m away.'''

no_result_message = '''Sorry, we can\'t find what you are searching for. We may not have written anything about it yet, 
but you can subscribe to our news letter for updates of our newest content 
--> https://runpee.com/about-runpee/runpee-movie-newsletter/'''

# instantiate RunPeeWeb class from search_runpee.py
runpee_web = search.Driver()
contains = []
text_file = open("GemsEvents.txt", "r")
contains = text_file.read().split(',')
contain = []
for i in range(len(contains)):
  print(contains[i])
text_file.close()


@client.event
async def on_ready():
  print(f'{client.user} is now online!')


@client.event
async def on_message(message): 
  if message.author == client.user:
      return  
  # lower case message
  message_content = message.content.lower()  

  
  if message.content.startswith(f'$hello'):
    await message.channel.send(hello_message)
  
  if f'$search' in message_content:
    result_links = runpee_web.search()
    #links = runpee_web.send_link(result_links, search_words)
    
    if len(result_links) > 0:
      for link in result_links:
       await message.channel.send(link.text)
    else:
      await message.channel.send(no_result_message)

  if f'$available' in message_content:
    await message.channel.send("@everyone")
    unfill = runpee_web.get_unfilled()
    if(len(unfill)== len(contains)):
      return
    v = len(unfill) - len(contains)
    len2 = len(contains)
    print("Length: ",len2)
    for i in range(len2, len2 + v):
      await message.channel.send(unfill[i])
      contains.append(unfill[i])

@tasks.loop(seconds=20.0)
async def automate():
    await asyncio.sleep(10)
    channel = client.get_channel(895760475445428277) # replace with channel ID that you want to send to
    msg_sent = False
    #while True:
            #if not msg_sent:
    text = open("GemsEvents.txt", "w")
    unfill = runpee_web.get_unfilled()
    if(len(unfill)== len(contains)):
        return
    v = len(unfill) - len(contains)
    len2 = len(contains)
    print("Length: ",len2+v)
    for i in range(len2, len2 + v):
       await channel.send("@everyone")
       await channel.send(unfill[i])
       contains.append(unfill[i])
       text.write(unfill[i]+",")
    print("Message Sent")
    text.close()
    msg_sent = True
            #else:
              #msg_sent = False
  

automate.start()
client.run(creds.DISCORD_TOKEN)


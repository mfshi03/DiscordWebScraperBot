
@client.event
async def on_message(message): 
  # make sure bot doesn't respond to it's own messages to avoid infinite loop
  if message.author == client.user:
      return  
  # lower case message
  message_content = message.content.lower()  
  
  if message.content.startswith(f'$hello'):
    await message.channel.send('''Hello there! I\'m the fidgeting bot from RunPee. 
    Sorry but I really need to go to the bathroom... Please read my manual by typing $help or $commands while I'm away.''')
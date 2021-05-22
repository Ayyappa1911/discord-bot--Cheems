import discord as d
import os
import requests
import json
import random
from keep_alive import keep_alive
#from replit import db


class bot:
  def __init__(self):
    self.client = d.Client()
    self.sad_words = ["sad","depressed","angry","unhappy","depressing"]

    self.starter_encouragements = ["cheer up!" , "Hang in there.", "you are a great person /bot!" ]


    @self.client.event
    async def on_ready():
      print('We are logged in as {0.user}'.format(self.client))

    @self.client.event
    async def on_message(message):
      if(message.author == self.client.user):
        return 
      
      if(message.content.startswith('$hey')):
        await message.channel.send("Hello!")

      if(message.content.startswith('$hello')):
        await message.channel.send("Hey!")

      if(message.content.startswith('$hi')):
        await message.channel.send("Hi!")

      if(message.content.startswith('$inspire')):
        self.quote = self.get_quote() 
        await message.channel.send(self.quote)

      if any(word in message.content for word in self.sad_words):
        await message.channel.send(random.choice(self.starter_encouragements))
 
 
    self.client.run(os.environ['TOKEN'])
  
  def get_quote(self):
    self.response = requests.get("https://zenquotes.io/api/random")
    self.json_data  = json.loads(self.response.text)
    self.quote = self.json_data[0]['q'] + " - " + self.json_data[0]['a']

    return self.quote 

keep_alive()
c = bot()

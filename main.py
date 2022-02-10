import discord as d
import os
import requests
import json
import random
from keep_alive import keep_alive
#from replit import db
from db import my_data_base

class bot:
  def __init__(self):
    self.client = d.Client()
    self.sad_words = ["sad","depressed","angry","unhappy","depressing"]

    self.starter_encouragements = ["cheer up!" , "Hang in there.", "you are a great person /bot!" ]
    
    self.mydb = my_data_base();


    @self.client.event
    async def on_ready():
      print('We are logged in as {0.user}'.format(self.client))

    @self.client.event
    async def on_message(message):
      if(message.author == self.client.user):
        return 
      
      if(message.content.startswith('$hey')):
        await message.channel.send("Hello! "+str(message.author.mention))

      if(message.content.startswith('$hello')):
        await message.channel.send("Hey! "+str(message.author.mention))

      if(message.content.startswith('$hi')):
        await message.channel.send("Hi! "+str(message.author.mention))

      if(message.content.startswith('$inspire')):
        self.quote = self.get_quote() 
        await message.channel.send(self.quote)

      if(message.content.startswith('$add_to_list')):
        self.tempo = (message.content).split(" ")
        self.tempo = self.tempo[1:]
        self.mess = ""
        for parts in self.tempo:
          self.mess += parts
        self.mydb.add(str(message.author),(self.mess))
      
      if(message.content.startswith('$show_my_list')):
        self.temp_list = self.mydb.display(str(message.author))
        i = 1
        #await message.channel.send((self.temp_list))
        temp_message = "To do list of "+ str(message.author)+" \n"
        for self.mess in self.temp_list:
          temp_message+=("  "+str(i)+") "+self.mess+"\n")
          i = i+1
        await message.channel.send("```ini\n"+temp_message+"\n```")


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
c.mydb.close()

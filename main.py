import discord as d
import os
import requests
import json
import random
from keep_alive import keep_alive
from db import my_data_base
#from plot import poll
#from textmagic.rest import TextmagicRestClient
from email.mime.text import MIMEText
#from email.mime.image import MIMEImage
#from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib

class bot:
  def __init__(self):
    self.client = d.Client()
    self.sad_words = ["sad","depressed","angry","unhappy","depressing"]

    self.starter_encouragements = ["cheer up!" , "Hang in there.", "you are a great person /bot!" ]
    
    self.mydb = my_data_base()
    #self.plot = poll()

    self.instructions = ">>> Hey there!,\nI am **Cheems**,the **~~helper~~ bot**\n\nHere is a list of __**commands**__ which are helpful to operate me.\n\n\n```\nSimple short user Commands\n```\n**__$hey, $hi, $hello__** these for are pinging me.\n\n**__$inspire__** for getting a Quote of inspiration.\n\n\n```\nTo-Do list Commands\n```\n**__$add__  [CONTENT] - ** for adding the _'CONTENT'_ to your TO-DO list.\n\n**__$show__ - ** for displaying your TO-DO list.\n\n**__$delete__  [no] - ** for deleting the item numbered _'no'_ from your TO-DO list.\n\n**__$clear__ - ** to empty your TO-DO list.\n ```\nNOTE :\n```\n_**Kindly try to avoid the usage of emoji's in the content of your TO-DO list**_. \n"


    @self.client.event
    async def on_ready():
      print('We are logged in as {0.user}'.format(self.client))

    @self.client.event
    async def on_message(message):
      if(message.author == self.client.user):
        return 
      
      if(message.content.startswith('$help')):
        await message.channel.send(self.instructions)
      
      if(message.content.startswith('$hey')):
        await message.channel.send("Hello! "+str(message.author.mention))

      if(message.content.startswith('$hello')):
        await message.channel.send("Hey! "+str(message.author.mention))

      if(message.content.startswith('$hi')):
        await message.channel.send("Hi! "+str(message.author.mention))

      if(message.content.startswith('$inspire')):
        self.quote = self.get_quote() 
        await message.channel.send(self.quote)

      if(message.content.startswith('$add')):
        self.tempo = (message.content).split(" ")
        self.tempo = self.tempo[1:]
        self.mess = ""
        for parts in self.tempo:
          self.mess += parts + " "
        self.mydb.add(str(message.author),(self.mess))
        await message.channel.send("**" + self.mess + "**" + " has been added to your list successfully!")
      
      if(message.content.startswith('$show')):
        self.temp_list = self.mydb.display(str(message.author))
        i = 1
        #await message.channel.send((self.temp_list))
        temp_message = "To do list of "+ str(message.author)+" \n"
        for self.mess in self.temp_list:
          temp_message+=("  "+str(i)+") "+self.mess+"\n\n")
          i = i+1
        await message.channel.send("```json\n"+temp_message+"\n```")
      
      if(message.content.startswith('$delete')):
        self.tempo = (message.content).split(" ")
        self.tempo = self.tempo[1:]
        no = int(str(self.tempo[0]))
        
        if(no > 0):
          msg = self.mydb.delete(str(message.author),no)
          
          if msg != "\0":
            await message.channel.send(msg)
          else:
            await message.channel.send("Sorry! No such task with the given index exists in your list.")

      if(message.content.startswith('$edit')):
        no = (message.content).split(" ")
        msgl = no[2:]
        msg = ""
        for i in msgl:
          msg += i + " "
        if(int(no[1]) > 0):
          m = self.mydb.edit(str(message.author) ,int(no[1]),msg)

          if m != "\0":
            await message.channel.send(m)
          else:
            await message.channel.send("Sorry! No such task with the given index exists in your list.")
            
      
      if(message.content.startswith('$clear')):
        self.mydb.clear(str(message.author))
        await message.channel.send("Your list has been cleared succesfully!")

      if(message.content.startswith('$ping me')): 
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.ehlo()
        smtp.starttls()
        smtp.login('cheems1911@gmail.com', 'Cheems@Ayyappa1911')

        msg = MIMEMultipart()
        msg['Subject'] = "Ping from Cheems"
        msg.attach(MIMEText("Hi there,\n\tI am your cheems, the helper bot. Please don't block me if this testing spams your mail box!! OwO.")) 
        
        
        to = ['ayyappakoppuravuri1908@gmail.com', 'teja00219@gmail.com']
        smtp.sendmail(from_addr="cheems1911@gmail.com",to_addrs=to, msg=msg.as_string())
        smtp.close()
        


      if(message.content.startswith('$send_plot')):
        my_filename = 'poll.png';
        with open(my_filename, "rb") as fh:
          f = d.File(fh, filename=my_filename)
        await message.channel.send(file=f)


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
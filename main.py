import discord
import os
import random
from datetime import datetime
import mysql.connector
import re

activity = discord.Activity(name='everything!', type=discord.ActivityType.watching)
client = discord.Client(activity=activity)

ayat_sedih = ['sedih', 'down', 'unhappy']
bot_self = ['<@848146220869484544>', '<@&848146220869484544>', '<@!848146220869484544>', '@&848146481034952725']
ayat_penyedap = ['Kau chill boleh tak?', 'Apahal? Cer cite', 'Kesah pulak aku.']
ayat_penyapa = ['hi', 'weh', 'oi', 'woi']
ayat_masa = ['pukul berapa sekarang?', 'sekarang pukul berapa?', 'pukul berapa?', 'pukul?']
ayat_reminder = ['ingatkan aku']
ayat_penyudah = ['K.', 'Yela.', 'Ha yela, yela.', 'Done']

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="620503",
    database="discord"
)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    msg = message.content

    #print(str(msg).split()[0])

    if message.author == client.user:
        return

    if any(word in msg for word in bot_self):
    
        if(len(str(msg).split()) == 1):
            await message.channel.send('Apa kau nak?')

        elif(len(str(msg).split()) == 2 and str(msg).split()[0].lower() in ayat_penyapa):
            await message.channel.send('Panggil saya ke?')

        elif(msg.endswith(('dah makan?', 'dah makan ke?'))):
            await message.channel.send('Soalan apa tu? Aku robot kot.')

        elif any(word in msg for word in ayat_masa):
            now = datetime.now()
            current_time = now.strftime("%I:%M %p")
            await message.channel.send('Takde jam ke? '+current_time)

        elif any(word in msg for word in ayat_sedih):
            await message.channel.send(random.choice(ayat_penyedap))

        
        elif any(word in msg for word in ayat_reminder):
            mycursor = mydb.cursor()
            sql = "INSERT INTO reminders (member_id, message) VALUES (%s, %s)"
            val = (message.author.id, re.findall(r'(?<=ingatkan aku )[^.]*', msg)[0])
            mycursor.execute(sql, val)
            mydb.commit()
            await message.channel.send(random.choice(ayat_penyudah))

        else: 
            await message.channel.send('Aku tak faham lah kau cakap apa.')
    
client.run('ODQ4MTQ2MjIwODY5NDg0NTQ0.YLIXuA.hN6BKqFKcRu_ZWfTUI3oMy54BIA')

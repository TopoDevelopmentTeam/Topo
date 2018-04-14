'''
__author__ = "Mateo Cetti, Ivan Nuñez, Francesco Silvetti"
__copyright__ = "Copyright 2018, The TOPO Project"
__credits__ = ["Mateo Cetti", "Ivan Nuñez", "Francesco Silvetti"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = ["Mateo Cetti", "Ivan Nuñez", "Francesco Silvetti"]
__email__ = None
__status__ = "Work in progress"
'''

import discord #Import Discord.py.
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands

import wikipedia
from googletrans import Translator #Google Translator API.

import time
import json
from utilities.functions import *

class Bot(commands.Bot):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

def main():

    bot = Bot(command_prefix=commands.when_mentioned_or("-"), description='This is a BOT.', pm_help=True) #Instanciate the Bot.

    @bot.event
    async def on_ready():
        '''
        This method is called when the bot is succesfully loged in into Discord.
        '''
        print("READY")
        print(bot.user.name)
        print(bot.user.id)
        print('------')

    @bot.event
    async def on_message(message):
        '''
        This method is called when the bot receives a message from any Discord client.
        '''
        await bot.process_commands(message) #MAGIC

        print(str(time.time()) + ' :Message received from: ' + str(message.author.id) + ' , And says: ' + str(message.content))

        if (contains_not_allowed_characters(message)):

            await bot.delete_message(message)

    @bot.command(pass_context=True)
    async def japanify(ctx, *args):
        '''
        Translates Roman text to Japanese.
        '''
        translator = Translator()
        translation = translator.translate(" ".join(args), dest="ja")
        await bot.send_message(ctx.message.author, "Original (Roman): {}\nTranslated (Japanese): {}".format(" ".join(args), translation.text))

    @bot.command(pass_context=True)
    async def romanify(ctx, *args):
        '''
        Translates Japanese text to Roman.
        '''
        translator = Translator()
        translation = translator.translate(" ".join(args), dest="es")
        await bot.send_message(ctx.message.author, "Original (Japanese): {}\nTranslated (Roman): {}".format(" ".join(args), translation.text))

    @bot.command(pass_context=True)
    async def wiki(ctx, *args):
        '''
        Searches a Japanesse Query in Wikipedia.
        '''
        #author = ctx.message.author
        #await bot.delete_message(ctx.message)
        wikipedia.set_lang('ja')
        msg = " ".join(args)
        search = wikipedia.search(msg)
        bot_msg = '```'
        if (len(search) < 5):
            cant = len(search)
        else:
            cant = 5
        for i in range(0, cant):
            bot_msg += '{}: {}\n'.format(i, search[i])        
        bot_msg += '```'
        await bot.send_message(ctx.message.author, bot_msg)
        index = await bot.wait_for_message(author=ctx.message.author, check=check)
        j = int(index.content)
        wiki_summary = wikipedia.summary(search[j], sentences=1)
        link = 'https://ja.wikipedia.org/wiki/{}'.format(search[j])
        await bot.send_message(ctx.message.author, '{}\n{}'.format(wiki_summary, link))

    def check(msg):
        return (msg.content in ['0', '1', '2', '3', '4'])

    try:

        with open('botinfo.json') as info_file:

            data = json.load(info_file)

        bot.run(data['bot'][0]['token']) #Runs TOPO using the token

    except Exception as e:

        print(e)

if __name__ == '__main__':
    main()

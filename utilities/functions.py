import discord
import asyncio
import wikipedia

from discord.ext import commands
from discord.ext.commands import Bot

def contains_not_allowed_characters(message):

    if (message.author.id != '434739824805806082'):

        not_allowed_characters = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'

        for char in message.content:

            for not_allowed in not_allowed_characters:

                if(char == not_allowed):

                    return True

        return False

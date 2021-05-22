import discord, string, asyncio
from discord.ext import commands, tasks


class rename:

    def __init__(self, bot, message):
        self.bot = bot
        self.message = message

    async def check_pseudo(self):
        message = self.message
        user = message.author
        name = user.nick
        if name is None:
            name = user.name
        for char in name:
            if char not in string.printable and char not in ('ê', 'é', 'è', 'à', 'Ͼ', 'M', 'Λ', 'Я', 'M'):
                member = message.author
                nick = '[AUTO] Renommage Automatique'
                await member.edit(nick=nick)
                await message.channel.send(f'Pseudo non-mentionnable facilement, je l\'ai changé de  {name} en {user.mention}.\nFais `c@!nickname < pseudo >` pour changer de pseudo !')
                return
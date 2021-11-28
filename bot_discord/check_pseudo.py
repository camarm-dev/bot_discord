import pseudo
from discord.ext import commands

bot = commands.Bot(command_prefix = "!!!!!!", description = "Official Community Chat Bot checkpseudo")


@bot.event
async def on_message(message):
    await pseudo.rename(bot, message).check_pseudo()
    if message.channel.id == 829360461660553216 or message.channel.id == 829668214354608169 or message.channel.id == 829710163619086386:
        if message.content.startswith('<ticket'):
            pass
        else:
            await message.delete()


bot.run("ODIyMTU2NzI3NDQ0NzAxMTg0.YFOLHg.VKK2MQsIo45SfxeO221nyZ8aws4")

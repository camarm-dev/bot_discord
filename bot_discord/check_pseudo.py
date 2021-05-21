import pseudo
from discord.ext import commands

bot = commands.Bot(command_prefix = "!!!!!!", description = "Official Community Chat Bot checkpseudo")


@bot.event
async def on_message(message):
    await pseudo.rename(bot, message).check_pseudo()
    if message.channel.id == 829360461660553216:
        if message.content.startswith('<ticket'):
            pass
        else:
            await message.delete()


#bot.run("NzcwNTk5MTIxMTUyOTAxMTYw.X5f6Ww.-MiZk-sJm6XMuUpF2z8EB0wagss")
bot.run("ODIyMTU2NzI3NDQ0NzAxMTg0.YFOLHg.VKK2MQsIo45SfxeO221nyZ8aws4")

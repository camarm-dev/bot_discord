import json

import discord
from discord.ext import commands, tasks
import random
import time
import asyncio
import message

bot = commands.Bot(command_prefix="<", description=" Official Team pêcheur Bot")

status = ["tp!help",
        "V0.0.0",
        "A votre service",
        "Team Pêcheur Bot",
        "Je suis connecter",
        "Mieux que toi"]


warns = {}
warns_reason = {}

@tasks.loop(seconds = 5)
async def changeStatus():
    game = discord.Game(random.choice(status))
    await bot.change_presence(status = discord.Status.online, activity = game)


@bot.command()
@commands.has_permissions(administrator = True)
async def start(ctx, password, secondes = 5):
    if password in ("sudo"):
        changeStatus.start()
        changeStatus.change_interval(seconds = secondes)
    else:
        await ctx.send("Permission non accordée")


@bot.command()
@commands.has_permissions(administrator = True)
async def load(ctx, backup):
    passed = False
    global warns, warns_reason
    try:
        with open('backup_id.txt') as id:
            base_nb = backup
            backup = int(backup.replace(".", ""))
            backup_id = int(id.read().replace(".", ""))
            if backup_id == backup:
                with open('warns.txt', 'r+') as warns_file:
                    warns = json.loads(warns_file.read())
                    warns_file.close()
                with open('warns_reason.txt', 'r+') as warns_reason_file:
                    warns_reason = json.loads(warns_reason_file.read())
                    warns_reason_file.close()
                    await ctx.send(f"La backup {backup} a bien été chargée\nLes warns précédent ont été remplacés par ceux de la backup {base_nb} !")
                    passed = True
        id.close()
        if not passed:
            await ctx.send(f"La backup {backup} n'a pas été chargée\nUne erreur est survenue veuillez recommencer .")
    except Exception as e:
        await ctx.send(f"La backup {backup} n'a pas été chargée\nUne erreur est survenue veuillez recommencer .")
        raise e


@bot.event
async def on_ready():
    print('\nBot joining...')
    print('\nBot is online')
    print('\nCommands setuping...')
    print('\nCommands are setuped')
    print('\nReady!')


@bot.command()
async def nickname(ctx, *name):
    name = " ".join(name)
    original = ctx.message.author.nick
    if original is None:
        original = ctx.message.author.name
    await ctx.message.author.edit(nick=name)
    embed = discord.Embed(title=f"Tu as bien été renommer {ctx.message.author.name}#{ctx.message.author.discriminator}", color=8026)
    embed.add_field(name=f"Avant: {original} ->\tAprès: {name}", value="Bien joué à lui !", inline=False)
    await ctx.send(embed=embed)


# @bot.event
# async def on_command_error(ctx, error):
# 	if isinstance(error, commands.CommandNotFound):
# 		await ctx.send("Command not found :(")
#
# 	if isinstance(error, commands.MissingRequiredArgument):
# 		await ctx.send("Il manque un argument.")
# 	elif isinstance(error, commands.MissingPermissions):
# 		await ctx.send("Vous n'avez pas les permissions pour faire cette commande.")
# 	elif isinstance(error, commands.CheckFailure):
# 		await ctx.send("Oups vous ne pouvez pas utilisez cette commande.")
# 	if isinstance(error.original, discord.Forbidden):
# 		await ctx.send("Le bot n'a pas les permissions nécéssaires pour faire cette commmande")


@bot.command()
async def serverinfo(ctx):
    server = ctx.guild
    numberOfTextChannels = len(server.text_channels)
    numberOfVoiceChannels = len(server.voice_channels)
    serverDescription = server.description
    numberOfPerson = server.member_count
    serverName = server.name
    message = f"Le serveur **{serverName}** contient **{numberOfPerson}** personnes ! \nLa description du serveur est **{serverDescription}**. \nCe serveur possède **{numberOfTextChannels}** salons écrits et **{numberOfVoiceChannels}** salon vocaux."
    await ctx.send(message)


@bot.command()
async def info(ctx):
    embed = discord.Embed(title="Discord Community Chat Bot V1.2.1", description="Le Team Pêcheur Bot est développé avec python (discord.py)", color=8026)
    embed.add_field(name="Commande d'aide :", value="`<help`", inline=False)
    embed.add_field(name="Editeur :", value="Développé par CAMARM_Flipz", inline=False)
    await ctx.send(embed=embed)


@bot.command()
async def ticket(ctx, *texte):
    if len(texte) < 1:
        return
    if ctx.channel.id != 829360461660553216 and ctx.channel.id != 829710163619086386:
        return
    await ctx.message.delete()
    user = ctx.message.author
    embed = discord.Embed(name="Confirmation de ticket:", description=f"Avant d'envoyer ton message :\n{' '.join(texte)}\n assure toi d'avoir respecter ces 3 règles:", color=8026)
    embed.add_field(name="1:", value="-Le message ne contient pas d'insultes/contenue choquant", inline=False)
    embed.add_field(name="2:", value="- Il vise a améliorer, suggérer quelque chose ou signaler un comportement inaproprié (et non autre chose)", inline=False)
    embed.add_field(name="3:", value="-La demande est réalisable", inline=False)
    embed.add_field(name="A toi de voir:", value=f"Si ton message respecte ces 3 règles et que tu est sure de l'envoyer réagis avec ✅ sinon réagis avec ❌  \nSi tout ce passe bien, au bout de 1min je réagis avec ☑, sinon je t'envoie un message et réagis avec ⛔ pour te dire que le ticket n'est plus valide.\n\nCordialement, de {bot.user.mention} pour {ctx.author.mention} !", inline=False)
    message_at = await user.send(embed=embed)
    await message_at.add_reaction("✅")
    await message_at.add_reaction("❌")

    try:
        tic = time.perf_counter()
        while True:
            print(time.perf_counter() - tic)
            cache_msg = await message_at.channel.fetch_message(message_at.id)
            time.sleep(2)
            count = str(cache_msg.reactions).replace(f"<Reaction emoji='{cache_msg.reactions[0]}' me=True count=", "").replace(">", "")
            count = int(count[1:2])
            count_no = str(cache_msg.reactions).replace(f"<Reaction emoji='{cache_msg.reactions[0]}' me=True count={count}>, <Reaction emoji='{cache_msg.reactions[1]}' me=True count=", "").replace(">", "")
            count_no = int(count_no[1:2])
            count_react = len(cache_msg.reactions)
            if count >= 2 or count_no >= 2 or count_react >= 3:
                try:
                    if str(cache_msg.reactions[0]) == "✅" and count >= 2:
                        message.send(' '.join(texte), ctx.message.author.mention)
                        await ctx.message.author.send("**L'idée/retour/plainte/aide a bien été envoyé !**")
                        await message_at.add_reaction("☑️")
                    else:
                        await ctx.message.author.send("L'envoie a bien été annulé.")
                        if count_no == 2:
                            pass
                        else:
                            await ctx.message.author.send(f"(Et au juste ton émoji {cache_msg.reactions[2]} je l'ai vu et c'est pas celui que j'attendais petit malin !)")
                    break
                except:
                    continue
            else:
                if time.perf_counter() - tic >= 60:
                    raise TimeoutError
                pass
    except Exception as e:
        if e.__class__.__name__ == "TimeoutError":
            await ctx.message.author.send("Temps écoulé le ticket n'est plus valide")
            await message_at.add_reaction("⛔")
            return
        embed = discord.Embed(name="Echec de la onfirmation de ticket:", description=f"L'envoie de votre ticket à échoué...", color=8026)
        embed.add_field(name="Solutions:", value="Réitérez la commande ou demandez de l'aide ici : https://discord.gg/DSqBxUjAqU !", inline=False)
        await ctx.message.author.send(embed=embed)
        await ctx.message.author.send("Temps écoulé le ticket n'est plus valide")
        await message_at.add_reaction("⛔")
        raise e


@bot.command()
async def say(ctx, *texte : str):
    embed = discord.Embed(title=f"{ctx.message.author} a dit", description=" ".join(texte), color=8026)
    embed.add_field(name="Le 15 janvier 3012", value="Respect à lui...", inline=False)
    await ctx.send(embed=embed)


@bot.command()
async def carspe(ctx, *text):
    chineseChar = "丹书匚刀巳下呂廾工丿片乚爪冂口尸Q尺丂丁凵V山乂Y乙"
    chineseText = []
    for word in text:
        for char in word.lower():
            if char.isalpha():
                index = ord(char) - ord("a")
                transformed = chineseChar[index]
                chineseText.append(transformed)
            else:
                chineseText.append(char)
        chineseText.append(" ")
    embed = discord.Embed(title="".join(chineseText), description=f"{ctx.message.author} a changé la police !", color=8026)
    await ctx.send(embed=embed)


@bot.command()
@commands.has_permissions(administrator = True)
async def ban(ctx, user : discord.User, *reason):
    if len(reason) <= 0:
        reason = 'Pas de raison donnée'
    else:
        reason = " ".join(reason)
    await ctx.guild.ban(user, reason=reason)
    embed = discord.Embed(title=f"{user} à été ban !", color=8026)
    embed.add_field(name="Pour:", value=f"{reason}", inline=False)
    await ctx.send(embed=embed)


@bot.command()
@commands.has_permissions(administrator = True)
async def ban_list(ctx):
    bannedUsers = await ctx.guild.bans()
    embed = discord.Embed(title=f"Utilisateurs bannis:", color=8026)
    for user in bannedUsers:
        embed.add_field(name=f"{user.user.name}#{user.user.discriminator}", value=f"A été bannis pour : {user.reason}.", inline=False)
    await ctx.send(embed=embed)


@bot.command()
@commands.has_permissions(administrator = True)
async def unban(ctx, *user):
    user = " ".join(user)
    userName, userId = user.split("#")
    bannedUsers = await ctx.guild.bans()
    for i in bannedUsers:
        if i.user.name == userName and i.user.discriminator == userId:
            await ctx.guild.unban(i.user)
            await ctx.send(f"{user} à été unban.")
            return
    #Ici on sait que lutilisateur na pas ete trouvé
    await ctx.send(f"L'utilisateur {user} n'est pas dans la liste des bans")


@bot.command()
@commands.has_permissions(administrator = True)
async def kick(ctx, user : discord.User, *reason):
    reason = " ".join(reason)
    await ctx.guild.kick(user, reason = reason)
    await ctx.send(f"{user} à été kick.")


@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def clear(ctx, nombre : int):
    await ctx.channel.purge(limit=nombre + 1)
    await ctx.send(f'**:white_check_mark:{nombre} messages** supprimés !')

@bot.command()
@commands.has_permissions(administrator = True)
async def nickname_ultra(ctx, user: discord.Member, *nick):
    nick = " ".join(nick)
    await user.edit(nick=nick)
    if len(nick) <= 0:
        nick = 'Pseudo original'
    embed = discord.Embed(title=f"Modérateur {ctx.message.author.name}#{ctx.message.author.discriminator} a renommé", color=8026)
    embed.add_field(name=f"{user.name}#{user.discriminator}", value=f"En {nick}", inline=False)
    await ctx.send(embed=embed)


@bot.command()
@commands.has_permissions(administrator=True)
async def warn(ctx, user: discord.User, *reason):
    reason = " ".join(reason)
    guild_name = ctx.guild.id
    if guild_name not in warns:
        warns[guild_name] = {}
        warns[guild_name][user.id] = 1
    if guild_name not in warns_reason:
        warns_reason[guild_name] = {}
        warns_reason[guild_name][user.id] = {}
        warns_reason[guild_name][user.id]['1'] = reason
    elif guild_name in warns:
        if user.id not in warns[guild_name]:
            warns[guild_name][user.id] = 1
            warns_reason[guild_name][user.id] = {}
            warns_reason[guild_name][user.id]['1'] = reason
        else:
            warns[guild_name][user.id] += 1
            nb_warns = warns[guild_name][user.id]
            warns_reason[guild_name][user.id][str(nb_warns)] = reason
    if warns[guild_name][user.id] == 1:
        ter = 'er'
    elif warns[guild_name][user.id] != 1:
        ter = 'ème'
    embed = discord.Embed(title=f"Modérateur {ctx.message.author.name}#{ctx.message.author.discriminator} a warn {user.name}#{user.discriminator}", color=8026)
    embed.add_field(name=f"C'est son {warns[guild_name][user.id]}{ter} warn.", value=f"!!! Attention !!! Mercị̣ de bien respecter les règles @everyone !!!", inline=False)
    await ctx.send(embed=embed)


@bot.command()
@commands.has_permissions(administrator=True)
async def warns_of(ctx, user: discord.User):
    compteur = 0
    try:
        user_warns = warns[ctx.guild.id][user.id]
    except:
        user_warns = 'aucun'
    embed = discord.Embed(title=f"Warns de {user.name}#{user.discriminator}:", color=8026)
    embed.add_field(name=f"{user.name}#{user.discriminator} a {user_warns} warns", value="_____________________________", inline=False)
    try:
        for warn_reason in warns_reason[ctx.guild.id][user.id]:
            compteur +=1
            if compteur == 1:
                ter = 'er'
            elif compteur != 1:
                ter = 'ème'
            embed.add_field(name=f"{compteur}{ter} warns", value=f"{warns_reason[ctx.guild.id][user.id][str(compteur)]}", inline=False)
    except:
        pass
    await ctx.send(embed=embed)


@bot.command()
@commands.has_permissions(administrator=True)
async def backup(ctx):
    bc_id = len(warns) + len(warns_reason) * 99.9
    with open('warns.txt', 'w+') as f_warn:
        f_warn.write(json.dumps(warns))
        f_warn.close()
    with open('warns_reason.txt', 'w+') as f_reason:
        f_reason.write(json.dumps(warns_reason))
        f_reason.close()
    with open('backup_id.txt', 'w+') as backup_id:
        backup_id.write(str(bc_id))
        backup_id.close()
    embed = discord.Embed(title=f"Backup de {bc_id} informations liées au serveur:", color=8026)
    embed.add_field(name=f"La backup a bien été effectuée, pour recharger celle-ci au démarrage du bot faite:", value=f"`<load {bc_id}`", inline=False)
    embed.add_field(name=f"Identifiant de backup:", value=f"`{bc_id}`", inline=False)
    await ctx.send(embed=embed)

bot.run("ODIyMTU2NzI3NDQ0NzAxMTg0.YFOLHg.VKK2MQsIo45SfxeO221nyZ8aws4")

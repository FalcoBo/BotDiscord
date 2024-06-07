import discord 
from discord.ext import commands
from commandhistory.List_CommandHistory import List_CommandHistory
from Data.functions_bot import load_command_history, save_command_history
import random

TOKEN = ""

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
list_history = List_CommandHistory()
# command_history_locks = {} Dictionnaire pour gérer les locks sur les commandes avec la hashmap
data_history = load_command_history()

# Launch the bot
@bot.event
async def on_ready():
    guild = bot.guilds[1]
    global data_history
    data_history = load_command_history()
    print("Le bot est prêt !")

# Use the bot on only one channel "bot"
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.channel.name != "bot":
        return

    await bot.process_commands(message) 

# Stop the bot
@bot.event
async def on_disconnect():
    # save_data(data_history)
    print("Bot déconnecté. Les données ont été sauvegardées.")

# Erreur de commande
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Cette commande n'existe pas. Veuillez réessayer avec une commande valide.\nTapez **!commands**  pour afficher la liste des commandes disponibles.")

# A new member join the server and take the role "Imigrés"
@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name="Imigrés")
    await member.add_roles(role)


# TOUTES LES COMMANDES
# Ajout d'une fonction pour suivre les commandes utilisées
def track_command(func):
    async def wrapper(ctx, *args, **kwargs):
        list_history.append_command(func.__name__)
        await func(ctx, *args, **kwargs)
    return wrapper

# Commande d'aide qui permet d'afficher la liste des commandes disponibles
@bot.command(name="commands")
@track_command
async def command_help(ctx):
    filename_nouveau = "commands.txt"
    filename_admin = "commands_admin.txt"
    if any(role.name == "SENSEI" for role in ctx.author.roles):
        try :
            with open(filename_nouveau, "r") as file:
                response = file.read()
                await ctx.send(f"```{response}```")
        except FileNotFoundError:
            await ctx.send("```Aucun fichier de commandes n'a été trouvé```")


# !! IL FAUT ETRE ADMIN (OU ACTUELLEMENT LE ROLE "SENSEI") POUR UTILISER CETTE COMMANDE !!
@bot.command(name="clear_channel")
@track_command
async def clear_channel(ctx, amount=1500):
        user = ctx.author
        if any(role.name == "SENSEI" for role in user.roles):
            await ctx.channel.purge(limit=amount+1)
            await ctx.channel.send(f"```Tout les messages de ce channel ont été supprimés```")
        else:
            await ctx.channel.send("```Vous n'avez pas les droits pour utiliser cette commande.```")


# Commandes en rapport avec l'historique des commandes
# L'historique des commandes est enregistré dans un dictionnaire qui contient les commandes utilisées par chaque utilisateur dans chaque serveur
@bot.command(name="history")
async def history(ctx, user: discord.Member = None):
    if user is None:
        user = ctx.author

    server_name = ctx.guild.name

    if server_name in data_history and user.name in data_history[server_name]:
        user_commands = data_history[server_name][user.name]
        filtered_commands = [cmd for cmd in user_commands if cmd != "!history"]
        if filtered_commands:
            response = "\n".join(filtered_commands)
            await ctx.send(f"```Liste des commandes que tu as utilisé {user.name} dans ce serveur:\n{response}```")
        else:
            await ctx.send(f"```Aucune commande n'a été trouvée pour {user.name} dans ce serveur.```")
    else:
        await ctx.send(f"```Aucune commande n'a été trouvée pour {user.name} dans ce serveur.```")

# Event triggered when a command is completed
@bot.event
async def on_command_completion(ctx):
    server_name = ctx.guild.name
    user_name = ctx.author.name
    command = ctx.message.content

    if server_name not in data_history:
        data_history[server_name] = {}

    if user_name not in data_history[server_name]:
        data_history[server_name][user_name] = []

    # async with command_history_locks[server_name]:
    data_history[server_name][user_name].append(command)
    save_command_history(data_history)


# Commandes pour l'historique des commandes
# First command
@bot.command(name="first")
async def first(ctx):
    if list_history.first is None:
        await ctx.channel.send("```Aucune commande enregistrée```")
        return
    else :
        first_command = list_history.get_first_command()
        await ctx.channel.send(f"```Voici la première commande : {first_command}```")

# Last command
@bot.command(name="last")
async def last(ctx):
    if list_history.last is None:
        await ctx.channel.send("```Aucune commande enregistrée```")
        return
    else :
        last_command = list_history.get_last_command()
        await ctx.channel.send(f"```Voici la dernière commande : {last_command}```")

# Clear history
@bot.command(name="clear_history")
async def clear_history(ctx):
    server_name = ctx.guild.name
    user_name = ctx.author.name

    if server_name in data_history and user_name in data_history[server_name]:
        del data_history[server_name][user_name]
        save_command_history(data_history)
        await ctx.channel.send("```L'historique des commandes a été supprimé !```")
    else:
        await ctx.channel.send("```Aucun historique de commandes trouvé pour cet utilisateur dans ce serveur.```")


# Command to ban a user (only for admin)
@bot.command(name="ban")
@track_command
async def ban(ctx, user: discord.Member, *, reason=None):
    if any(role.name == "Master" for role in user.roles):
        await user.ban(reason=reason)
        await ctx.send(f"{user} a été banni !")


# Command for a mystery pick for valorant agent
@bot.command(name="mystery_pick")
@track_command
async def mystery_pick(ctx):
    agents = {
        "Astra": "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExMDh0M2U3eTdkN2RzenJiZXc0NjcyZ2J4emtiOWh6NGltcDJwMXM5bCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/66ypQhs0NDgUXLtWxp/giphy-downsized-large.gif",
        "Breach": "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3NsdmFncnRvaHZjdHFidWx6NHk5djN6cGpkbHZlMWxoeGd1cG1hOCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3M8bTKtEN84lgdznll/giphy.gif",
        "Brimstone": "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3NsdmFncnRvaHZjdHFidWx6NHk5djN6cGpkbHZlMWxoeGd1cG1hOCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3M8bTKtEN84lgdznll/giphy.gif",
        "Cypher": "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExYnk4a2U2aDRzMHE0YmY5cXUxeGM5cW5nNmgzN25hZWlnZmNsdXdjdiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/jRtZJvoWxWVJ7uF1cx/giphy.gif",
        "Clove" : "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExYnk4a2U2aDRzMHE0YmY5cXUxeGM5cW5nNmgzN25hZWlnZmNsdXdjdiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/jRtZJvoWxWVJ7uF1cx/giphy.gif",
        "Chamber": "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExYnk4a2U2aDRzMHE0YmY5cXUxeGM5cW5nNmgzN25hZWlnZmNsdXdjdiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/jRtZJvoWxWVJ7uF1cx/giphy.gif",
        "Geko" : "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExOWFvczF3dXg4eTZyNTRlYzhrMWI1MXgwdmprdmQ1d3R2dG9yb3NqYSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/1roEXC1g4difJ3F3wa/giphy.gif",
        "Jett": "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExbXp5OW44bjZvbWRkc2lnajFnMHdtN3IwNW4ybmZ4NDVzZWV3NGF6ZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/2M8ySvCe6OkyPZIhM6/giphy.gif",
        "Killjoy": "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExN3EyZHVsbW9lb2ZtZTdrejZ2cHIwd3k4dTN6dm5jcnhzM3RnbGh4MSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/aHA3cHzwZLb0wGq53a/giphy.gif",
        "Omen": "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExYTJ5OGdkcXFwMjg2eGZ4MDVlMW41ZzdkZnN3eWg2Y2oxN2xxeDh5NiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/OvXOVKpUbGQzmW6GPH/giphy.gif",
        "Phoenix": "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExMmtrZ3o1MWtwZ2Y0NzVjbnZ6Y2pxY2JwMzRneDhrNmFjZHRhOHZnMSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/TzQ4pMIO0E0DjUlcbB/giphy.gif",
        "Raze": "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExeXBnZTZoODdhZG9nbWc5a3d3N3d4ejBsbWl4MnZrNmRsMHlnYmpvYSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/e6wlM2pxP7A71bPrvO/giphy.gif",
        "Reyna": "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExa21kNTU3a29laWx2ampqZjBpazl6ZGZxNDFhaDI4bjg2NXp5NjI5ZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/WqNmbi4La3IJg9PhcR/giphy-downsized-large.gif",
        "Sage": "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExYTU5dmJwOTh5M3kxZ3FxMnY5Zm5tZDl3ajlnbzM2dXVwaWZ2Z3BheSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/surwH0JQfjr7YfXzTg/giphy-downsized-large.gif",
        "Skye": "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExYXppbWZrYWx4NDMxbWhtajFvNzNud2VrY3cxMzJrcmhxeXloMWprcSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/IeCVgNtnx68peargEB/giphy.gif",
        "Sova": "https://giphy.com/clips/playvalorant-valorant-agent-fade-MRAh2ohEbYUs8zEu2d",
        "Viper": "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExOG5ya203Z2kybDY2dzN5Z2tmb3p5enp1Z20ydWsyMTdkcHlsbHd2ciZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/SW7epHMX7VeNzevLIz/giphy.gif",
        "Yoru": "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExZTZuNDYyMTU4ZzhtM2MzNXZkN2Z2Y28zdGlpeG45czR4OHFhMmg0dCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/JNwtPWpMlhmw2au5MG/giphy.gif",
        "Neon": "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExMmdyZHdwcnVzd2pncjFkNXB6MmsxeWY4OWpuMG53Z2lkbG96cmp0aiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/dlxLT7iDuwVxMHKI5c/giphy.gif"
    }

    agent = random.choice(list(agents.keys()))
    gif_url = agents[agent]
    
    await ctx.send(f"```Mystery pick : {agent}```")
    await ctx.send(gif_url)

# Command for a mystery pick for valorant gun
@bot.command(name="mystery_gun")
@track_command
async def mystery_gun(ctx):
    guns = {
        "Classic": "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExMmtrZ3o1MWtwZ2Y0NzVjbnZ6Y2pxY2JwMzRneDhrNmFjZHRhOHZnMSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/TzQ4pMIO0E0DjUlcbB/giphy.gif",
        "Shorty": "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExMmtrZ3o1MWtwZ2Y0NzVjbnZ6Y2pxY2JwMzRneDhrNmFjZHRhOHZnMSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/TzQ4pMIO0E0DjUlcbB/giphy.gif",
        "Frenzy": "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExMmtrZ3o1MWtwZ2Y0NzVjbnZ6Y2pxY2JwMzRneDhrNmFjZHRhOHZnMSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/TzQ4pMIO0E0DjUlcbB/giphy.gif",
        "Ghost": "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExMmtrZ3o1MWtwZ2Y0NzVjbnZ6Y2pxY2JwMzRneDhrNmFjZHRhOHZnMSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/TzQ4pMIO0E0DjUlcbB/giphy.gif",
        "Sheriff": "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExMmtrZ3o1MWtwZ2Y0NzVjbnZ6Y2pxY2JwMzRneDhrNmFjZHRhOHZnMSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/TzQ4pMIO0E0DjUlcbB/giphy.gif",
        "Stinger": "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExMmtrZ3o1MWtwZ2Y0NzVjbnZ6Y2pxY2JwMzRneDhrNmFjZHRhOHZnMSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/TzQ4pMIO0E0DjUlcbB/giphy.gif",
        "Spectre": "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExMmtrZ3o1MWtwZ2Y0NzVjbnZ6Y2pxY2JwMzRneDhrNmFjZHRhOHZnMSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/TzQ4pMIO0E0DjUlcbB/giphy.gif",
        "Bucky": "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExMmtrZ3o1MWtwZ2Y0NzVjbnZ6Y2pxY2JwMzRneDhrNmFjZHRhOHZnMSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/TzQ4pMIO0E0DjUlcbB/giphy.gif",
        "Judge": "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExMmtrZ3o1MWtwZ2Y0NzVjbnZ6Y2pxY2JwMzRneDhrNmFjZHRhOHZnMSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/TzQ4pMIO0E0DjUlcbB/giphy.gif",
        "Ares": "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExMmtrZ3o1MWtwZ2Y0NzVjbnZ6Y2pxY2JwMzRneDhrNmFjZHRhOHZnMSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/TzQ4pMIO0E0DjUlcbB/giphy.gif",
        "Odin": "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExMmtrZ3o1MWtwZ2Y0NzVjbnZ6Y2pxY2JwMzRneDhrNmFjZHRhOHZnMSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/TzQ4pMIO0E0DjUlcbB/giphy.gif",
        "Phantom": "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExMmtrZ3o1MWtwZ2Y0NzVjbnZ6Y2pxY2JwMzRneDhrNmFjZHRhOHZnMSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/TzQ4pMIO0E0DjUlcbB/giphy.gif",
        "Vandal": "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExMmtrZ3o1MWtwZ2Y0NzVjbnZ6Y2pxY2JwMzRneDhrNmFjZHRhOHZnMSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/TzQ4pMIO0E0DjUlcbB/giphy.gif",
        "Marshal": "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExMmtrZ3o1MWtwZ2Y0NzVjbnZ6Y2pxY2JwMzRneDhrNmFjZHRhOHZnMSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/TzQ4pMIO0E0DjUlcbB/giphy.gif",
        "Operator": "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExMmtrZ3o1MWtwZ2Y0NzVjbnZ6Y2pxY2JwMzRneDhrNmFjZHRhOHZnMSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/TzQ4pMIO0E0DjUlcbB/giphy.gif",
        "Guardian": "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExMmtrZ3o1MWtwZ2Y0NzVjbnZ6Y2pxY2JwMzRneDhrNmFjZHRhOHZnMSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/TzQ4pMIO0E0DjUlcbB/giphy.gif",
        "Bulldog": "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExMmtrZ3o1MWtwZ2Y0NzVjbnZ6Y2pxY2JwMzRneDhrNmFjZHRhOHZnMSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/TzQ4pMIO0E0DjUlcbB/giphy.gif",
        "Knife": "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExMmtrZ3o1MWtwZ2Y0NzVjbnZ6Y2pxY2JwMzRneDhrNmFjZHRhOHZnMSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/TzQ4pMIO0E0DjUlcbB/giphy.gif"
    }

    gun = random.choice(list(guns.keys()))
    gif_url = guns[gun]
    await ctx.send(f"```Mystery gun : {gun}```")
    await ctx.send(gif_url)


# Command for a mystery kick for kick a person from the voice channel
@bot.command(name="mystery_kick")
@track_command
async def mystery_kick(ctx):
    user = ctx.author
    if user.voice is None:
        await ctx.send("```Tu n'es pas dans un channel vocal```")
        return
    
    voice_channel = user.voice.channel
    members = voice_channel.members
    
    if len(members) < 2:
        await ctx.send("```Il n'y a pas assez de membres dans le channel vocal pour jouer```")
        return
    
    member_to_kick = random.choice(members)
    
    await member_to_kick.move_to(None)
    await ctx.send(f"```{member_to_kick.name} a été kick du channel vocal {voice_channel.name}```")

# Command for a mystery ban for ban 60s a person from the server
# @bot.command(name="mystery_ban")
# async def mystery_ban(ctx):
#     user = ctx.author
#     if user.voice is None:
#         await ctx.send("```Tu n'es pas dans un channel vocal```")
#         return
    
#     voice_channel = user.voice.channel
#     members = voice_channel.members

#     if len(members) < 2:
#         await ctx.send("```Il n'y a pas assez de membres dans le channel vocal pour jouer```")
#         return

#     # Choose a random member to ban
#     members = [member for member in members if member != user]
#     member_to_ban = random.choice(members)

#     # Ban the member for 60s
#     await ctx.guild.ban(member_to_ban, reason="Mystery ban", delete_message_days=0)
#     await ctx.send(f"```{member_to_ban.display_name} a été banni du serveur pour 60 secondes```")

#     # Beban the member after 60s
#     await asyncio.sleep(60)
#     await ctx.guild.unban(member_to_ban, reason="Bannissement temporaire terminé")
#     await ctx.send(f"```{member_to_ban.display_name} a été débanni du serveur```")

#     # Send an invite link to the banned member
#     invite = await ctx.channel.create_invite()
#     await member_to_ban.send(f"Tu as été banni du serveur pour 60 secondes. Voici un lien pour rejoindre le serveur: {invite}")


# Command to clear the 5 last messages
@bot.command(name="clear")
@track_command
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount+1)

#Token du bot
bot.run(TOKEN)
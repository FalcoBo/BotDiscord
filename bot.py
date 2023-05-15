import discord 
from discord.ext import commands
from commandhistory.List_CommandHistory import List_CommandHistory
from Data.functions_bot import load_command_history, save_command_history
import youtube_dl

TOKEN = ""

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
list_history = List_CommandHistory()
# command_history_locks = {} Dictionnaire pour gérer les locks sur les commandes avec la hashmap
data_history = load_command_history()

# Démarrage du bot
@bot.event
async def on_ready():
    guild = bot.guilds[1]
    channel = discord.utils.get(guild.channels, name='rôles')
    global data_history
    data_history = load_command_history()
    print("Le bot est prêt !")

    if channel is None:
        print("Le canal 'rôles' n'a pas été trouvé sur le serveur.")
        return

    async for message in channel.history():
        if message.author == bot.user:
            return
        
    message = await channel.send("Bienvenue sur le serveur! Réagissez avec l'emoji pour obtenir le rôle Nouveau.")
    await message.add_reaction('👍')

# Arrêt du bot
@bot.event
async def on_disconnect():
    # save_data(data_history)
    print("Bot déconnecté. Les données ont été sauvegardées.")

# Erreur de commande
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Cette commande n'existe pas. Veuillez réessayer avec une commande valide.\nTapez **!commands**  pour afficher la liste des commandes disponibles.")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if 'video' in message.content:
        await message.channel.send('https://www.youtube.com/watch?v=8P5WCI0iQlo')

    await bot.process_commands(message)

# Message de bienvenue et attribution d'un rôle pour les nouveaux utilisateurs
@bot.event
async def on_raw_reaction_add(payload):
    if payload.channel_id == 1106483823883071509:
        if payload.emoji.name == '👍':
            guild = bot.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            role = discord.utils.get(guild.roles, name='Nouveau')

            if role is not None:
                await member.add_roles(role)
                print(f"{member.name} a obtenu le rôle 'Nouveau'")
            else:
                print("Le rôle 'Nouveau' n'a pas été trouvé sur le serveur.")
        else:
            print("Une autre réaction que '👍' a été ajoutée au message de bienvenue.")

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
    if any(role.name == "Nouveau" for role in ctx.author.roles):
        try:
            with open(filename_nouveau, 'r') as file:
                content = file.read()
                await ctx.send(f"Voici la liste des commandes utilisables :\n```{content}```")
        except FileNotFoundError:
            await ctx.send(f"Le fichier {filename_nouveau} n'a pas été trouvé.")
    elif any(role.name == "Master" for role in ctx.author.roles):
        try:
            with open(filename_admin, 'r') as file:
                content = file.read()
                await ctx.send(f"Voici la liste des commandes utilisables pour les admins :\n```{content}```")
        except FileNotFoundError:
            await ctx.send(f"Le fichier {filename_admin} n'a pas été trouvé.")
    else: 
        await ctx.send("```Veuillez choisir un rôles dans le channel **rôles** pour pouvoir utiliser les commandes.```")

# Commande 
@bot.command(name="hello")
@track_command
async def hello(ctx):
    await ctx.send("Hello !")

# !! IL FAUT ETRE ADMIN (OU ACTUELLEMENT LE ROLE "Master") POUR UTILISER CETTE COMMANDE !!
@bot.command(name="clear_channel")
@track_command
async def clear_channel(ctx, amount=1500):
        user = ctx.author
        if any(role.name == "Master" for role in user.roles):
            await ctx.channel.purge(limit=amount+1)
            await ctx.channel.send(f"```Tout les messages de ce channel ont été supprimés```")
        else:
            await ctx.channel.send("```Vous n'avez pas les droits pour utiliser cette commande.```")

# Commande de test
@bot.command(name="txt")
@track_command
async def txt(ctx):
    await ctx.channel.send("Hello World !")

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
# Première commande
@bot.command(name="first")
async def first(ctx):
    if list_history.first is None:
        await ctx.channel.send("```Aucune commande enregistrée```")
        return
    else :
        first_command = list_history.get_first_command()
        await ctx.channel.send(f"```Voici la première commande : {first_command}```")

# Dernière commande
@bot.command(name="last")
async def last(ctx):
    if list_history.last is None:
        await ctx.channel.send("```Aucune commande enregistrée```")
        return
    else :
        last_command = list_history.get_last_command()
        await ctx.channel.send(f"```Voici la dernière commande : {last_command}```")

# Supprimer l'historique des commandes
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


# Commande pour lire des vidéos youtube dans un channel vocal
@bot.command(name="play")
@track_command
async def play(ctx, url):
    voice_channel = ctx.author.voice.channel

    if voice_channel is None:
        await ctx.send("Tu dois être connecté à un canal vocal pour utiliser cette commande.")
        return

    # Vérification si le bot est déjà connecté à un canal vocal
    if ctx.voice_client is not None:
        await ctx.voice_client.move_to(voice_channel)
    else:
        vc = await voice_channel.connect()

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        vc.play(discord.FFmpegPCMAudio(url2))

    await ctx.send(f"Lecture de la vidéo : {info['title']}")

@bot.command(name="stop")
@track_command
async def stop(ctx):
    if ctx.voice_client is not None:
        await ctx.voice_client.disconnect()

# Commande pour ban un utilisateur
@bot.command(name="ban")
@track_command
async def ban(ctx, user: discord.Member, *, reason=None):
    if any(role.name == "Master" for role in user.roles):
        await user.ban(reason=reason)
        await ctx.send(f"{user} a été banni !")

#Token du bot
bot.run(TOKEN)
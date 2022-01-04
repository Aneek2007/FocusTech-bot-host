# # Importing modules
# from discord_components import *
# from discord_components import DiscordComponents as DiscordButtons
import asyncio
import json
from os import name
import random
from datetime import datetime, timedelta
import disnake as discord
from disnake import guild
from disnake import player
from disnake.embeds import Embed
from disnake.emoji import Emoji
from disnake.file import File
from disnake.partial_emoji import PartialEmoji
from disnake.ext import commands, tasks
from disnake.ext.commands import Context
from disnake.ext.commands.core import command
from disnake.guild import Guild
from disnake.member import Member
from disnake.message import Message
from functools import update_wrapper
from io import BytesIO, StringIO
from itertools import cycle
from itertools import cycle
from PIL import Image # Wait
import sys
for k, v in list(sys.modules.items()):
    if k.startswith("disnake"):
        sys.modules[k.replace("disnake", "discord")] = v
# third party discord modules after this line
from discord_components import *
from discord_slash import SlashCommand
import DiscordUtils

#wait i hv smtng
# Get_prefix command
def get_prefix(message: Message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    if message.guild.id not in prefixes:
        return next(iter(prefixes.values())) # default prefix
    return prefixes[str(message.guild.id)]
fake_message = type("m", (), {"guild": type("G", (), {"id": 0})()})()
intents = discord.Intents().all()
client = commands.Bot(command_prefix=get_prefix(fake_message), intents=intents)
slash = SlashCommand(client, sync_commands=True)
music = DiscordUtils.Music()
client.ticket_configs = {}
# Bot status
status = cycle([
    "Watching The Chill Zone",
    "Good times with The Chill Zone",
    "Having Fun!",
    ".help"
])
# Executing the loop for the bot's
@tasks.loop(seconds=10)
async def status_swap():
    await client.change_presence(activity=discord.Game(next(status)))
# On_ready function
@client.event
async def on_ready():
    

    print('FocusTech is good to go!')
    status_swap.start()
# Ping command
@client.command(aliases=['p'])
async def ping(ctx: Context):
    await ctx.send('Pong!')
# Setprefix command continued
@client.event
async def on_guild_join(guild: Guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(guild.id)] = 'c!'
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@client.event
async def on_guild_remove(guild: Guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes.pop(str(guild.id))
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

# 8ball command
@client.command(aliases=['8ball','8b'])
async def eightball(ctx: Context, *,question):
    responses = [
        'Hell no.',
        'Prolly not.',
        'Idk bro.',
        'Prolly.',
        'Hell yeah my dude.',
        'It is certain.',
        'It is decidedly so.',
        'Without a Doubt.',
        'Yes - Definitaly.',
        'You may rely on it.',
        'As i see it, Yes.',
        'Most Likely.',
        'Outlook Good.',
        'Yes!',
        'No!',
        'Signs a point to Yes!',
        'Reply Hazy, Try again.',
        'IDK but u should subscribe to Exotix On Youtube and Follow Him On Insta mahad.ali.khan.',
        'Better not tell you know.',
        'Cannot predict now.',
        'Concentrate and ask again.',
        "Don't Count on it.",
        'My reply is No.',
        'My sources say No.',
        'Outlook not so good.',
        'Very Doubtful']
    await ctx.send(f':8ball: Question: {question}\n:8ball: Answer: {random.choice(responses)}')

# Kick command
@client.command(aliases=['boot'])
async def kick(ctx: Context, member:discord.Member,*,reason=None):
    if (not ctx.author.guild_permissions.kick_members):
        await ctx.send('''You don't have permission to do so.''')
        return
    await member.kick(reason=reason)
    await ctx.send(f'''{member.mention} has been kicked.''')

# Ban command
@client.command(aliases=['hammer'])
async def ban(ctx: Context, member:discord.Member,*,reason=None):
    if (not ctx.author.guild_permissions.ban_members):
        await ctx.send('''You don't have permission to do so.''')
        return
    await member.ban(reason=reason)
    await ctx.send(f'''{member.mention} has been banned.''')

# Unban command
@client.command(aliases=['forgive'])
async def unban(ctx: Context, *,member: Member):
    banned_users =  await ctx.guild.bans()
    parts = member.split('#')
    member_name, member_discriminator = '', ''
    member_id = 0
    if len(parts) == 1:
        # Using the user ID e.g. 235148962103951360
        member_id = int(parts[0])
    else:
        member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user =  ban_entry.user

        if (
            user.id == member_id or
            (user.name, user.discriminator) == (member_name, member_discriminator)
        ):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return

# Purge command
@client.command(aliases=['purge', 'cc'])
async def clear(ctx: Context, amount=11):
    if (not ctx.author.guild_permissions.manage_messages):
        await ctx.send('''You don't have the permission to do so.''')
        return
    amount = amount+1
    if amount >101:
        await ctx.send('Can not delete more than 100 messages.')
    else:
        await ctx.channel.purge(limit=amount)
        await ctx.send('Cleared Messages')

# Executing setprefix command
@client.command(aliases=['prefix'])
async def setprefix(ctx: Context, prefixset=None):
    if (not ctx.author.guild_permissions.manage_channels):
        await ctx.send('''You don't have permission to do so.''')
        return
    if (prefixset == None):
        prefixset = '.'

    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(ctx.guild.id)] = prefixset

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
    client.command_prefix = prefixset
    await ctx.send(f'The bot prefix has been changed to {prefixset}')

# Mute command
@client.command()
async def mute(ctx: Context, member : discord.Member,*, reason=None):
    if (not ctx.author.guild_permissions.manage_messages):
        await ctx.send('''You don't have the permission to do so.''')
        return
    guild = ctx.guild
    muteRole = discord.utils.get(guild.roles, name = "Muted")

    if not muteRole:
        await ctx.send("No mute has been found, creating a mute role....")

        muteRole = await guild.create_role(name='Muted')

        for channel in guild.channels:
            await guild.set_permissions(muteRole, speak = False, send_messages = False, read_message_history = True, read_messages = True)
    await member.add_roles(muteRole, reason=reason)
    await ctx.send("User is muted.")
    await member.send(f"You have been muted from **{guild.name}** | Reason: **{reason}**")

#Unmute command
@client.command()
async def unmute(ctx: Context, member : discord.Member,*, reason=None):
    if (not ctx.author.guild_permissions.manage_messages):
        await ctx.send('''You don't have the permission to do so.''')
        return
    guild = ctx.guild
    muteRole = discord.utils.get(guild.roles, name = "Muted")

    if not muteRole:
        await ctx.send("No mute has been found.")
        return



    await member.remove_roles(muteRole, reason=reason)
    await ctx.send("User is unmuted.")
    await member.send(f"You have been unmuted from **{guild.name}** | Reason: **{reason}**")

# Error handling (8ball)
@eightball.error
async def eightball_error(ctx: Context, error):
    if error.__class__.__name__.startswith('MissingRequiredArgument'):
        await ctx.send("Please include a question.")

# Error handling (ban)
@ban.error
async def ban_error(ctx: Context, error):
    if error.__class__.__name__.startswith('MissingRequiredArgument'):
        await ctx.send("Please mention a member to ban.")

# Error handling (mute)
@mute.error
async def mute_error(ctx: Context, error):
    if error.__class__.__name__.startswith('MissingRequiredArgument'):
        await ctx.send("Please mention a member to mute.")

# Error handling (kick)
@kick.error
async def kick_error(ctx: Context, error):
    if error.__class__.__name__.startswith('MissingRequiredArgument'):
        await ctx.send("Please mention a member to kick.")

# slowmode command
@client.command()
async def slowmode(ctx: Context, time:int):
    if (not ctx.author.guild_permissions.manage_messages):
        await ctx.send('''You don't have the permission to do so.''')
        return
    try:
        if time == 0:
            await ctx.send("Slowmode Off")
            await ctx.channel.edit(slowmode_delay = 0)
        elif time > 21600:
            await ctx.send("You cannot set slowmode above 6 hours.")
        else:
            await ctx.channel.edit(slowmode_delay = time)
            await ctx.send(f"Slowmode set to {time} seconds!")
    except Exception:
        await print("Oops!")

# Say command
@client.command()
async def say(ctx: Context, saymssg=None):
    if saymssg==None:
        return await ctx.send("You must tell me something to say")
    await ctx.send(saymssg)

# Server information command
@client.command()
async def serverinfo(ctx: Context):
    guild = ctx.guild
    role_count = len(ctx.guild.roles)
    list_of_bots = [bot.mention for bot in ctx.guild.members if bot.bot]

    serverinfoEmbed = discord.Embed(title= f"{guild.name} info",timestamp=ctx.message.created_at, color=ctx.author.color, description=f"This is the official information of the {guild.name} server!",)
    serverinfoEmbed.set_thumbnail(url="https://media.discordapp.net/attachments/830411572408745995/926515169524318208/1640968826685.jpg?width=395&height=395")
    serverinfoEmbed.add_field(name = 'Name', value=f"{ctx.guild.name}", inline=False)
    serverinfoEmbed.add_field(name="Member Count", value=ctx.guild.member_count, inline=False)
    serverinfoEmbed.add_field(name="Verification Level", value=str(ctx.guild.verification_level), inline=False)
    serverinfoEmbed.add_field(name="Highest Role",value=ctx.guild.roles[-1].mention, inline=False)
    serverinfoEmbed.add_field(name="Bots", value=', '.join(list_of_bots), inline=False)

    await ctx.send(embed = serverinfoEmbed)

# Wanted command
@client.command()
async def wanted(ctx: Context, member : discord.Member = None):
    if member == None:
        member = ctx.author

    wanted = Image.open("poster_wanted.jpg")

    asset = member.avatar.with_size(128)
    data = BytesIO(await asset.read())
    profilepic = Image.open(data)
    profilepic = profilepic.resize((300, 300))

    wanted.paste(profilepic, (78, 219))

    wanted.save("wantedpic.jpg")
    await ctx.send(file = File("wantedpic.jpg"))

# Help command
class MyHelpCommand(commands.HelpCommand):
    async def command_callback(self, ctx: Context, *,command=None):
        if command:
           await ctx.send(f"This the help page for the command {command} ")
        else:
            helpEmbed = discord.Embed(title="FocusTech help here!", color = discord.Color.blue(), description = "Ready to help you anytime my freind")
            helpEmbed.add_field(name="**Fun**", value="`🔫 !wanted <mention member> - Shows wanted user.`\n `🔴 !ping - Replies you with a message.`\n `🗣️ !say - Repeats what you asked to say.`",inline=False)
            helpEmbed.add_field(name = "**Games**", value="`🎱 !8ball <Your question> - Plays 8ball with you.`", inline=False)
            helpEmbed.add_field(name="Music", value="`🎵 !play <url of the song> - Plays the song.`\n `🚪 !join - Joins the voice channel.`\n `📤 !leave - Leaves the voice channel.`", inline=False)
            helpEmbed.add_field(name="**Information**", value="`👨 !avatar <mention_member>- Shows the member's avatar.`\n `ℹ️ !serverinfo - Get the official server information.`\n `🧑 !whois <mention_member> - Gives the user information of the mentioned member.`\n `🎚️ !level <mention_member> - Shows the level of the member mentioned.`", inline=False)

            if (ctx.author.guild_permissions.manage_messages
            and ctx.author.guild_permissions.manage_channels):
                helpEmbed.add_field(name="**Moderation**" , value="`🔨 !ban <mention_member> - Bans the user mentioned.`\n `👼 !unban <member id> -  Unbans banned users mentioned.`\n `👢 !kick <mention member> - Kicks the user mentioned.`\n `🔇 !mute <mention member> - Mutes the user mentioned.`\n `🔈 !unmute <mention member> - Unmutes the user mentioned.`\n `❌ !clear <clear limit> -  Clear chats in the channel.`\n `❗ setprefix <your_prefix> - Sets the requested prefix.`\n `⏲️ !slowmode <time in seconds (10 s)> - Sets slowmode in the channel you typed in the command.`\n `🎉 !giveaway` - Starts giveaway.", inline=False)

            await ctx.send(embed = helpEmbed)
client.help_command=MyHelpCommand()

# User information command
@client.command()
async def whois(ctx: Context, member : discord.Member):
    roles = [role for role in member.roles]
    who_embed = discord.Embed(colour=member.color, timestamp = ctx.message.created_at)
    who_embed.set_author(name = f"User info - {member}")
    who_embed.set_thumbnail(url = member.avatar.url)
    who_embed.set_footer(text = f'Requested by - {ctx.author}')
    who_embed.add_field(name = 'ID', value = member.id),
    who_embed.add_field(name = 'Name', value = member.display_name)
    who_embed.add_field(name = 'Created at : ', value = fmtdate(member.created_at))
    who_embed.add_field(name = 'Joined at : ', value = fmtdate(member.joined_at))
    who_embed.add_field(name = 'Bot ?', value = yesno(member.bot))
    who_embed.add_field(name = f'Roles:({len(roles)})', value = " ".join([role.mention for role in roles]))
    who_embed.add_field(name = 'Top Role : ', value = member.top_role.mention)
    await ctx.send(embed=who_embed)

def fmtdate(date):
    return datetime.fromisoformat(str(date)).strftime("%A, %d %B %Y  %H:%m:%S IST")

def yesno(value):
  return "Yes" if value else "No"
# Avatar command
@client.command()
async def avatar(ctx: Context, member : discord.Member = None):
    if member == None:
        member = ctx.author

    memberAvatar = member.avatar_url

    avaEmbed = discord.Embed(title = f"{member.display_name}'s avatar")
    avaEmbed.set_image(url = memberAvatar)


    await ctx.send(embed = avaEmbed)

# Giveaway command
@client.command()
async def giveaway(ctx: Context):
    giveaway_questions = ['Which channel will i host the giveaway in?', 'What is the prize?', 'How long should the giveaway run for (in seconds)?', 'How many winners will be there?']
    giveaway_answers = []

    def check(m: Context):
        return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id
        
# question
# why did you have to add this check here? Was it matching the wrong 
# message?
# 
# Let's run the cmd first and btw what does disnake does?
# discord.py was unmaintaned remeber? disnake is the successor to it that has 
# compatibility and its actvely maintained ok u should use nextcord it's good too anyways let's run the bot and see what error it throws when we trigger giveaway cmd o kOK 
    channel = None
    for question in giveaway_questions:
        await ctx.send(question)
        try:
            message = await client.wait_for('message', timeout = 30.0, check = check)
        except asyncio.TimeoutError:
            await ctx.send('''You didn't answer in time. Please try again and be sure to send your answer within 30 seconds of the question being asked. ''')

            return
        else:
            giveaway_answers.append(message.content)
            if len(giveaway_answers) == 1:
                try:
                    c_id = int(giveaway_answers[0][2:-1])
                    if c_id <= 0:
                        raise ValueError
                    channel = client.get_channel(c_id)
                    if channel is None:
                        raise ValueError
                except:
                    await ctx.send(f"You failed to mention the channel correctly. Please do it like this : {ctx.channel.mention}")
                    return
            elif len(giveaway_answers) == 3:
                try:
                    time_amt, time_unit, *_ = (giveaway_answers[2] + " x x").split()
                    time_amt = int(time_amt)
                    if not time_unit or time_unit.lower().startswith("s"):
                        time = time_amt 
                    elif  time_unit.lower().startswith("m"):
                        time = time_amt * 60
                    elif time_unit.lower().startswith("h"):
                        time = time_amt * 3600
                except:
                    await ctx.send(f"You failed to give a valid duration for the giveaway. Please do it like this : '5 s', '10 m'")
                    return
    
    prize = str(giveaway_answers[1])
    winners = int(giveaway_answers[3])

    await ctx.send(f'The giveaway for {prize} will begin shortly.\n Please direct your attention to {channel.mention}, this giveaway will end in {time} seconds.')


    give = discord.Embed(color = 0x2ecc71)
    give.set_author(name = f'GIVEAWAY TIME!', icon_url = 'https://i.imgur.com/VaX0pfM.png')
    if time > 60:
        min, sec = divmod(time, 60)
        timedesc = f"{min} min {sec} seconds"
    else:
        timedesc = f"{time} seconds"
    give.add_field(name = f'{ctx.author.name} is giving away: {prize}!', value = f'React with :tada: to enter!\n Ends in {timedesc}!', inline = False)
    end = datetime.utcnow() + timedelta(seconds = time)
    give.set_footer(text = f'Giveaway ends at {fmtdate(end)} IST!')
    my_message = await channel.send(embed = give)

    await my_message.add_reaction("🎉")
    await asyncio.sleep(time)

    new_message = await channel.fetch_message(my_message.id)

    winner_count = winners
    for i in range(winner_count):

        users = await new_message.reactions[0].users().flatten()
        
        if not users: break
        users.pop(users.index(client.user))
        winner = random.choice(users)

        winning_announcement = discord.Embed(color = 0xff2424)
        winning_announcement.set_author(name = f'THE GIVEAWAY HAS ENDED!', icon_url= 'https://i.imgur.com/DDric14.png' )
        winning_announcement.add_field(name = f':tada: Prize: {prize}', value = f':partying_face: **Winner** : {winner.mention}\n:ticket:**Number of Entrants** : {len(users)}', inline = False)
        winning_announcement.set_footer(text = 'Thanks for entering!')
        await channel.send(embed = winning_announcement)


# Level cmd
@client.event
async def on_member_join(member):
    with open('users.json', 'r') as f:
        users = json.load(f)

        await update_data(users, member)

        with open('user.json','w') as f:
            json.dump(users, f, indent=4)

@client.event
async def on_message(message):
    if message.author.bot == False:
        with open('users.json', 'r') as f:
            try:
                users = json.load(f)
            except:
                users = {}
        await update_data(users, message.author)
        await add_experience(users, message.author, 5)
        await level_up(users, message.author, message)

        with open('users.json', 'w') as f:
            json.dump(users, f, indent=4)
    await client.process_commands(message)


async def update_data(users, user):
    if not f'{user.id}' in users:
        users[f'{user.id}'] = {}
        users[f'{user.id}']['experience'] = 0
        users[f'{user.id}']['level'] = 0
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=4)

async def add_experience(users, user, exp):
    await update_data(users, user)
    users[f'{user.id}'] = users.get(str(user.id), {})
    users[f'{user.id}']['experience'] += exp
    await update_data(users, user)

async def level_up(users, user, message):
    await update_data(users, user)
    experience = users[f'{user.id}']['experience']
    lvl_start = users[f'{user.id}']['level']
    users[f'{user.id}']['level'] = lvl_start
    lvl_end = int(experience ** (1/4))
    if lvl_start < lvl_end:
        await message.channel.send(f'{user.mention} has leveled up!! **LEVEL** - {lvl_end}')
        users[f'{user.id}']['level'] = lvl_end
    await update_data(users, user)


@client.command()
async def level(ctx , member : discord.Member = None):
    if not member:
        id = ctx.message.author.id
        with open('users.json', 'r') as f:
            users = json.load(f)
        lvl = users[str(id)]['level']
        await ctx.send(f'You are at *{lvl}!')
    else:
        id = member.id
    with open('users.json', 'r') as f:
        users = json.load(f)
    await update_data(users, member)
    lvl = users[str(id)]['level']
    await ctx.send(f'{member} is at {lvl}!')
@slash.slash(description="Shows the bot latency.")
async def ping(ctx: Context):
    await ctx.send(f'Bot Speed - {round(client.latency * 1000)}ms')



@client.command()
async def join(ctx : Context):
    voicetrue = ctx.author.voice
    if voicetrue is None:
        return await ctx.send("You are currently not on a voice channel")
    await ctx.author.voice.channel.connect()
    await ctx.send("Joined your voice channel.")

@client.command()
async def leave(ctx : Context):
    voicetrue = ctx.author.voice
    mevoicetrue = ctx.guild.me.voice
    if voicetrue is None:
        return await ctx.send("You are currently not on a voice channel")
    if mevoicetrue is None:
        return await ctx.send("I am currently not on a voice channel")
    await ctx.voice_client.disconnect()
    await ctx.send("Left your voice channel.")

@client.command()
async def play(ctx, *, url):
    player = music.get_player(guild_id=ctx.guild.id)
    if not player:
        player = music.create_player(ctx, ffmpeg_error_betterfix=True)
    if not ctx.voice_client.is_playing():
        await player.queue(url, search=True)
        song = await player.play()
        await ctx.send(f'I have started playing `{song.name}`')
    else:
        song = await player.queue(url, search=True)
        await ctx.send(f'{song.name} has been added to the playlist')

@client.command()
async def queue(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    nl = "\n"
    queueEmbed = discord.Embed(title = f'''Songs queue -:''', description="This is your song's queue.")
    queueEmbed.add_field(name="**Queue**",value= f"{nl.join([song.name for song in player.current_queue()])}")
    await ctx.send(embed = queueEmbed)
@client.command()
async def pause(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.pause()
    await ctx.send(f'Paused {song.name}')
@client.command()
async def resume(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.resume()
    await ctx.send(f'Resumed {song.name}')

@client.command()
async def loop(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.toggle_song_loop()
    if song.is_looping:
        return await ctx.send(f'{song.name} is looping!')
    else:
        return await ctx.send(f'{song.name} is not looping!')

@client.command()
async def nowplayer(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = player.now_playing()
    await ctx.send(song.name)

# @client.command()
# async def remove(ctx):
#     player = music.get_player(guild_id=ctx.guild.id)
#     song = await player.remove_from_queue(int(index))
#     await ctx.send(f'Removed {song.name} from queue')

# @client.command(name="selfrole")
# async def self_role(ctx):
#     await ctx.send("Answer These Question In Next 2Min!")

#     questions = ["Enter Message: ", "Enter Emojis: ", "Enter Roles: ", "Enter Channel: "]
#     answers = []

#     def check(user):
#         return user.author == ctx.author and user.channel == ctx.channel
    
#     for question in questions:
#         await ctx.send(question)

#         try:
#             msg = await client.wait_for('message', timeout=120.0, check=check)
#         except asyncio.TimeoutError:
#             await ctx.send("Type Faster Next Time!")
#             return
#         else:
#             answers.append(msg.content)

#     emojis = answers[1].split(" ")
#     roles = answers[2].split(" ")
#     c_id = int(answers[3][2:-1])
#     channel = client.get_channel(c_id)

#     bot_msg = await channel.send(answers[0])

#     with open("selfrole.json", "r") as f:
#         self_roles = json.load(f)

#     self_roles[str(bot_msg.id)] = {}
#     self_roles[str(bot_msg.id)]["emojis"] = emojis
#     self_roles[str(bot_msg.id)]["roles"] = roles

#     with open("selfrole.json", "w") as f:
#         json.dump(self_roles, f)

#     for emoji in emojis:
#         await bot_msg.add_reaction(emoji)

# @client.event
# async def on_raw_reaction_add(payload):
#     msg_id = payload.message_id

#     with open("selfrole.json", "r") as f:
#         self_roles = json.load(f)

#     if payload.member.bot:
#         return
    
#     if str(msg_id) in self_roles:
#         emojis = []
#         roles = []

#         for emoji in self_roles[str(msg_id)]['emojis']:
#             emojis.append(emoji)

#         for role in self_roles[str(msg_id)]['roles']:
#             roles.append(role)
        
#         guild = client.get_guild(payload.guild_id)

#         for i in range(len(emojis)):
#             choosed_emoji = str(payload.emoji)
#             if choosed_emoji == emojis[i]:
#                 selected_role = roles[i]

#                 role = discord.utils.get(guild.roles, name=selected_role)

#                 await payload.member.add_roles(role)
#                 await payload.member.send(f"You Got {selected_role} Role!")

# @client.event
# async def on_raw_reaction_remove(payload):
#     msg_id = payload.message_id

#     with open("selfrole.json", "r") as f:
#         self_roles = json.load(f)
    
#     if str(msg_id) in self_roles:
#         emojis = []
#         roles = []

#         for emoji in self_roles[str(msg_id)]['emojis']:
#             emojis.append(
#                 emoji)

#         for role in self_roles[str(msg_id)]['roles']:
#             roles.append(role)
        
#         guild = client.get_guild(payload.guild_id)

#         for i in range(len(emojis)):
#             choosed_emoji = str(payload.emoji)
#             if choosed_emoji == emojis[i]:
#                 selected_role = roles[i]

#                 role = discord.utils.get(guild.roles, name=selected_role)

#                 member = await(guild.fetch_member(payload.user_id))
#                 if member is not None:
#                     await member.remove_roles(role)


client.run('OTIyNTE5ODQ5MTAyNjI2ODE3.YcCpjw.nP0agxfAlo78-SFBfwvihszYr0o')



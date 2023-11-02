import discord
from discord.ext import commands
import token_manager

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.message_content = True  # Add this for command handling


TOKEN = token_manager.bot_token()


SERVER_ID = token_manager.server_token()


bot = commands.Bot(command_prefix='$', intents=intents)


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.event
async def on_member_join(member):
    # When a member joins, change their nickname
    new_nickname = format_username(member, member.display_name.split(" ")[0])
    try:
        await member.edit(nick=new_nickname)
        print(f'Changed nickname for {member.name} to {new_nickname}')
    except Exception as e:
        print(f'Failed to change nickname for {member.name}: {e}')

@bot.event
async def on_member_update(before, after):
    if before.guild.id == int(SERVER_ID):
        # Check if the nickname has changed
        if before.display_name != after.display_name:
            print(f'{before.name} changed their nickname from {before.nick} to {after.nick}')
            new_nickname = format_username(after, after.display_name.split(" ")[0])
            try:
                await after.edit(nick=new_nickname)
                print(f'Changed nickname for {after.name} to {new_nickname}')
            except Exception as e:
                print(f'Failed to change nickname for {after.name}: {e}')

@bot.command(name="test", brief="test")
async def test(cfx):
    await cfx.send("Hello")

@bot.command(name='join')
async def join_voice(ctx):
    # Check if the user is in a voice channel
    if ctx.author.voice is None:
        await ctx.send('You are not in a voice channel.')
        return

    # Join the user's voice channel
    channel = ctx.author.voice.channel
    voice_client = await channel.connect()

    # Send a message in the text channel
    await ctx.send(f'Joined voice channel: {channel.name}')

    # Play an audio message (you can replace this with your own audio file)
    audio_source = discord.FFmpegPCMAudio('audio_file.mp3')  # Replace 'audio_file.mp3' with your audio file
    voice_client.play(audio_source)

@bot.command(name='leave')
async def leave_voice(ctx):
    # Check if the bot is in a voice channel
    if ctx.voice_client is not None:
        # Leave the voice channel
        await ctx.voice_client.disconnect()
        await ctx.send('Left voice channel.')

def format_username(member, name: str = ""):
    if not name:
        name = member.display_name
    main_role = member.top_role.name

    if "|" in name:
        parts = name.split("|")
        username = parts[0].strip()
        return f'{username} | {main_role}'
    else:
        return f'{name} | {main_role}'


bot.run(TOKEN)

import asyncio

import discord
from discord.ext import commands
import token_manager
import os
import music_manager
from youtube_music import get_video_name

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
    if ctx.author.voice is None:
        await ctx.send('You are not in a voice channel.')
        return

    channel = ctx.author.voice.channel
    voice_client = await channel.connect()
    await ctx.send(f'Joined voice channel: {channel.name}')

@bot.command(name="lp")
async def show_pl(ctx, play_list_name: str):
    a = music_manager.list_pl(play_list_name)
    await ctx.send(a)

@bot.command(name="playpl")
async def play(ctx, playlist_name: str):
    music_manager.preload(playlist_name)
    mp3s = os.listdir("files/")

    for mp3 in mp3s:
        voice_client = ctx.voice_client
        m = os.path.join("files", mp3)
        source = discord.FFmpegPCMAudio(m)
        voice_client.play(source)
        while voice_client.is_playing():
            await asyncio.sleep(1)

@bot.command(name="newp")
async def new(ctx, playlist_name: str):
    if " " not in playlist_name:
        music_manager.create_playlist(playlist_name)
        await ctx.send(f"Created Playlist: {playlist_name}")
    else:
        await ctx.send("Playlists cannot contain spaces!")

@bot.command(name="addtop")
async def add(ctx, pn: str, sn: str):
    music_manager.add_song_to_playlist(pn, music_manager.get_song(sn))
    await ctx.send(f"Added {sn} to {pn}.")

@bot.command(name="rs")
async def rs(ctx, pn: str, si: str):
    si = int(si)
    music_manager.remove_song(pn, si)
    await ctx.send("Song removed from playlist.\nNew Playlist:")
    a = music_manager.list_pl(pn)
    await ctx.send(a)

@bot.command(name='leave')
async def leave_voice(ctx):
    # Check if the bot is in a voice channel
    if ctx.voice_client is not None:
        # Leave the voice channel
        await ctx.voice_client.disconnect()
        await ctx.send('Left voice channel.')

@bot.command(name="addtopurl")
async def add_via_url(ctx, pn: str, su: str):
    try:
        name = get_video_name(su)
        music_manager.add_song_to_pl_via_url(pn, su)
        await ctx.send(f"Song ('{name}') added to playlist: {pn}")
    except:
        await ctx.send("Invalid link.")

@bot.command(name="stop")
async def stop(ctx):
    await ctx.voice_client.stop()
    music_manager.clear_preload()

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

import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.message_content = True  # Add this for command handling


TOKEN = 'MTE2OTM3MDYxMjkzMDcyODAyOA.GhOxCk.hijCFJzsq1lGjtkCOr2HepTpKL5YMKys3zUMlQ'


SERVER_ID = '1166787640004186152'


bot = commands.Bot(command_prefix='/', intents=intents)


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

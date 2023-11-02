import discord
from discord.ext import commands

from bot import client

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.messages = True
intents.message_content = True


TOKEN = 'MTE2OTM3MDYxMjkzMDcyODAyOA.GhOxCk.hijCFJzsq1lGjtkCOr2HepTpKL5YMKys3zUMlQ'


SERVER_ID = '1166787640004186152'

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command(name='role-as-name', brief="Renames usernames to fit the member roles.")
async def on_ready():
    print(f'We have logged in as {client.user}')

    # Get the server by ID
    server = client.get_guild(int(SERVER_ID))

    # Check if the server exists
    if server:
        # Loop through all server members and change their username
        for member in server.members:
            try:
                new_username = format_username(member)
                await member.edit(nick=new_username)
                print(f'Changed username for {member.name} to {new_username}')
            except Exception as e:
                print(f'Failed to change username for {member.name}: {e}')

                try:
                    new_username = format_username(member, member.display_name.split(" ")[0])
                    await member.edit(nick=new_username)
                    print(f'Changed username for {member.name} to {new_username}')
                except Exception as e:
                    print(f'Failed to change username for {member.name}: {e}')
    else:
        print(f"Server with ID {SERVER_ID} not found.")

    input("\nPress enter to exit\n")
    exit()


def format_username(member, name: str = ""):
    # Use the member's nickname, or their username if they don't have a nickname
    if not name:
        name = member.display_name
    # Get the main role (highest role)
    main_role = member.top_role.name

    if main_role not in name:
        i = name.index("|")
        name = name[:i]
        while name[-1] == " ":
            name = name[:-1]
        return f'{name} | {main_role}'

    else:
        return name


client.run(TOKEN)

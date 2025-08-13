import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
token = os.getenv('DISCORD_TOKEN')

if not token:
    raise RuntimeError("DISCORD_TOKEN not found. Check your .env file.")

# Logging configuration
handler = logging.FileHandler(filename="discord.log", encoding='utf-8', mode='w')

# Intents setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Bot setup
bot = commands.Bot(command_prefix='*', intents=intents)

secret_role = "munnu"

@bot.event
async def on_ready():
    print(f"We are ready to go in, {bot.user.name}")

@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to the server {member.name}!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "shit" in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author.mention} - don't use that word!")

    # Process commands after handling messages
    await bot.process_commands(message)

# Correct decorator for commands
@bot.command()
async def hello(ctx):
    """Responds with a hello message."""
    await ctx.send(f"Hello {ctx.author.mention}!")


@bot.command()
async def assign(ctx):
    role = discord.utils.get(ctx.guild.roles, name=secret_role)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} is now assigned to {secret_role}")
    else:
        await ctx.send("Role doesn't exist")

    

@bot.command()
async def remove(ctx):
    role = discord.utils.get(ctx.guild.roles, name=secret_role)
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} has had the {secret_role} removed")
    else:
        await ctx.send("Role doesn't exist")



@bot.command()
async def dm(ctx, *, msg):
    await ctx.author.send(f"You said {msg}")




@bot.command()
async def reply(ctx):
    await ctx.reply("This is a reply to your msg!")   



@bot.command()
async def poll(ctx, *, question):
    embed = discord.Embed(title = "New Poll", description = question)
    poll_message = await ctx.send(embed = embed)
    
    await poll_message.add_reaction("👍")
    await poll_message.add_reaction("👎")






@bot.command()
@commands.has_role(secret_role)
async def secret(ctx):
    await ctx.send(f"Welcome to the club!")
    
@secret.error
async def secret_error(ctx, error):
    if isinstance(error, commands.MissingRole):
     await ctx.send(f"You do not have the following permission, sorry!!")





# Run bot
bot.run(token, log_handler=handler, log_level=logging.DEBUG)

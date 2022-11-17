# Import pycord to acces the discord api
import discord
from discord import option

# Import the os module to access the environment variables
import os

# Import the dotenv module to access the .env file
from dotenv import load_dotenv
load_dotenv()

# Get the token from the .env file
TOKEN = os.getenv('DISCORD_TOKEN')
DEBUG_GUILD = os.getenv('DEBUG_GUILD')

# Import mcstatus to access the minecraft server information
import mcstatus

# Import motd cleaner from utils.py
from src.utils import motd_cleaner

# Set "bot" to the discord client
bot = discord.Bot(debug_guilds=[DEBUG_GUILD])

# When the bot is ready, print a message to the console, count the guilds and print the number of guilds
@bot.event
async def on_ready():
	print('We have logged in as {0.user}'.format(bot))
	guild_count = 0
	for guild in bot.guilds:
		print(f"- {guild.id} (name: {guild.name})")
		guild_count = guild_count + 1
	print("MSPB is in " + str(guild_count) + " guilds.")

# When a message is sent, check if it is a command, if it is, run the command, if not, send an error message
# @bot.event
# async def on_command_error(ctx, error):
# 	if isinstance(error, discord.ext.commands.errors.CommandNotFound):
# 		await ctx.send("That's not a command!! Usage: ***?ping <serveradress or IP>***")
# 	if isinstance(error, commands.CommandOnCooldown):
# 		await ctx.send("You have to wait another %.2f seconds before doing this again!" % error.retry_after)
# 	if isinstance(error, discord.ext.commands.errors.CommandInvokeError):
# 		await ctx.send(":x: Couldn't reach the server, maybe he's offline?")

# When the help command is called send an embed with some basic information about the bot


# When the ping command is called send an embed with some basic server information
@bot.slash_command(name="ping", description="Ping a server and get some basic information about it")
@option("version", description="Choose the version of the server", choices=["Java", "Bedrock"])
async def ping(ctx, serveradress: str, version: str):
	if version == "Java":
		server = mcstatus.JavaServer.lookup(serveradress)
		status = server.status()
		embed = discord.Embed(title="Server ping", description="We pinged **{0}** for you!".format(serveradress), color=0x0090FF)
		embed.add_field(name="Latency", value="{0} ms".format(int(status.latency)))
		embed.add_field(name="Players", value="{0}/{1}".format(status.players.online, status.players.max))
		embed.set_thumbnail(url="https://eu.mc-api.net/v3/server/favicon/{0}".format(serveradress))
		embed.set_footer(text="Consider voting for our bot on top.gg!", icon_url="https://i.ibb.co/pXQc66y/MSPB.png")
		await ctx.respond(embed=embed)
	else:
		server = mcstatus.BedrockServer.lookup(serveradress)
		status = server.status()
		embed = discord.Embed(title="Server ping", description="We pinged **{0}** for you!".format(serveradress), color=0x0090FF)
		embed.add_field(name="Latency", value="{0} ms".format(int(status.latency)))
		embed.add_field(name="Players", value="{0}/{1}".format(status.players_online, status.players_max))
		embed.set_thumbnail(url="https://eu.mc-api.net/v3/server/favicon/{0}".format(serveradress))
		embed.set_footer(text="Consider voting for our bot on top.gg!", icon_url="https://i.ibb.co/pXQc66y/MSPB.png")
		await ctx.respond(embed=embed)

# When the status command is called send an embed with detailed server information
@bot.slash_command(name="status", description="Ping a server and get a detailed report about it")
@option("version", description="Choose the version of the server", choices=["Java", "Bedrock"])
async def status(ctx, serveradress: str, version: str):
	if version == "Java":
		server = mcstatus.JavaServer.lookup(serveradress)
		status = server.status()
		embed = discord.Embed(title="Server status", description="Full status of **{0}**".format(serveradress), color=0x0090FF)
		embed.add_field(name="Latency", value="The server replied in ***{0}*** ms".format(int(status.latency)))
		embed.add_field(name="Online players", value="There are currently ***{0}*** players online".format(status.players.online))
		embed.add_field(name="Max players", value="The maximum player count of this server is ***{0}***".format(status.players.max))
		embed.add_field(name="Version", value="{0} v{1}".format(status.version.name, status.version.protocol))
		embed.add_field(name="Description", value="{0}".format(motd_cleaner(status.description)))
		embed.set_thumbnail(url="https://eu.mc-api.net/v3/server/favicon/{0}".format(serveradress))
		embed.set_footer(text="Consider voting for our bot on top.gg!", icon_url="https://i.ibb.co/pXQc66y/MSPB.png")
		await ctx.respond(embed=embed)
	else:
		server = mcstatus.BedrockServer.lookup(serveradress)
		status = server.status()
		embed = discord.Embed(title="Server status", description="Full status of **{0}**".format(serveradress), color=0x0090FF)
		embed.add_field(name="Latency", value="The server replied in ***{0}*** ms".format(int(status.latency)))
		embed.add_field(name="Online players", value="There are currently ***{0}*** players online".format(status.players_online))
		embed.add_field(name="Max players", value="The maximum player count of this server is ***{0}***".format(status.players_max))
		embed.add_field(name="Version", value="{0} v{1}".format(status.version.version, status.version.protocol))
		embed.add_field(name="Description", value="{0}".format(motd_cleaner(status.motd)))
		embed.set_thumbnail(url="https://eu.mc-api.net/v3/server/favicon/{0}".format(serveradress))
		embed.set_footer(text="Consider voting for our bot on top.gg!", icon_url="https://i.ibb.co/pXQc66y/MSPB.png")
		await ctx.respond(embed=embed)

bot.run(TOKEN)
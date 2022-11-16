# IMPORT DISCORD.PY. ALLOWS ACCESS TO DISCORD'S API.
import discord

# IMPORT THE OS MODULE.
import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

from discord.ext import commands

from mcstatus import MinecraftServer

# GETS THE CLIENT OBJECT FROM DISCORD.PY. CLIENT IS SYNONYMOUS WITH BOT.
bot = discord.Client()

bot = commands.Bot(command_prefix='?')

@bot.event
async def on_ready():
  print('We have logged in as {0.user}'.format(bot))
  guild_count = 0
  for guild in bot.guilds:
	  print(f"- {guild.id} (name: {guild.name})")
	  guild_count = guild_count + 1
  print("MSPB is in " + str(guild_count) + " guilds.")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await ctx.send("That's not a command!! Usage: ***?ping <serveradress or IP>***")
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("You have to wait another %.2f seconds before doing this again!" % error.retry_after)
    if isinstance(error, discord.ext.commands.errors.CommandInvokeError):
        await ctx.send(":x: Couldn't reach the server, maybe he's offline?")

@bot.command(name="ping", help="?ping <servername of IP>")
async def ping(ctx, server_name):
    server = MinecraftServer.lookup(server_name)
    status = server.status()
    embed = discord.Embed(title="Server ping", description="We pinged **{0}** for you!".format(server_name), color=0x0090FF)
    embed.add_field(name="Latency", value="{0} ms".format(status.latency))
    embed.add_field(name="Players", value="{0}/{1}".format(status.players.online, status.players.max))
    embed.set_thumbnail(url="https://eu.mc-api.net/v3/server/favicon/{0}".format(server_name))
    embed.set_footer(text="Consider voting for our bot on top.gg!", icon_url="https://i.ibb.co/pXQc66y/MSPB.png")
    await ctx.channel.send(embed=embed)

@bot.command(name="status", help="?status <servername of IP>")
async def status(ctx, server_name):
    server = MinecraftServer.lookup(server_name)
    status = server.status()
    embed = discord.Embed(title="Server status", description="Full status of **{0}**".format(server_name), color=0x0090FF)
    embed.add_field(name="Latency", value="The server replied in ***{0}*** ms".format(status.latency))
    embed.add_field(name="Online players", value="There are currently ***{0}*** players online".format(status.players.online))
    embed.add_field(name="Max players", value="The maximum player count of this server is ***{0}***".format(status.players.max))
    embed.add_field(name="Version", value="{0} v{1}".format(status.version.name, status.version.protocol))
    embed.add_field(name="Description", value="{0}".format(status.description))
    embed.set_thumbnail(url="https://eu.mc-api.net/v3/server/favicon/{0}".format(server_name))
    embed.set_footer(text="Consider voting for our bot on top.gg!", icon_url="https://i.ibb.co/pXQc66y/MSPB.png")
    await ctx.channel.send(embed=embed)

bot.run(TOKEN)
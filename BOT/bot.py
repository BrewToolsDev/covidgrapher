import os, sys, json, time, logging, traceback
import logging.handlers
import asyncio
import aiohttp

import discord
from discord.ext import commands

from covidgrapher import make_covid_graph

aboutstring = """
covidgrapher_discord
By the BrewTools Discord
https://brewtools.dev/
Script Licensed under GPLv3
A python discord bot for producing covid graph data.
Uses matplotlib, PIL and Discord Py
Covid Data provided by covidtracking.com
API data licensed under Creative Commons CC BY 4.0.
This program should not be used for anything critical."""

YES_VALUES = ["Y", "YES", "TRUE"]

valid_graph_keys = [
	"postitiveIncrease",
	"negativeIncrease",
	"hospitalizedCurrently",
	"inIcuCurrently",
	"onVentilatorCurrently",
	"totalTestResultsIncrease",
	"deathIncrease",
	"hospitalizedIncrease"
]

script_name = os.path.basename(__file__).split('.')[0]

log_file_name = f"{script_name}.log"

# Limit of discord (non-nitro) is 8MB (not MiB)
max_file_size = 1000 * 1000 * 8
backup_count = 3
file_handler = logging.handlers.RotatingFileHandler(
	filename=log_file_name, maxBytes=max_file_size, backupCount=backup_count)
stdout_handler = logging.StreamHandler(sys.stdout)

log_format = logging.Formatter(
	'[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s')
file_handler.setFormatter(log_format)
stdout_handler.setFormatter(log_format)

log = logging.getLogger('discord_covid')
log.setLevel(logging.INFO)
log.addHandler(file_handler)
log.addHandler(stdout_handler)

bot = commands.Bot(command_prefix="c.", description="The covid bot", pm_help=False)

bot.log = log
bot.loop = asyncio.get_event_loop()
bot.script_name = script_name
bot.make_covid_graph = None

@bot.event
async def on_ready():
	aioh = {"User-Agent": f"{script_name}/1.0'"}
	bot.aiosession = aiohttp.ClientSession(headers=aioh)
	bot.app_info = await bot.application_info()

	log.info(f'\nLogged in as: {bot.user.name} - '
			 f'{bot.user.id}\ndpy version: {discord.__version__}\n')
 
	activity = discord.Activity(name="c.help",type=discord.ActivityType.listening)
	await bot.change_presence(activity=activity)

@bot.event
async def on_command(ctx):
	log_text = f"{ctx.message.author} ({ctx.message.author.id}): "\
			   f"\"{ctx.message.content}\" "
	log.info(log_text)

@bot.event
async def on_error(event_method, *args, **kwargs):
	log.error(f"Error on {event_method}: {sys.exc_info()}")

@bot.event
async def on_command_error(ctx, error):
	error_text = str(error)
	err_msg = f"Command error - {ctx.message.content} - {type(error)} - {error_text}"
	log.error(err_msg)
	if isinstance(error, commands.BotMissingPermissions):
		roles_needed = '\n-'.join(error.missing_perms)
		return await ctx.send(f"{ctx.author.mention}: Bot Missing Permissions:```{roles_needed}```")
	elif isinstance(error, commands.CommandNotFound):
		return # do nothing if command isn't found
	cmd = ctx.prefix + ctx.command.signature
	help_text = f"Command Usage is: `{cmd}`. See {ctx.prefix}help {ctx.command.name}"
	if isinstance(error, commands.BadArgument):
		return await ctx.send(f"{ctx.author.mention}: Bad Arguments\n{help_text}"
							  f"arguments. {help_text}")
	elif isinstance(error, commands.MissingRequiredArgument):
		return await ctx.send(f"{ctx.author.mention}: Incomplete Arguments.\n{help_text}")

@bot.command(name = 'about')
async def about(ctx):
	await ctx.message.channel.send(aboutstring)

@bot.command(name = 'ping')
async def ping(ctx):
	"""Calculate round-trip ping (No arguments)"""
	before = time.monotonic()
	tmp = await ctx.send('Calculating ping...')
	after = time.monotonic()
	rtt_ms = (after - before) * 1000
	gw_ms = bot.latency * 1000
	message_text = f":ping_pong:\n"\
				   f"rtt: `{rtt_ms:.1f}ms`\n"\
				   f"gw: `{gw_ms:.1f}ms`"
	bot.log.info(message_text)
	await tmp.edit(content=message_text)

@bot.command(name = "graph")
async def graph(ctx = None, data_key: str = "positiveIncrease", smooth: str = "True", regions: str ="US"):
	tmp = await ctx.send('Getting graph, please wait.')
	try:
		"""Creates a covid graph. USAGE: data key (list with .keys), apply 7-day smooth (TRUE/FALSE), and region codes (more than one must be wrapped in quotes).\nExamplse:\n\t.graph inIcuCurrently FALSE US\n\t.graph inIcuCurrently TRUE "CA NY OH"\n"""
		if smooth.upper() in YES_VALUES:
			smooth = True
		else: smooth = False
		regions = regions.split(" ")
		await tmp.edit(content = f'Getting graph, please wait.\n\t`Graph args: regions - {regions}, smooth - {smooth}, data_key - {data_key}`')
		if bot.client: img = bot.make_covid_graph(bot.api_url, regions = regions, smooth = smooth, datakey = data_key)
		else: img = bot.make_covid_graph(regions = regions, smooth = smooth, datakey = data_key)
		await tmp.delete()
		await ctx.message.channel.send(file = discord.File(img))
	except Exception as e:
		await tmp.edit(content = f"Error making graph - {e}")
	
@bot.command(name = "keys")
async def keys(ctx = None,):
	"""Lists valid keys to plot with 'graph' (No arguments)"""
	msg = "Valid key values to plot include - " + json.dumps(valid_graph_keys, indent=4)
	await ctx.message.channel.send(msg)

@bot.event
async def on_message(message):
	if message.author.bot:
		return
	ctx = await bot.get_context(message)
	await bot.invoke(ctx)

if __name__ == "__main__":
	bot.run(TOKEN, bot=True, reconnect=True)
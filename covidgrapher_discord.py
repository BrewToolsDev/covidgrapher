import os, argparse
from BOT.bot import bot, YES_VALUES
from covidgrapher import download_file, cache_folder, make_covid_graph, get_covid_graph_from_api

try:
	from config import discord_token as TOKEN
except:
	print("Failed to get discord_token from config.py file. Script will be unable to run if it is not passed as an arg.")

intro = f"""
Welcome to Covid Stat Grapher Discord - US
By Andrew Spangler
Licensed under GPLv3
A tool to visualize covid data.
Covid Data provided by covidtracking.com
Api data licensed under Creative Commons CC BY 4.0.
Run with -h for options."""

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description=intro)
	clienthelp = """Runs the script in client mode which downloads the graphs from an api host rather than generating them locally.
This argument must be passed an api url to download the graphs from.
You can host your own api with covidgrapher_flask.py, if you are hosting the api on the same machine 
as this script you can usually connect with covidgrapher.py -c 127.0.0.1:5000/"""
	parser.add_argument("-c", "--client", required = False, help = clienthelp)
	parser.add_argument("--token", required = False, help = "Discord API token. Set this if running without config.py")
	args = parser.parse_args()
	bot.client = bool(args.client)
	bot.api_url = args.client if bot.client else None
	if bot.client: bot.make_covid_graph = get_covid_graph_from_api
	else: bot.make_covid_graph = make_covid_graph
	try: TOKEN
	except:
		TOKEN = args.token
		if not TOKEN:
			raise ValueError("Discord token not in config and not passed as arg.")
		
	bot.run(TOKEN, bot=True, reconnect=True)
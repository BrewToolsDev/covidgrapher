from aiohttp import web
from discord.ext import commands, tasks
import discord
import os, io, time
import aiohttp
from PIL import Image
from SITE.easy_html_generator import build_page, make_html_table_from_dict
from SITE.dynamic_page_code import COVIDFORMSCRIPT, COVIDFORM, HOMEPAGE, STYLE

from aiohttp_wsgi import WSGIHandler
app = web.Application()
wsgi_handler = WSGIHandler(app)
routes = web.RouteTableDef()

def setup(bot):
	bot.add_cog(Webserver(bot))

def html_file_response(file):
	with open (file) as f:
		c = f.read()
	return web.Response(text=c, content_type='text/html')

def get_bot_stats_html(bot):
	name = bot.user.name
	uid = bot.user.id
	discord_py_version = discord.__version__
	bot_version = bot.version
	bot.user.avatar_url
	numservers = len(bot.guilds)

	entries = {
		"Bot User Name" : name,
		"Bot User ID" : uid,
		"Bot Version" : bot_version,
		"Discord.py Version" : discord_py_version,
		"Server Count" : numservers,
	}

	return "<h1>Covid Grapher Discord Bot Stats</h1>" + make_html_table_from_dict(entries)

class Webserver(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.web_server.start()

		@routes.get('/')
		async def welcome(request):
			page = build_page("Covid Grapher Bot Home Page", HOMEPAGE, STYLE)
			return web.Response(text=page, content_type='text/html')

		@routes.get('/bot')
		@routes.get('/bot/')
		async def bot_stats(request):
			bot_stats_text = get_bot_stats_html(bot)
			page = build_page("Bot Statistics", bot_stats_text, STYLE)
			return web.Response(text = page, content_type='text/html')

		@routes.get('/log')
		@routes.get('/log/')
		async def read_log(request):
			with open ("bot.log") as log:
				l = log.read()
			logstring = "<h1>Covid Grapher Bot Log</h1>"
			for l in reversed(l.splitlines()):
				logstring += f"<p class='logline'>{l}</p>"

			page = build_page("Covid Grapher Bot Log", logstring, STYLE)
			return web.Response(text = page, content_type='text/html')

		@routes.get('/form')
		@routes.get('/form/')
		async def get_form(request):
			page = build_page("Covid Grapher API Web Form", COVIDFORM, STYLE, COVIDFORMSCRIPT)
			return web.Response(text = page, content_type='text/html')

		@routes.get("/graph")
		@routes.get("/graph/")
		async def graph(request):
			def make_graph():
				try:
					region = request.rel_url.query['region']
				except:
					region = "US"
				if region:
					region = region.split(" ")
					region = [r.upper() for r in region]
				else: region = ["US"]
				try:
					key = request.rel_url.query['key'] or "positiveIncrease"
				except:
					key = "positiveIncrease"
				try:
					s = request.rel_url.query['smooth']
				except:
					s = "TRUE"
				if s:
					if s.upper() == "TRUE": smooth = True
					elif s.upper() == "FALSE": smooth = False
					else: raise TypeError("Invalid smooth value passed, must be 'True' or 'False' (no quotes)")
				else: smooth = True
				
				print(region, smooth, key)
				if self.bot.client:
					img = self.bot.make_covid_graph(self.bot.api_url, regions = region, smooth = smooth, filename = None, datakey = key, show = False)
				else:
					img = self.bot.make_covid_graph(regions = region, smooth = smooth, filename = None, datakey = key, show = False)
				im = io.BytesIO()
				Image.open(img).save(im, format = "PNG")
				return web.Response(body=im.getvalue(), content_type="image/jpeg")
			return make_graph()

		self.webserver_port = os.environ.get('PORT', 5000)
		app.add_routes(routes)
		print("Init webserver")

	@tasks.loop()
	async def web_server(self):
		runner = web.AppRunner(app)
		await runner.setup()
		site = web.TCPSite(runner, host='127.0.0.1', port=self.webserver_port)
		await site.start()

	@web_server.before_loop
	async def web_server_before_loop(self):
		await self.bot.wait_until_ready()

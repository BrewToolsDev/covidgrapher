from covidgrapher import make_covid_graph, get_covid_graph_from_api
from GUI.controller import Controller
import argparse

intro = f"""
Welcome to Covid Stat Grapher Discord - US
By Andrew Spangler
Licensed under GPLv3
A tool to visualize covid data.
Covid Data provided by covidtracking.com
Api data licensed under Creative Commons CC BY 4.0.
Run with -h for options."""

VERSION = "V 0.3"

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description=intro)
	clienthelp = f"""Runs the script in client mode which downloads the graphs from an api host rather than generating them locally using data from covidtracking.com".
This argument must be passed an api url to download the graphs from.
You can host your own api with covidgrapher_flask.py, if you are hosting the api on the same machine 
as this script you can usually connect with {__file__} -c 127.0.0.1:5000/"""
	parser.add_argument("-c", "--client", required = False, help = clienthelp)
	args = parser.parse_args()
	client = bool(args.client)
	api_url = args.client if client else None
	graph_function = get_covid_graph_from_api if client else make_covid_graph
	if client: print(f"Running in Client mode with api at {api_url}. Graphs will be generated remotely.")
	else: print(f"Running in Local mode. Graphe will be generated locally.")
	app = Controller(VERSION, graph_function, client = client, api_url = api_url, devmode = False)
	app.start_mainloop() #Call tk mainloop
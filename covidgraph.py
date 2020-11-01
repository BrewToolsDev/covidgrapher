#covidgrapher.py
#Copyright 2020, Andrew Spangler, All rights reserved.


import urllib.request, json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import argparse
from statistics import mean
from sys import exit
import os

opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
urllib.request.install_opener(opener)

years = mdates.YearLocator()
months = mdates.MonthLocator()
years_fmt = mdates.DateFormatter('%Y')
months_fmt = mdates.DateFormatter('%m')

separator_string = "--------------------------------"

REGIONS = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
		  "GU", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
		  "MP", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
		  "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "PR", "RI", "SC", 
		  "SD", "TN", "TX", "UT", "VT", "VA", "VI", "WA", "WV", "WI", "WY"]

YES_VALUES = ["Y", "YES"]
NO_VALUES = ["N", "NO"]
YES_NO_VALUES = []
YES_NO_VALUES.extend(YES_VALUES)
YES_NO_VALUES.extend(NO_VALUES)

def get_input(text, output_list = None):
	output_list = [o.lower() for o in output_list]
	while True:
		res = input(text + " ")
		if output_list:
			if res.lower() in output_list: return res
			else: continue
		if res: return res

def get_yes_no(text):
	res = get_input(text, YES_NO_VALUES)
	if res.upper() in YES_VALUES: return True
	return False

def get_options(title, options):
	j = 0
	while True:
		print(title)
		for o in options:
			print("\t" + f"{j}) " + o)
			j += 1
		i = input("\n\t>: ")
		try:
			i = int(i)
			break
		except:
			j = 0 #If a non integer was passed
			print(separator_string)
			continue
	print(separator_string)
	return i

def yield_n_items_of_list(l,n): 
	for i in range(0, len(l), n): yield l[i:i+n]

def smooth_increases(increases_list):
	vals = []
	new_vals = []
	right = 0
	while True: 
		vals.append(increases_list[right])
		if len(vals) > 7: vals.pop(0)
		new_vals.append(int(mean(vals)))
		right += 1
		if right == len(increases_list):
			return new_vals

def clean_dates(dates):
	newdates = []
	for d in dates:
		y, m, day = d[0:4], d[4:6], d[6:8]
		newdates.append(mdates.datestr2num(f"{m}/{day}/{y}"))
	return newdates

intro = f"""{separator_string}
Welcome to Covid Stat Graph - US
By Andrew Spangler
Licensed under GPLv3
A tool to visualize covid data.
Covid Data provided by covidtracking.com
Api data licensed under Creative Commons CC BY 4.0.
Run with -h for options.
{separator_string}"""

helpme = "Covid Stat Graph by Andrew Spangler - GPLv3 - API under Creative Commons CC BY 4.0"

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description=helpme)
	parser.add_argument("-i", "--interactive", action = "store_true", help = "Interactive command line mode, if passed, all other arguments will be ignored.")
	parser.add_argument("-o", "--output", required = False, help = "Outputs graph to passed filename if specified.")
	parser.add_argument("-r", "--region", required = False, help = "Region of graph, defaults to entire US if not specified. Run the tool in interactive mode to list regions.")
	parser.add_argument("-s", "--smooth", action = "store_true", help = "Applies a 7-Day rolling average to daily increases to account for weekly reporting spikes if specified.")
	args = parser.parse_args()
	print(intro)

	if args.interactive: #If in interactive mode
		outputs = [
			"Pyplot Window",
			"Image",	
		]
		while True:
			output = get_options("Output Type:", outputs)
			if type(output) is int and output < len(outputs):
				if output: #If writing to a file
					filename = None
					while not filename:
						filename = input("Save file path:\n\t>: ")
						print(separator_string)
				break

		smooth = get_yes_no("Apply a 7-Day rolling average to account for weekly reporting spikes?\n\t>:")
		print(separator_string)

		localities = [
			"Whole US",
			"State",
		]
		while True:
			locality_type = get_options("Locality Type:", localities)
			if type(locality_type) is int and locality_type < len(localities):
				break

		if locality_type: #Only need to get state if it's not a full US graph
			while True:
				region = input("Enter 2-Letter State or Region Code (R to list):\n\t>: ")
				if region:
					region = region.upper()
					if region == "R":
						print("Printing Region List -")
						for sts in yield_n_items_of_list(REGIONS, 10):
							print("\t", sts)
					elif region in REGIONS:
						print(separator_string)
						break
				print(separator_string)
		else: region = "US"

	else: #If in args-based cli
		output = bool(args.output)
		filename = args.output or "output_graph.png"
		filename = os.path.abspath(filename)
		locality_type = bool(args.region)
		region = args.region
		if region:
			region = region.upper()
			if not region in REGIONS:
				exit("Invalid region.")
		else: region = "US"
		smooth = args.smooth

	#Get data from api
	if locality_type: apiaddr = f"https://api.covidtracking.com/v1/states/{region}/daily.json"
	else: apiaddr = 'https://api.covidtracking.com/v1/US/daily.json'
	print(f"Getting api data at {apiaddr}")
	data = json.loads(urllib.request.urlopen(apiaddr).read())
	#Parse dates and increases
	dates = [v for v in reversed([str(d["date"]) for d in data])]
	increases = [v for v in [int(d["positiveIncrease"]) for d in data]]
	#Smooth graph if specified
	if smooth:
		print("Applying smooth.")
		increases = smooth_increases(increases)
	increases = [v for v in reversed(increases)]
	dates = clean_dates(dates) #Make dates friendly for matplotlob
	print("Making graph.")
	plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
	plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
	plt.plot(dates, increases)
	plt.gcf().autofmt_xdate() #Makes dates look nice
	plt.title(f"Daily New Covid Cases - 7 Day Rolling Average - {region}")
	plt.ylabel("Daily New Cases")

	if output:
		print(f"Saving graph to {filename}")
		plt.savefig(filename) #Save to file
	else:
		print("Showing graph.")
		plt.show() #Show Graph
#covidgrapher.py Copyright 2020, Andrew Spangler, All rights reserved.

separator_string = "--------------------------------"
intro = f"""{separator_string}
Welcome to Covid Stat Grapher - US
By Andrew Spangler
Licensed under GPLv3
A tool to visualize covid data.
Covid Data provided by covidtracking.com
Api data licensed under Creative Commons CC BY 4.0.
Run with -h for options.
{separator_string}"""
helpme = "Covid Stat Grapher by Andrew Spangler - GPLv3 - API under Creative Commons CC BY 4.0"

import os, sys, json, shutil, argparse, subprocess, urllib.request
from statistics import mean
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import use

use('Agg') #Prevents graphs from failing on flask / threads

opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
urllib.request.install_opener(opener)

years = mdates.YearLocator()
months = mdates.MonthLocator()
years_fmt = mdates.DateFormatter('%Y')
months_fmt = mdates.DateFormatter('%m')

APIADDR = 'https://api.covidtracking.com/v1/US/daily.json'
APIREG = "https://api.covidtracking.com/v1/states/{}/daily.json"

REGIONS = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
		  "GU", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
		  "MP", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
		  "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "PR", "RI", "SC", 
		  "SD", "TN", "TX", "US", "UT", "VT", "VA", "VI", "WA", "WV", "WI",
		  "WY"]

DATA_OPTIONS = [
	"New Cases",
	"Hospitalized",
	"In ICU",
	"On Ventilator",
	"Confirmed Deaths",
]

DATA_OPTIONS_MAP = {
	"New Cases": "positiveIncrease",
	"On Ventilator": "onVentilatorCurrently",
	"Hospitalized": "hospitalizedCurrently",
	"In ICU": "inIcuCurrently",
	"Confirmed Deaths": "deathIncrease",
}
REVERSED_DATA_OPTIONS_MAP = {}
for v in DATA_OPTIONS_MAP: REVERSED_DATA_OPTIONS_MAP[DATA_OPTIONS_MAP[v]]=v

DIR = os.path.abspath(os.path.dirname(__file__))
cache_folder = os.path.join(DIR, "cache")
json_folder = os.path.join(cache_folder, "json")
if not os.path.isdir(json_folder): os.makedirs(json_folder, exist_ok = True)

def open_image_by_path(path):
    cli_image = {
    	'win32':'explorer',
    	'linux':'xdg-open',
  		'darwin':'open'
  	}
    subprocess.run([cli_image[sys.platform], path])

"""CACHING-----------------"""
ETAGFILE = "cache/json/etags.json"
etag_header = "If-None-Match" #Header for checking if etag is updated
useragent = 'Mozilla/5.0'
def download_file(url, file):
	# try:
	req = urllib.request.Request(url)
	with urllib.request.urlopen(req) as response, open(file, 'wb+') as out_file:
		shutil.copyfileobj(response, out_file)
		print("file {} - Dowloaded".format(file))
	return(file)
	# except Exception as e:
	# 	return f"Failed to download file - {file} - {e}"

def accessETaggedFile(url, file):
	req = urllib.request.Request(url)
	req.add_header('User-Agent', useragent)
	etag = getEtag(file)
	if etag: req.add_header(etag_header, "{}".format(etag))
	try:
		with urllib.request.urlopen(req) as response, open(file, 'wb+') as out_file:
			shutil.copyfileobj(response, out_file)
			headers = response.info()
			newetag = headers["ETag"]
			setEtag(file,newetag)
		print("file {} - Updated".format(file))
	except urllib.error.URLError as e:
		if e.reason == "Not Modified": #304 error, what we want to see if nothing has been updated
			print("file {} - {}".format(file, e.reason))
		else:  
			print("etag download error - {} - {}\n\n".format(file, e.reason))
			return None
	return(file)

def setEtag(tag, etag):
	if not os.path.isfile(ETAGFILE):
		print("No ETag file, initializing")
		with open(ETAGFILE, 'w+', encoding="utf-8") as jfile: 
			newfile = {"created_by" : __file__}
			json.dump(newfile, jfile, indent=4,)
	newentry = {tag : etag}
	with open(ETAGFILE, 'r', encoding="utf-8") as jfile:  
		originaljfile = json.load(jfile)
	originaljfile.update(newentry)
	with open(ETAGFILE, 'w', encoding="utf-8") as jfile:
		json.dump(originaljfile, jfile, indent=4,)

def getEtag(tag):
	try:
		with open(ETAGFILE, 'r', encoding="utf-8") as json_file:  
			jfile = json.load(json_file)
		try: etag = jfile[tag]
		except: etag = None
	except: etag = None
	return etag

#Super simple caching system, items all use a unique name and end up in /cache/json
#Uses etagging to reduce unnecessary load on the server
def getJson(distinctname, apiurl):
	try:
		jsonfile = os.path.join("cache/json", distinctname + ".json")
		jfile = accessETaggedFile(apiurl,jsonfile)
		return jfile
	except Exception as e:
		return print("{}\nfailed to download json file for {}".format(e, distinctname))
"""ENDCACHING-----------------"""

"""PARSING-----------------"""
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

def parse_json_data(data, smooth, datakey = None):
	datakey = datakey if datakey else "positiveIncrease"
	dates = [v for v in reversed([str(d["date"]) for d in data])]
	
	increases = [(v if v else 0) for v in [d[datakey] for d in data]]

	if smooth:
		print("Applying smooth.")
		increases = smooth_increases(increases)
	increases = [v for v in reversed(increases)]
	dates = clean_dates(dates) #Make dates friendly for matplotlob
	return dates, increases
"""ENDPARSING-----------------"""


"""GRAPHING-----------------"""
def make_US_graph(smooth = True, datakey = None):
	apiaddr = APIADDR
	print(f"Getting api data at {apiaddr}")
	with open(getJson("US", apiaddr)) as f:
		data = json.loads(f.read())
	dates, increases = parse_json_data(data, smooth, datakey)
	plt.plot(dates, increases, label = "US")

def plot_regional_graph(region, smooth = True, datakey = None):
	print(f"Plotting - {region}")
	if region == "US": return make_US_graph()
	apiaddr = APIREG.format(region)
	print(f"Getting api data at {apiaddr}")
	with open(getJson(region, apiaddr)) as f:
		data = json.loads(f.read())
	dates, increases = parse_json_data(data, smooth, datakey)
	plt.plot(dates, increases, label=region)

def make_covid_graph(regions = None, smooth = True, filename = None, datakey = "positiveIncrease", show = False):
	xa = plt.gca().xaxis
	xa.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
	xa.set_major_locator(mdates.MonthLocator())
	print("Making graph.")
	if regions == "US" or regions == ["US"] or not regions:
		regions = ["US"]
		make_US_graph(smooth, datakey)
	else:
		for r in regions: plot_regional_graph(r, smooth, datakey)
	plt.gcf().autofmt_xdate() #Makes dates look nice
	try: typestring = REVERSED_DATA_OPTIONS_MAP[datakey]
	except: typestring = datakey
	title = "Covid19 - "
	title += typestring
	if smooth: title += f" - 7 Day Rolling Average"
	if len(regions) == 1:
		title += " - " + regions[0]
	else:
		title += "\n"
		i = 1
		lr = len(regions)
		for r in regions:
			title += r
			if not i == lr: title +=", "
			if not i % 15: title += "\n"
			i += 1
	plt.title(title)
	plt.ylabel(typestring)
	plt.legend(mode="expand", frameon = False, ncol = 7, loc = "upper left")
	plt.tight_layout()
	if filename:
		print(f"Saving graph to {filename}")
	else: filename = os.path.join(cache_folder, "lastimage.png")
	plt.savefig(filename, format = "png", dpi = 150)
	if show: open_image_by_path(filename)
	plt.clf()
	return filename

"""ENDGRAPHING-----------------"""

#Client method to access images hosted by covidgrapher_flask.py
def get_covid_graph_from_api(api_url, regions = ["US"], smooth = True, filename = None, datakey = "positiveIncrease", show = False):
	if type(regions) is str:
		regions = [regions]		
	smooth = str(bool(smooth)).upper()
	if not api_url.endswith("/"): api_url += "/"
	geturl = api_url + f"graph/?smooth={smooth}"
	if regions:
		if len(regions) > 1:
			outstr = ""
			for r in regions:
				outstr += r.upper()
				if not regions.index(r) == len(regions) - 1:
					outstr += "+"
			geturl += f"&region={outstr}"
		else:
			r = regions[0].upper()
			geturl += f"&region={r}"
	if datakey:
		geturl += f"&key={datakey}"
	print(f"Downloading - {geturl}")
	filename = filename or os.path.join(cache_folder, "last_graph.png")
	f = download_file(geturl, filename)
	print(f,filename)
	if show: open_image_by_path(filename)
	return f

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description=helpme)
	clienthelp = """Runs the script in client mode. This argument must be passed an api url to download the graphs from.
You can host your own api with covidgrapher_flask.py, if you are hosting the api on the same machine 
as this script you can usually connect with covidgrapher.py -c 127.0.0.1:5000/"""
	parser.add_argument("-o", "--output", required = False, help = "Outputs graph to passed filename if specified, if not graph will be opened in the system default file viewer.")
	parser.add_argument("-r", "--region", required = False, help = "Region of graph, defaults to entire US if not specified. Pass multiple regions as a string separated by spaces eg 'US CA WA OR'")
	parser.add_argument("-c", "--client", required = False, help = clienthelp)
	parser.add_argument("-s", "--smooth", action = "store_true", help = "Applies a 7-Day rolling average to account for weekly reporting spikes if specified.")
	parser.add_argument("-k", "--key", help = "Key value to graph. Defaults to 'positiveIncrease.' Valid keys can be found in the README.")
	args = parser.parse_args()
	filename = os.path.abspath(args.output) if args.output else None
	
	if not args.region: regions = ["US"]
	else:
		regions = [r.upper() for r in args.region.split(" ")]
		for r in regions:
			if not r in REGIONS: sys.exit("Invalid region.")

	datakey = args.key or "positiveIncrease"
	show = False if filename else True

	if args.client:
		print("Getting from api")
		graph = get_covid_graph_from_api(args.client, regions, args.smooth, filename = filename, datakey = datakey, show = show)
	else: graph = make_covid_graph(regions, args.smooth, filename = filename, datakey = datakey, show = show)
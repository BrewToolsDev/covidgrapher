import time, argparse
from covidgrapher import make_covid_graph, get_covid_graph_from_api, REGIONS
import tweepy
try:
	from config import twitter_api_key
except:
	print("Failed to get twitter_api_key from config.py file. Script will be unable to run if it is not passed as an arg.")
try:
	from config import twitter_api_secret_key
except:
	print("Failed to get twitter_api_secret_key from config.py file. Script will be unable to run if it is not passed as an arg.")
try:
	from config import twitter_access_token
except:
	print("Failed to get twitter_access_token from config.py file. Script will be unable to run if it is not passed as an arg.")
try:
	from config import twitter_access_token_secret
except:
	print("Failed to get twitter_access_token_secret from config.py file. Script will be unable to run if it is not passed as an arg.")

helpme = "Covid Stat Grapher by Andrew Spangler - GPLv3 - API under Creative Commons CC BY 4.0"

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description=helpme)
	clienthelp = f"""Runs the script in client mode which downloads the graphs from an api host rather than generating them locally using data from covidtracking.com".
This argument must be passed an api url to download the graphs from.
You can host your own api with covidgrapher_flask.py, if you are hosting the api on the same machine 
as this script you can usually connect with {__file__} -c 127.0.0.1:5000/"""
	parser.add_argument("-d", "--delay",  required = False, type=int, help = "Post interval in minutes, by default 1440 (one day).")
	parser.add_argument("-r", "--region", required = False, help = "Region of graph, defaults to entire US if not specified. Pass multiple regions as a string separated by spaces eg 'US CA WA OR'")
	parser.add_argument("-c", "--client", required = False, help = clienthelp)
	parser.add_argument("-s", "--smooth", action = "store_true", help = "Applies a 7-Day rolling average to account for weekly reporting spikes if specified.")
	parser.add_argument("-k", "--key", help = "Data key value to graph. Defaults to 'positiveIncrease.' Valid keys can be found in the README.")
	parser.add_argument("--api_key", required = False, help = "Twitter API key. Set this if running without config.py")
	parser.add_argument("--api_secret_key", required = False, help = "Twitter API secret key. Set this if running without config.py")
	parser.add_argument("--access_token", required = False, help = "Twitter access token. Set this if running without config.py")
	parser.add_argument("--access_token_secret", required = False, help = "Twitter access token secret. Defaults to 'positiveIncrease.' Valid keys can be found in the README.")

	args = parser.parse_args()
	delay = args.delay * 60 if args.delay else 60 * 60 * 24 #Number of minutes or one day if not specified
	if not delay:raise ValueError("Invalid Post Interval.")

	#If the key doesn't exist yet
	try: twitter_api_key
	except:
		twitter_api_key = args.api_key
		if not twitter_api_key:
			raise ValueError("API key not in config and not passed as arg.")
	try: twitter_api_secret_key
	except:
		twitter_api_secret_key = args.api_secret_key
		if not twitter_api_secret_key:
			raise ValueError("API secret key not in config and not passed as arg.")
	try: twitter_access_token
	except:
		twitter_access_token = args.access_token
		if not twitter_access_token:
			raise ValueError("Access token not in config and not passed as arg.")
	try: twitter_access_token_secret
	except:
		twitter_access_token_secret = args.access_token_secret
		if not twitter_access_token_secret:
			raise ValueError("Access token secret not in config and not passed as arg.")
		
	if not args.region: regions = ["US"]
	else:
		regions = [r.upper() for r in args.region.split(" ")]
		for r in regions:
			if not r in REGIONS: sys.exit("Invalid region.")

	datakey = args.key or "positiveIncrease"

	auth = tweepy.OAuthHandler(twitter_api_key, twitter_api_secret_key)
	auth.set_access_token(twitter_access_token, twitter_access_token_secret)

	api = tweepy.API(auth)
	api.verify_credentials()
	print("Authentication OK")

	while True:
		if args.client:
			print("Getting from api")
			graph = get_covid_graph_from_api(args.client, regions, args.smooth, filename = None, datakey = datakey, show = False)
		else: graph = make_covid_graph(regions, args.smooth, filename = None, datakey = datakey, show = False)
		api.update_with_media(graph, status="")
		print("Posted graph.")
		print(f"Sleeping {delay/60} minutes")
		time.sleep(delay)
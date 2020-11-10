[![License](https://img.shields.io/badge/License-GPLv3-blue.svg)]()

# covidgrapher
A python tool for producing covid graph data, with a variety of interfaces.
Uses matplotlib, PIL, Tkinter, Flask, and tweepy.
Has basic examples of usage with Discord and Twitter.

Covid Data provided by covidtracking.com

API data licensed under Creative Commons CC BY 4.0.

##### Output
<p align="center"><img src="https://raw.githubusercontent.com/BrewToolsDev/covidgrapher/main/docu/example.png"></p>

##### Graphical Interface
<p align="center"><img src="https://raw.githubusercontent.com/BrewToolsDev/covidgrapher/main/docu/example_gui.png"></p>

#### Requirements:
		Works on: macOS, Windows, Linux
		Python 3.6 or greater
		Dependencies vary by OS, GUI has additional requirements, see below.

## Installation:

Download the lastest version of covidgrapher.zip from [covidgrapher latest](https://www.github.com/BrewToolsDev/covidgrapher/releases/latest)

#### CLI / ALL:

This step must be completed for any portion of the project to work.

- Windows:
	- Extract covidgrapher.zip to the location you intend to run it from.
	- Install [python](https://www.python.org/downloads/release/python-373/)
		- You *must* restart your pc after installing python.
		- If you do a custom installation remember to add python to the path, include pip, and (if you wish to use the GUI) install tcl/tk
	- In a command prompt navigate to the dir you extracted the app to run `pip install -r requirements.txt`
- Linux:
	- Extract covidgrapher.zip to the location you wish to run it from.
	- In a command prompt navigate to the dir you extracted the app to:
		- Install python and pip based on distro:
			- Ubuntu/Debian: `sudo apt install python3 python3-pip`
			- Manjaro/Arch: `sudo pacman -S python3 python-pip`
		- Run `pip3 install -r requirements.txt` to install dependencies
- MacOS:
	- Extract covidgrapher.zip to the location you intend to run it from.
	- Install [python](https://www.python.org/downloads/release/python-373/)
	  - If you do a custom installation remember to install tcl/tk, add python to the path, and include pip
	- In a command prompt navigate to the dir you extracted the app to and run `pip3 install -r requirements.txt`

#### GUI:

- Windows:
	- In a command prompt navigate to the dir you extracted the app to run `pip install -r requirements_gui.txt`
	- If the script fails with errors about tkinter not being found, reinstall python and make sure the 'install tc/tk' box is ticked
- Linux:
	- In a command prompt navigate to the dir you extracted the app to and run `pip3 install -r requirements_gui.txt`
		- Run `pip install -r requirements_gui.txt`
		- Then based on your distro do the following
		- Ubuntu/Debian: `sudo apt install python3-tk python3-pil.imagetk`
			- Manjaro/Arch: `sudo pacman -S tk python-pillow`
- MacOS:
	- In a command prompt navigate to the dir you extracted the app to and run `pip3 install -r requirements_gui.txt`
	- Sometimes MacOS ships with a borken version of Tkinter, you may have to reinstall python to fix it.

#### Flask API:
- All platforms:
	- In a command prompt navigate to the dir you extracted the app to run `pip install -r requirements_flask.txt`

#### Twitter Poster:
- All platforms:
	- In a command prompt navigate to the dir you extracted the app to run `pip install -r requirements_twitter.txt`

#### Discord Bot:
- All platforms:
	- In a command prompt navigate to the dir you extracted the app to run `pip install -r requirements_discord.txt`

## Usage:

#### CLI:
```
	usage: covidgrapher.py [-h] [-o OUTPUT] [-r REGION] [-s] [-k]
	optional arguments:
		-h, --help            show this help message and exit
		-o OUTPUT, --output OUTPUT
													Outputs graph to passed filename if specified, if not graph will be displayed in a matplotlib window.
		-r REGION, --region REGION
													Region of graph, defaults to entire US if not specified. Pass multiple regions as a string separated by spaces eg "US CA WA OR"
		-s, --smooth          Applies a 7-Day rolling average to account for weekly reporting spikes if specified.
		-k, --key             Key value to graph. Defaults to 'positiveIncrease.' Valid keys can be found in the README.
```
##### Valid keys to graph include:
- postitiveIncrease (default)
- negativeIncrease
- hospitalizedCurrently
- inIcuCurrently
- onVentilatorCurrently
- totalTestResultsIncrease
- deathIncrease
- hospitalizedIncrease

View raw json cached in /cache/json for full list of keys.
This program comes with a tiny script called make_cached_json_readable.py that will format the cached json to be human readable. Simply run it, then open a cached json file in the text viewer or editor of your choice.

#### GUI:
```
usage: covidgrapher_gui.py [-h] [-c CLIENT]
optional arguments:
  -h, --help            show this help message and exit
  -c CLIENT, --client CLIENT
                        Runs the script in client mode which downloads the graphs from an api host rather than generating them locally using data from covidtracking.com". This argument must be passed an api url to download the graphs
                        from. You can host your own api with covidgrapher_flask.py, if you are hosting the api on the same machine as this script you can usually connect with covidgrapher_gui.py -c 127.0.0.1:5000/
```
- Running:
	- Client Mode: Run with `-c api.your_domain.url` to use a remote source of graph images.
	- Windows:
		- In Command Prompt navigate to the folder you extracted the zip to and run `python.exe covidgrapher_gui.py`
		- Aternatively double-click the included `gui.bat` file in File Explorer.
	- Macintosh:
		- In Terminal navigate to the folder you extracted the zip to and run `python covidgrapher_gui.py`
		- Aternatively double-click `covidgrapher_gui.py` in Finder.
	- Linux:
		- In a terminal navigate to the folder you extracted the zip to and run `python3 covidgrapher_gui.py`
		- Alternatively double-click the included `gui.sh` file in a file browser.
- Usage:
	- By default the GUI graphs just total US results, you will need to untick the "Whole US" checkbox to select individual regions.
	- Select and deselect regions in the scrolling listbox by clicking and clicking again.
	- Click the 'Build Graph' button to generate a graph. Click it again with new options to generate a new one. 

#### Discord Bot:
```
	usage: covidgrapher_discord.py [-h] [-c CLIENT] [--token TOKEN]
	optional arguments:
	  -h, --help            show this help message and exit
	  -c CLIENT, --client CLIENT
	                        Runs the script in client mode which downloads the graphs from an api host rather than generating them locally. This argument must be passed an api url to download the graphs from. You
	                        can host your own api with covidgrapher_flask.py, if you are hosting the api on the same machine as this script you can usually connect with covidgrapher.py -c 127.0.0.1:5000/
	  --token TOKEN         Discord API token. Set this if running without config.py
```
The discord bot requires a bot token to work. See [Getting Bot Token](https://www.writebots.com/discord-bot-token/)
You must create a file in the same directory as the script called 'config.py' and add the line `discord_token = "XYZ"` where XYZ is the token.
The bot will need 'Send Messages' and 'Read Message History' permissions.
You must then invite the bot to your server (also detailed in the Bot Token link above)
- Running
	- Client Mode: Run with `-c api.your_domain.url` to use a remote source of graph images.
	- Windows
		- run `python.exe covidgrapher_discord.py`
	- Linux
		- run `python3 covidgrapher_discord.py`
	- MacOS
		- run `python covidgrapher_discord.py`
- Usage
	- Type `c.help` in a discord server with the bot to receive a help message and a list of valid commands.
	- To get a graph use `c.graph [data_key=positiveIncrease] [smooth=True] [regions=US]`
		- Examples:
		- c.graph positiveIncrease TRUE US
		- c.graph inIcuCurrently TRUE "CA WA OR ID"

#### Twitter Poster:
```
	usage: covidgrapher_twitter.py [-h] [-d DELAY] [-r REGION] [-c CLIENT] [-s] [-k KEY] [--api_key API_KEY] [--api_secret_key API_SECRET_KEY] [--access_token ACCESS_TOKEN] [--access_token_secret ACCESS_TOKEN_SECRET]
	optional arguments:
	  -h, --help            show this help message and exit
	  -d DELAY, --delay DELAY
	                        Post interval in minutes, by default 1440 (one day).
	  -r REGION, --region REGION
	                        Region of graph, defaults to entire US if not specified. Pass multiple regions as a string separated by spaces eg 'US CA WA OR'
	  -c CLIENT, --client CLIENT
	                        Runs the script in client mode which downloads the graphs from an api host rather than generating them locally using data from covidtracking.com". This argument must be passed an api
	                        url to download the graphs from. You can host your own api with covidgrapher_flask.py, if you are hosting the api on the same machine as this script you can usually connect with
	                        covidgrapher_twitter.py -c 127.0.0.1:5000/
	  -s, --smooth          Applies a 7-Day rolling average to account for weekly reporting spikes if specified.
	  -k KEY, --key KEY     Data key value to graph. Defaults to 'positiveIncrease.' Valid keys can be found in the README.
	  --api_key API_KEY     Twitter API key. Set this if running without config.py
	  --api_secret_key API_SECRET_KEY
	                        Twitter API secret key. Set this if running without config.py
	  --access_token ACCESS_TOKEN
	                        Twitter access token. Set this if running without config.py
	  --access_token_secret ACCESS_TOKEN_SECRET
	                        Twitter access token secret. Defaults to 'positiveIncrease.' Valid keys can be found in the README.
```
This is a very basic twitter posting script, more of a proof of concept than anything.
you will have to get a Twitter developer account and create a file in the same directory as the script called 
`config.py` and add the lines below, filling in the keys you need with values from your Twitter developer account.
```
twitter_api_key = "X"
twitter_api_secret_key = "X"
twitter_access_token = "X"
twitter_access_token_secret = "X"
```
- Running
	- Client Mode: Run with `-c api.your_domain.url` to use a remote source of graph images.
	- Windows
		- run `python.exe covidgrapher_discord.py`
	- Linux
		- run `python3 covidgrapher_discord.py`
	- MacOS
		- run `python covidgrapher_discord.py`
- Usage
	- The usage for this script is basically the same as the normal covidgrapher.py script.
	- There is an additional -d argument that specifies how frequently a new graph is posted.
	- 

#### Flask API:
This program comes with a Flask-based API server for distributing graphs to multiple clients on the same localhost.
The same script can be used to set a web api on common web hosting services like namecheap.

- Setup:
	- For use on a localhost:
		- Windows
			- run `python.exe covidgrapher_flask.py`
		- Linux
			- run `python3 covidgrapher_flask.py`
		- MacOS
			- run `python covidgrapher_flask.py`
	- This should start a a flask server at 127.0.0.1:5000
	- To use the localhost server with the other scripts launch them with the 'client' argument like `covidgrapher_gui.py -c 'https://127.0.0.1:5000/'`
- API Usage:
	The url-based api takes the following arguments:
	- region=(region or regions separated by '+') US if not specified
	- key=(key from list above) positiveIncrease if not specified
	- smooth=(False to turn off 7-day smoothing) True if not specified
	- Example: https://127.0.0.1:5000/graph/?region=CA+WA&key=positiveIncrease&smooth=True

## Disclaimer:
This program should not be used for anything critical. By using this program you agree not to hold me liable for any loss or injury that may occur.
```
IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING
WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MODIFIES AND/OR CONVEYS
THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES, INCLUDING ANY
GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE
USE OR INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED TO LOSS OF
DATA OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY YOU OR THIRD
PARTIES OR A FAILURE OF THE PROGRAM TO OPERATE WITH ANY OTHER PROGRAMS),
EVEN IF SUCH HOLDER OR OTHER PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF
SUCH DAMAGES.
```
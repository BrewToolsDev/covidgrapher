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

##### CLI / ALL:

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

##### GUI:

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

##### Flask API:
- All platforms:
	- In a command prompt navigate to the dir you extracted the app to run `pip install -r requirements_flask.txt`

##### Twitter Poster:
- All platforms:
	- In a command prompt navigate to the dir you extracted the app to run `pip install -r requirements_twitter.txt`

##### Discord Bot:
- All platforms:
	- In a command prompt navigate to the dir you extracted the app to run `pip install -r requirements_discord.txt`

## Usage:

##### CLI:
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
###### Valid keys to graph include:
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

##### GUI:
The GUI scripts do not take any arguments.
There are two very similar gui scripts, `covidgrapher_gui.py` and `covidgrapher_client_gui.py` 
The former generates graphs using data from covidtracking.com while the latter fetches graphs from api.brewtools.dev/covid/graph/ which uses the same graph generation code as a backend.

- Windows:
	- In Command Prompt navigate to the folder you extracted the zip to and run `python.exe covidgrapher_gui.py`
	- Aternatively double-click the included `gui.bat` file in File Explorer.
- Macintosh:
	- In Terminal navigate to the folder you extracted the zip to and run `python covidgrapher_gui.py`
	- Aternatively double-click `covidgrapher_gui.py` in Finder.
- Linux:
	- In a terminal navigate to the folder you extracted the zip to and run `python3 covidgrapher_gui.py`
	- Alternatively double-click the included `gui.sh` file in a file browser.

##### Flask API:
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

### Disclaimer:
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
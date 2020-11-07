[![License](https://img.shields.io/badge/License-GPLv3-blue.svg)]()

# covidgrapher
A python tool for producing covid graph data, with both command line and graphical interface.
Uses numpy, matplotlib, PIL and Tkinter

##### Output
<p align="center"><img src="https://raw.githubusercontent.com/BrewToolsDev/covidgrapher/main/example.png"></p>

##### Graphical Interface
<p align="center"><img src="https://raw.githubusercontent.com/BrewToolsDev/covidgrapher/main/example_gui.png"></p>

#### Requirements:
    Works on: macOS, Windows, Linux
    Python 3.6 or greater
    Dependencies vary by OS, GUI has additional requirements, see below.

## Installation:

Download the lastest version of covidgrapher.zip from [covidgrapher latest](https://www.github.com/BrewToolsDev/covidgrapher/releases/latest)

#### Windows:
- Extract covidgrapher.zip to the location you intend to run it from.
- Install [python](https://www.python.org/downloads/release/python-373/)
  - You *must* restart your pc after installing python.
  - If you do a custom installation remember to install tcl/tk, add python to the path, and include pip
- In a command prompt navigate to the dir you extracted the app to and run `pip install -r requirements.txt` to install dependencies
  - If you intend to use the GUI run `pip install -r requirements_gui.txt` at this time.

#### Macintosh:
- Extract covidgrapher.zip to the location you intend to run it from.
- Install [python](https://www.python.org/downloads/release/python-373/)
  - If you do a custom installation remember to install tcl/tk, add python to the path, and include pip
- In a command prompt navigate to the dir you extracted the app to and run `pip3 install -r requirements.txt` to install dependencies
  - If you intend to use the GUI run `pip install -r requirements_gui.txt` at this time.

#### Linux:
- Extract covidgrapher.zip to the location you wish to run it from.
- In a command prompt navigate to the dir you extracted the app to:
  - Install python and pip based on distro:
  	- Ubuntu/Debian: `sudo apt install python3 python3-pip`
    - Manjaro/Arch: `sudo pacman -S python3 python-pip`
  - Run `pip3 install -r requirements.txt` to install dependencies
  - If you intend to use the GUI:
  	- Run `pip install -r requirements_gui.txt`
    - Then based on your distro do the following
	  - Ubuntu/Debian: `sudo apt install python3-tk python3-pil.imagetk`
      - Manjaro/Arch: `sudo pacman -S tk python-pillow`

## Usage:

### CLI:
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

### GUI:
The GUI script does not take any arguments.

#### Windows:
- In Command Prompt navigate to the folder you extracted the zip to and run `python.exe covidgrapher_gui.py`
- Aternatively double-click the included `gui.bat` file in File Explorer.

#### Macintosh:
- In Terminal navigate to the folder you extracted the zip to and run `python covidgrapher_gui.py`
- Aternatively double-click `covidgrapher_gui.py` in Finder.

#### Linux:
- In Terminal / Shell navigate to the folder you extracted the zip to and run `python3 covidgrapher_gui.py`
- Alternatively double-click the included `gui.sh` file in a file browser.

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
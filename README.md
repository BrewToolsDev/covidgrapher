# covidgrapher
A python cli tool for producing covid graph data.

Pass -i for an interactive CLI

## Usage:
```
usage: covidgraph.py [-h] [-i] [-o OUTPUT] [-r REGION] [-s]
optional arguments:
  -h, --help            show this help message and exit
  -i, --interactive     Interactive command line mode, if passed, all other arguments will be ignored.
  -o OUTPUT, --output OUTPUT
                        Outputs graph to passed filename if specified.
  -r REGION, --region REGION
                        Region of graph, defaults to entire US if not specified. Run the tool in interactive mode to list regions.
  -s, --smooth          Applies a 7-Day rolling average to daily increases to account for weekly reporting spikes if specified.
```

<p align="center"><img src="https://raw.githubusercontent.com/BrewToolsDev/covidgrapher/primary/example.png"></p>

Disclaimer: This program should not be used for anything critical. By using this program you agree not to hold me liable for any loss or injury that may occur.
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
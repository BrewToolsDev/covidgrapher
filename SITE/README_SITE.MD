[![License](https://img.shields.io/badge/License-GPLv3-blue.svg)]()
[![API License](https://img.shields.io/badge/API%20License-Creative%20Commons%20CC%20BY%204.0-blue
)]()
[![Language](https://img.shields.io/badge/Language-Python-green
)]()

# covidgrapherflask

A python-based web api for producing covid graph data.
Uses matplotlib, and flask

Backend licensed under GPLv3

Covid Data provided by covidtracking.com

API data licensed under Creative Commons CC BY 4.0.

## Usage:
The url-based api takes the following arguments:
api.brewtools.dev/covid/graph/?
 - region=(region or regions separated by '+') US if not specified
 - key=(key from list below) positiveIncrease if not specified
 - smooth=(False to turn off 7-day smoothing) True if not specified

#### Example:
[https://api.brewtools.dev/covid/graph/?region=CA+WA&key=positiveIncrease&smooth=True](https://api.brewtools.dev/covid/graph/?region=CA+WA&key=positiveIncrease&smooth=True)


#### Valid keys to graph include:
- postitiveIncrease (default)
- negativeIncrease
- hospitalizedCurrently
- inIcuCurrently
- onVentilatorCurrently
- totalTestResultsIncrease
- deathIncrease
- hospitalizedIncrease

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
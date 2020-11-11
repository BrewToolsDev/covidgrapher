INTRO = """<!DOCTYPE html>
<html>
    <head>
    	<meta name="viewport" charset="utf-8" content="width=device-width, initial-scale=1">"""
TITLE = """
		<title>{}</title>"""
STYLE = """
		<style>\n{}\n		</style>"""
POSTSTYLE = """
	</head>
	<body>
		<div class="topnav">
			<a href="/")'>Home Page</a>
			<a href="/form">Graph API Web Form</a>
			<a href="/log">Application Log</a>
			<a href="https://covidtracking.com/">The COVID Tracking Project</a>
		</div>
		<div class= "mainbody">
"""
FOOTER = """
			<code>
			IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING
			WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MODIFIES AND/OR CONVEYS
			THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES, INCLUDING ANY
			GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE
			USE OR INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED TO LOSS OF
			DATA OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY YOU OR THIRD
			PARTIES OR A FAILURE OF THE PROGRAM TO OPERATE WITH ANY OTHER PROGRAMS),
			EVEN IF SUCH HOLDER OR OTHER PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF
			SUCH DAMAGES.
			</code>
	   	</div>
    </body>"""
SCRIPT = """
	<script>\n{}\n	</script>"""
END = "</html>"


def build_page(title, body = "", style = "",script = ""):
	page = ""
	page += INTRO
	page += TITLE.format(title)
	if style:
		stylestring = ""
		for s in style.splitlines():
			stylestring += f"\t\t\t{s}\n"
		page += STYLE.format(stylestring)
	page += POSTSTYLE
	page += body
	page += FOOTER
	if script:
		page += SCRIPT.format(script)
	page += END
	return page


tablestart = """
<div class="centeredtable">
	<table>"""
tableentry = """
		<tr>
			<th>{}</th>
			<td>{}</td>
		</tr>"""
tableend = """
	</table>
</div>"""

def make_html_table_from_dict(tbldict):
	outstr = tablestart
	for e in tbldict:
		outstr += tableentry.format(e, tbldict[e])
	return outstr + tableend
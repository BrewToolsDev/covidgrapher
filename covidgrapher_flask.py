import os, time, logging, multiprocessing, traceback
from flask import Flask, request, send_file

from covidgrapher import make_covid_graph

def getHTMLErrorString(title, error):
	return f"{title}<br/>{error}"
 
app = Flask(__name__)
t = time.ctime()
print(f"Started at {t}")

DIR = os.path.abspath(os.path.dirname(__file__))
logfile = os.path.join(DIR, __file__.split(".")[0] + ".log")

def log_decor(method):
	def apply(*args, **kw):
		try:
			t = time.ctime()
			name = method.__name__
			outstr = f"Method '{name}' at {t}"
			print(outstr)
			start = time.time()
			result = method(*args, **kw)
			end = time.time()
			outstr = 'Method - {} took {} ms'.format(method.__name__, "%2.2f" % ((end - start) * 1000))
			print(outstr)
			return result
		except Exception as e:
			title = f"Error running {method.__name__} with args {args} and kwargs {kw}"
			string = traceback.format_exc()
			print(title, string)
			return getHTMLErrorString(title, string.replace("\n", "<br/>"))
	return apply
		
@app.route('/')
def home():
	@log_decor
	def do_home():
		with open("SITE/home.html") as f:
			return f.read()
	return do_home()

@app.route('/log/')
def log():
	@log_decor
	def do_log():
		with open(logfile) as f:
			return f.read().replace("\n", "<br/>")
	return do_log()

@app.route('/form/')
def form():
	@log_decor
	def do_form():
		with open("SITE/form.html") as f:
			return f.read()
	return do_form()

@app.route("/graph/")
def graph():
	@log_decor
	def make_graph():
		region = request.args.get("region")
		if not region:
			region = ["US"]
		else:
			region = region.split(" ")
			region = [r.upper() for r in region]
		key = request.args.get("key") or "positiveIncrease"
		s = request.args.get("smooth")
		if s:
			if s.upper() == "TRUE": smooth = True
			elif s.upper() == "FALSE": smooth = False
			else: raise TypeError("Invalid smooth value passed, must be 'True' or 'False' (no quotes)")
		else:
			smooth = True
		
		img = make_covid_graph(regions = region, smooth = smooth, filename = None, datakey = key, show = False)
		return send_file(img, mimetype='image/gif')
	return make_graph()

application = app
if __name__ == '__main__':
	app.run(debug=True)
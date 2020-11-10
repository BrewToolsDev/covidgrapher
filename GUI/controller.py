from tkinter import messagebox
from .rootWindow import RootWindow

import threading

class asyncThread(threading.Thread):
    def __init__(self, func, arglist = []):
        threading.Thread.__init__(self, target=func, args=arglist)
        self.handled = False

class Threader:
	def __init__(self):
		pass

	def do(self, func, arglist = []):
		asyncThread(func, arglist).start()

class Controller:
	def __init__(self, version, graph_function, client = False, api_url = None, devmode = False):
		if client: self.name = f"Client Mode ({api_url})"
		else: self.name = f"Local Mode"
		self.client = client
		self.api_url = api_url
		self.devmode = devmode
		self.version = version
		self.graph_function = graph_function

		self.threader = Threader()
		
	def start_mainloop(self):
		self.root = RootWindow(self)
		self.root.mainloop()

	def report_callback_exception(self, *args):
		messagebox.showerror('Exception', traceback.format_exception(*args))
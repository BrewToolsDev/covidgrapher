import os, sys, json, ctypes, signal, traceback, threading, multiprocessing
from collections import deque
from covidgrapher import make_covid_graph, REGIONS, DATA_OPTIONS, DATA_OPTIONS_MAP
from PIL import Image, ImageTk
from copy import deepcopy
from tkinter import ttk, Tk, Toplevel, Listbox, Button, StringVar, Frame, \
messagebox, Checkbutton, Label, IntVar, StringVar, OptionMenu, Canvas, \
Listbox, Scrollbar

VERSION = "V 0.1"

helpme ="Covid Stat Grapher Gui by Andrew Spangler - GPLv3 - API under Creative Commons CC BY 4.0"

#Object to be instantiated outside tkinter mainloop to call threads
class Threader:
	def do(self, callback, arglist: list = []):
		threading.Thread(target = callback, args = arglist).start()

class LabeledCheckbutton(ttk.Frame):
	def __init__(self, text = None, default = "", *args, **kwargs):
		command = kwargs.pop("command") if kwargs.get("command") else None
		ttk.Frame.__init__(self, *args, **kwargs)
		self.var = IntVar()
		self.var.set(default)
		entry = Checkbutton(self, variable = self.var, command = command)
		entry.pack(side = "right", fill = "x", expand = False, padx = 2)
		label = Label(self, text = text)
		label.pack(side = "left", fill = None, padx = 2, expand = False)
	def get(self): return self.var.get()
	def set(self, val): self.var.set(val)

class ResizableCanvas(Canvas):
	def __init__(self,parent,**kwargs):
		Canvas.__init__(self,parent,**kwargs)
		self.configure(borderwidth = 0, highlightthickness = 0)
		self.bind("<Configure>", self.on_resize)
		self.height = self.winfo_reqheight()
		self.width = self.winfo_reqwidth()

	def resize(self, oldwidth, oldheight, newwidth, newheight):
		wscale = newwidth/oldwidth
		hscale = newheight/oldheight
		self.config(width=newwidth, height=newheight)
		self.scale("all",0,0,wscale,hscale)
		self.width = newwidth
		self.height = newheight

	def on_resize(self,event):
		self.resize(self.width, self.height,event.width, event.height)
	def refresh(self):
		self.resize(self.width, self.height, self.winfo_reqwidth(), self.winfo_reqheight())

class WindowFrame(ttk.Frame):
	def __init__(self, controller, *args, **kwargs):
		ttk.Frame.__init__(self, *args, **kwargs)
		self.place(relwidth = 1, relheight = 1)
		self.controller = controller
		self.image = None
		self.raw_img = None
		self.edited_image = None

		left_column_container = Frame(self)
		left_column_container.pack(side = "left", fill = "both", expand = True)

		canvas_container = Frame(left_column_container)
		canvas_container.pack(side = "top", fill = "both", expand = True)
		self.canvas_height = 720
		self.canvas_width = 1080
		self.canvas = ResizableCanvas(canvas_container, relief="sunken", background = "#333333")
		self.canvas.config(width = self.canvas_width, height = self.canvas_height, highlightthickness=0)
		self.canvas.place(relwidth = 1, relheight = 1)
		self.canvas_frame = Frame(self.canvas, border = 0, highlightthickness = 0)
		self.canvas_frame.config(width= self.canvas_width, height = self.canvas_height)
		self.canvas.create_window(0,0, window=self.canvas_frame, anchor='nw')

		sidebar_container = Frame(self)
		sidebar_container.pack(side = "right", fill = "y", expand = False)
		sidebar_container.configure(width = 50)

		self.data_type_var = StringVar()
		self.data_type_var.set(DATA_OPTIONS[0])
		self.data_type_dropdown = OptionMenu(sidebar_container, self.data_type_var, *DATA_OPTIONS)
		self.data_type_dropdown.pack(side="top", fill = "x", expand = False, padx = 2)

		self.smoothing_button = LabeledCheckbutton("7-Day Smoothing", True, sidebar_container)
		self.smoothing_button.pack(side="top", fill = "x", expand = False, padx = 2)
		self.us_button = LabeledCheckbutton("Total US Graph", True, sidebar_container, command = self.on_us_set)
		self.us_button.pack(side="top", fill = "x", expand = False, padx = 2)
		
		listbox_container = Frame(sidebar_container)
		listbox_container.pack(side = "top", fill = "y", expand = True)

		self.scrollbar = Scrollbar(listbox_container)
		self.scrollbar.pack(side="right", fill="y", padx = (0,2))
		self.listbox = Listbox(listbox_container, selectmode = "multiple")
		self.listbox.pack(side = "right", fill = "y", expand = True, padx = (2,0))

		build_button = Button(sidebar_container, text = "Build Graph", command = self.on_build)
		build_button.pack(side="top", fill = "x", expand = False, padx = 4, pady = 4)

		for r in REGIONS:
			self.listbox.insert("end", r)
		self.listbox.config(yscrollcommand=self.scrollbar.set)
		self.scrollbar.config(command=self.listbox.yview)

		self.bind("<Configure>", self.on_configure)
		self.on_us_set()
		self.on_build()
		self.after(10, self.on_configure)

	def on_us_set(self):
		if self.us_button.get(): self.listbox.configure(state="disable")
		else: self.listbox.configure(state="normal")

	def resize_canvas_image(self):
		picwidth = self.canvas.winfo_width()
		wpercent = (picwidth/float(self.raw_image.size[0]))
		hsize = int((float(self.raw_image.size[1])*float(wpercent)))
		if picwidth < 1 or hsize < 1: return 
		picheight = self.canvas.winfo_height()
		if hsize > picheight:
			hpercent = (picheight/float(self.raw_image.size[1]))
			wsize = int((float(self.raw_image.size[0])*float(hpercent)))
			self.edited_image = self.raw_image.resize((wsize,picheight), Image.ANTIALIAS)
		else: self.edited_image = self.raw_image.resize((picwidth,hsize), Image.ANTIALIAS)
		self.image = ImageTk.PhotoImage(image = self.edited_image)
		self.canvas.create_image(self.canvas.winfo_width()/2, self.canvas.winfo_height()/2, anchor = "center", image = self.image)

	def on_build(self, event = None):
		self.canvas.delete("all")
		t = self.canvas.create_text(
			self.canvas.winfo_width()/2,
			self.canvas.winfo_height()/2,
			text = "Building graph,\nplease be patient.",
			anchor = "center",
			font = ("Sans", 30),
			fill = "white",
			justify = "center"
		)
		self.winfo_toplevel().update_idletasks() #Refresh screen
		self.edited_image = None
		region = []
		if not self.us_button.get():
			indx = self.listbox.curselection()
			if indx:
				for i in indx:
					r = self.listbox.get(i)
					region.append(r)
			else: region = "US"
		else: region = "US"
		smooth = self.smoothing_button.get()
		datakey = DATA_OPTIONS_MAP[self.data_type_var.get()]
		fn = make_covid_graph(region, smooth, datakey = datakey)
		self.raw_image = Image.open(fn)
		self.resize_canvas_image()
		self.after(100, lambda:self.canvas.delete(t))
			
	def on_configure(self, event = None):
		if not self.edited_image: self.resize_canvas_image()
		self.after(50, self.resize_canvas_image)
		
class RootWindow(ttk.Frame):
	def __init__(self, controller):
		ttk.Frame.__init__(self)
		#Controller to allow inter-window access, passed to all windows and some widgets
		self.controller = controller 
		#Because we are instantiating a widget without passing it a parent window one is created for the ttk.Frame
		#This is some trickery that allows a tk.Toplevel to be in control of the tkinter mainloop without
		#establishing a proper tk.Root
		#Because the tk.toplevel was instantiated behind the scenes we have to grab it
		self.window = self._nametowidget(self.winfo_parent()) #Get toplevel window name
		self.window.bind("<Escape>", self.exit) #Bind escape key to exit window
		self.window.title(f"Covid Grapher Gui - {controller.version}") #Set window title
		self.window.geometry("1080x720") #Set window start size
		#Override normal exit protocol when the close button is pushed to shut down gently instead
		self.window.protocol("WM_DELETE_WINDOW", self.exit)
		WindowFrame(controller, self)
		# if self.controller.devmode: self.window.report_callback_exception = self.controller.report_callback_exception
		self.place(relwidth = 1, relheight = 1)

	def exit(self, *args):
		if messagebox.askyesno("Exit?", "Are you sure you wish to exit?"):
			self.window.destroy()
			sys.exit()

class Controller:
	def __init__(self, devmode = False):
		self.devmode = devmode
		self.version = VERSION
		self.threader = Threader()
		
	def start_mainloop(self):
		self.root = RootWindow(self)
		self.root.mainloop()

	def report_callback_exception(self, *args):
		messagebox.showerror('Exception', traceback.format_exception(*args))

if __name__ == "__main__":
	app = Controller(devmode = True)
	app.start_mainloop() #Call tk mainloop
from PIL import Image, ImageTk
from io import BytesIO
from covidgrapher import REGIONS, DATA_OPTIONS, DATA_OPTIONS_MAP

from tkinter import ttk, Toplevel, Listbox, Button, StringVar, Frame, \
Checkbutton, Label, IntVar, StringVar, OptionMenu, Canvas, Scrollbar, \
filedialog, Radiobutton, Text

FLOPPY_BYTES = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00YIDATx\x9c\xbd\x93A\n\x00 \x08\x04w\xa3\xff\x7f\xb9nb\x1bDj$t\x08\xb6q\x10#\x80\x81X\xd1_Z\xf01\xb4\xa1\x07P\x82tG3\x06\xc9\x18,\x90\x0c`\x81\xf4C\xe8j\xb8Y\x03+5\xd0A\xfe7\xb8]*3}n\xb0u\x90\xda\x0c\xcb\x06e\x00\x11\xff\x8do\r&2<\t)\xe6\x84\xac\xa0\x00\x00\x00\x00IEND\xaeB`\x82'

# Sizing options constants
SCALAR = 0
PIXELS = 1
SIZING_OPTIONS = {
	SCALAR : "Scale output",
	PIXELS : "Custom"
}

#loads a pil image from a bytestring
def load_image_object_from_bytes_array(bytes_array):
	return Image.open(BytesIO(bytes_array))

class MainInterface(ttk.Frame):
	def __init__(self, controller, *args, **kwargs):
		ttk.Frame.__init__(self, *args, **kwargs)
		self.place(relwidth = 1, relheight = 1)
		self.controller = controller
		self.image = None
		self.raw_image = None
		self.edited_image = None
		self.tiles = []

		self.save_image = ImageTk.PhotoImage(load_image_object_from_bytes_array(FLOPPY_BYTES))

		left_column_container = Frame(self)
		left_column_container.pack(side = "left", fill = "both", expand = True)

		canvas_container = Frame(left_column_container)
		canvas_container.pack(side = "top", fill = "both", expand = True)
		self.canvas_height = 720
		self.canvas_width = 1080
		self.canvas = ResizableCanvas(canvas_container, relief="sunken")
		self.canvas.config(width = self.canvas_width, height = self.canvas_height, highlightthickness=0)
		self.canvas.place(relwidth = 1, relheight = 1)
		self.canvas_frame = Frame(self.canvas, border = 0, highlightthickness = 0)
		self.canvas_frame.config(width= self.canvas_width, height = self.canvas_height)
		self.canvas.create_window(0,0, window=self.canvas_frame, anchor='nw')
		self.canvas.bind("<Motion>", self.on_mouse_move)
		self.canvas.bind("<Button-1>", self.on_left_click)

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

		self.build_button = Button(sidebar_container, text = "Build Graph", command = lambda: self.controller.threader.do(self.on_build))
		self.build_button.pack(side="top", fill = "x", expand = False, padx = 4, pady = 4)

		for r in REGIONS: self.listbox.insert("end", r)
		self.listbox.config(yscrollcommand=self.scrollbar.set)
		self.scrollbar.config(command=self.listbox.yview)

		self.bind("<Configure>", self.on_configure)
		self.on_us_set()
		
		def first_run_async():
			save_button = Tile(self, self.save_image, self.save_image, self.save)
			save_button.set_dimensions(10,10,25,25)
			self.tiles.append(save_button)
			self.place_tiles()
			self.on_build()
			self.after(10, self.on_configure)

		self.controller.threader.do(first_run_async, [])
		

		

	def on_us_set(self):
		if self.us_button.get(): self.listbox.configure(state="disable")
		else: self.listbox.configure(state="normal")

	def resize_canvas_image(self):
		if not self.raw_image: return
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
		self.place_tiles()

	def on_build(self, event = None):
		self.build_button.configure(state = "disable")
		self.canvas.delete("all")
		t = self.canvas.create_text(
			self.canvas.winfo_width()/2,
			self.canvas.winfo_height()/2,
			text = "Building graph,\nplease be patient.",
			anchor = "center",
			font = ("Sans", 30),
			fill = "#333333",
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
		if self.controller.client:
			fn = self.controller.graph_function(self.controller.api_url, region, smooth, datakey = datakey)
		else: fn = self.controller.graph_function(region, smooth, datakey = datakey)
		self.raw_image = Image.open(fn)
		self.resize_canvas_image()
		self.build_button.configure(state = "normal")
		self.after(100, lambda:self.canvas.delete(t))

	def on_configure(self, event = None):
		if not self.edited_image: self.resize_canvas_image()
		self.after(50, self.resize_canvas_image)

	def place_tiles(self, event = None):
		for t in self.tiles:
			for r in t.references:
				self.canvas.delete(r)
			for r in t.active_references:
				self.canvas.delete(r)
			self.place_tile(t)

	def place_tile(self, tile):
		if tile.active:
			tile.references.append(self.canvas.create_image(tile.x + 4, tile.y + 4, anchor = "nw", image = tile.active_image))
			self.activate_tile()
		else: tile.references.append(self.canvas.create_image(tile.x + 4, tile.y + 4, anchor = "nw", image = tile.inactive_image))

	def on_mouse_move(self, event):
		y = int(event.y + (float(self.canvas.yview()[0]) * self.canvas_height))
		x = event.x
		for t in self.tiles:
			if t.is_in_range(x,y):
				if t.active: continue
				else: t.activate()
			else: t.deactivate()

	def activate_tile(self, tile):
		tile.active_references.extend([
			self.canvas.create_rectangle(tile.x - 1, tile.y - 1, tile.x + tile.width, tile.y + tile.height, outline="#000000", width = 2),
		])

	def deactivate_tile(self, tile):
		for r in tile.active_references:
			self.canvas.delete(r)

	def on_left_click(self, event):
		for t in self.tiles:
			if t.on_click(event.x,event.y): break

	def save(self): SaveMenu(self.controller, self.raw_image)

class LabeledEntry(ttk.Frame):
	def __init__(self, text = None, default = "", *args, **kwargs):
		ttk.Frame.__init__(self, *args, **kwargs)
		label = Label(self, text = text)
		label.pack(side = "left", fill = None, padx = 2)
		self.var = StringVar()
		self.var.set(default)
		entry = ttk.Entry(self, textvariable = self.var)
		entry.pack(side = "right", fill = "x", expand = True, padx = 2)
	def get(self): return self.var.get()
	def set(self, val): self.var.set(val)

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

class selection_box(ttk.LabelFrame):
	def __init__(self, label_text, selection_list, command, *args, **kwargs):
		ttk.LabelFrame.__init__(self, *args, **kwargs)
		self.inner_frame = Frame(self)
		self.inner_frame.pack(fill = "both", expand = True, side = "left")
		self.configure(text = label_text)
		self.var = IntVar()
		for text, value in selection_list:
			b = Radiobutton(self.inner_frame, text = text, variable = self.var, value = value, command = command)
			b.pack(anchor = "w", fill = "y", expand = False)
		#select first button
		for s in selection_list: self.var.set(s[1]); break
	def get(self): return self.var.get()

class Tile():
	def __init__(self, manager, active_image, inactive_image, callback):
		self.x, self.y, self.width, self.height = 0, 0, 0, 0
		self.manager = manager
		self.references = []
		self.active_references = []
		self.active = False
		self.active_image = active_image
		self.inactive_image = inactive_image
		self.callback = callback

	def set_dimensions(self, x, y, width, height):
		self.x, self.y, self.width, self.height = x, y, width, height

	def is_in_range(self, pointer_x, pointer_y):
		left_bound = self.x
		right_bound = self.x + self.width
		top_bound = self.y
		bottom_bound = self.y + self.height
		if pointer_x > left_bound and pointer_x < right_bound:
			if pointer_y > top_bound and pointer_y < bottom_bound:
				return True

	def on_click(self, pointer_x, pointer_y):
		if self.is_in_range(pointer_x, pointer_y):
			self.callback()
			return True

	def activate(self):
		self.active = True
		self.manager.activate_tile(self)

	def deactivate(self):
		self.active = False
		self.manager.deactivate_tile(self)

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

class SaveMenu(Toplevel):
	def __init__(self, controller, image_data):
		Toplevel.__init__(self)
		self.geometry(f"{350}x{200}")
		self.title("Export")
		self.resizable(True, True)
		self.attributes('-topmost', True)
		self.image_data = image_data
		self.outer_frame = Frame(self)
		self.outer_frame.pack(fill = "both", expand = True)
		sizing_and_color_frame = Frame(self.outer_frame)
		sizing_and_color_frame.pack(expand = True, fill = "both")
		sizing_options = [(SIZING_OPTIONS[SCALAR], SCALAR), (SIZING_OPTIONS[PIXELS], PIXELS)]
	
		size_selection_and_size_option_frame = Frame(sizing_and_color_frame)
		size_selection_and_size_option_frame.pack(fill = "both", expand = True, padx = 4)
		self.size_selection = selection_box("SIZING", sizing_options, self.on_size_select, size_selection_and_size_option_frame)
		self.size_selection.pack(side = "left", fill = "y")

		selection_frame_frame = ttk.LabelFrame(size_selection_and_size_option_frame, text = "SIZE OPTIONS")
		selection_frame_frame.pack(fill = "both", expand = True, side = "left")
		self.scaling_frame = Frame(selection_frame_frame)
		self.scaling_frame.place(relwidth = 1, relheight = 1)
		self.scaling_factor = LabeledEntry("Scaling Factor - ", 1, self.scaling_frame)
		self.scaling_factor.place(relwidth = 1, relheight = 1)

		self.custom_dimensions_frame = Frame(selection_frame_frame)
		self.custom_dimensions_frame.place(relwidth = 1, relheight = 1)
		self.dimension_x_entry = LabeledEntry("Width - ", "16", self.custom_dimensions_frame)
		self.dimension_x_entry.pack(fill = "both", expand = True, anchor = "w")
		self.dimension_y_entry = LabeledEntry("Height - ", "16", self.custom_dimensions_frame)
		self.dimension_y_entry.pack(fill = "both", expand = True, anchor = "w")
		self.on_size_select()

		footer = ttk.LabelFrame(self.outer_frame, text = "FILE")

		select_path_frame = Frame(footer)
		select_path_frame.pack(fill = "both", expand = True)
		self.file_path_entry = LabeledEntry("File path", "", select_path_frame)
		self.file_path_entry.pack(fill = "both", expand = True, side = "left", padx = (2, 2))
		select_path_button = Button(select_path_frame, command = self.set_save_path, text = "Select file").pack(side = "right", pady = (4,6), padx = (2, 2), expand = False)
		Button(footer, text = "Save", command = self.save).pack(fill = "x", expand = False, padx = 4, pady = 4)
		footer.pack(fill = "x", expand = False, padx = 4, side = "top", pady = 4)

	def set_save_path(self):
		save_as = filedialog.asksaveasfilename(
			defaultextension = ".*",
			filetypes = [
					("All files", ".*"), 
					("PNG files", ".png"), 
					("JPEG files", ".jpg .jpeg"), 
					("BMP files", ".bmp"), 
					("ICO files", ".ico")
			]
		)
		self.file_path_entry.set(save_as)

	def on_size_select(self):
		sizing_mode = self.size_selection.get()
		def handle_scalar():self.scaling_frame.tkraise()
		def handle_pixels():self.custom_dimensions_frame.tkraise()
		modes = {SCALAR : handle_scalar,PIXELS : handle_pixels}
		modes[sizing_mode]()

	def on_loop_select(self):
		loop_mode = self.loop_selection.get()
		def handle_loop(): self.number_of_loops_frame.tkraise()
		def handle_no_loop(): self.no_loop_frame.tkraise()
		modes = { LOOP : handle_loop, NO_LOOP : handle_no_loop }
		modes[loop_mode]()

	def save(self):
		print("Beginning image conversion")
		image_data = self.image_data #Make a copy of the image data for manipulation in case save fails and needs to be redone
		def handle_scalar(image):
			print("Appling scalar resize to image")
			try:
				factor = int(self.scaling_factor.get())
				print(f"Resizing image by factor {factor}")
			except Exception as e:
				return self.error(f"Invalid scaling factor: {e}")
			if not factor:
				return self.error(f"Scaling factor cannot be zero")
			if factor == 1: return image
			else: return image.resize((int(image.height) * int(factor), int(image.width) * int(factor)), Image.BOX)

		def handle_pixels(image): 
			try:
				width = self.dimension_x_entry.get()
				height = self.dimension_y_entry.get()
				print(f"Resizing image to {width} x {height}")
			except Exception as e:
				return self.error(f"Invalid pixel resize values {e}")

			try: return image.resize((int(height), int(width)), Image.BOX)
			except Exception as e:
				return self.error(f"Error resizing image - {e}")
			
		sizing_options = {
			SCALAR : handle_scalar,
			PIXELS : handle_pixels
		}
		sizing_mode = self.size_selection.get()
		image_data = sizing_options[sizing_mode](image_data)
		if not image_data: return

		try: filename = self.file_path_entry.get()
		except Exception as e:
			return self.error(f"Error getting file name: {e}")
		if not filename:
			return self.error(f"No filename specified")

		try:
			print("Saving...")
			image_data.save(filename)
		except Exception as e:
			return self.error(f"Error saving image: {e}")

		self.destroy() #Sucessful!

	def error(self, error):
		print(error)
		error_frame = error_window(error, self.outer_frame)
		error_frame.place(relwidth = 1, relheight = 1)

class error_window(Frame):
	def __init__(self, error, *args, **kwargs):
		Frame.__init__(self, *args, **kwargs)
		self.error = Text(self, wrap = "word")
		self.error.insert("end", error)
		self.error.configure(state = "disable")
		self.error.place(relwidth = 1, x = +4, width = -8, height = - 33, relheight = 1)
		self.exit_button = Button(self, command = self.exit, text = "Accept")
		self.exit_button.place(relwidth = 1, x = +4, width = -8, rely = 1, y = - 29, height = 25)
	def exit(self): self.destroy()
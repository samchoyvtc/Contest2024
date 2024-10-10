import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import matplotlib.colors as mcolors

class GUI():
    def __init__(self, master,gm):
        self.state = 0
        self.animation_step = -1
        self.graph = []
        self.algorithm_steps = ["0","0","0"]
        self.post_btns = []
        self.master = master
        self.master.title("Array Viewer")
        self.master.attributes('-fullscreen', False)

        # Bind F11 and Escape keys for full-screen toggle
        self.master.bind("<F11>", self.toggle_fullscreen)
        self.master.bind("<Escape>", self.toggle_fullscreen)

        # Create buttons
        self.create_buttons(gm)

        # Create input fields
        #self.create_input_fields(gm)

        # Create canvas for plots
        self.create_plots(gm)

        # Create additional buttons at the bottom
        self.create_bottom_buttons(gm)

    def reset_animationstep(self):
        self.animation_step = -1

    def create_buttons(self,gm):
        # Create labels above the buttons
        ttk.Label(self.master, text=f"Algorithm 1 steps:  " + str(self.algorithm_steps[0]), font=("Helvetica", 15)).grid(row=12, column=0, padx=10, pady=10)
        ttk.Label(self.master, text=f"Algorithm 2 steps:  " + str(self.algorithm_steps[1]), font=("Helvetica", 15)).grid(row=13, column=0, padx=10, pady=10)
        ttk.Label(self.master, text=f"Algorithm 3 steps:  " + str(self.algorithm_steps[2]), font=("Helvetica", 15)).grid(row=14, column=0, padx=10, pady=10)

        # Create algorithm buttons at the top middle
        button_frame = ttk.Frame(self.master)  # Create a frame to hold the buttons
        button_frame.grid(row=8, column=0, columnspan=3, padx=10, pady=10, sticky="n")

        selected_algorithm = tk.StringVar()

        # Create algorithm buttons
        for i in range(3):
            button = ttk.Button(button_frame, text=f"Run Algorithm {i+1}", command=lambda i=i: self.on_algorithm_button_click(i), width=20)
            button.grid(row=12+i, column=3, padx=10, pady=10)  # Add buttons to the button_frame

    def create_bottom_buttons(self,gm):
        """Create additional buttons at the bottom of the canvas."""
        bottom_frame = ttk.Frame(self.master)  # Create a frame to hold the buttons
        bottom_frame.grid(row=15, column=1, columnspan=3, padx=10, pady=10, sticky="n")

        button_names = ["use algorthim 1 ans","use algorthim 2 ans","use algorthim 3 ans","use typing ans","Start Ques Animation","Ques animation NextStep"]  # Names for the buttons
        for i, name in enumerate(button_names):
            button = ttk.Button(bottom_frame, text=name, command=lambda i=i: self.on_bottom_button_click(i), width=30)
            button.grid(row=0, column=i, padx=10, pady=10)  # Add buttons to the bottom_frame
            self.post_btns.append(button)
            self.post_btns[i]["state"]="disabled"
        self.post_btns[4]["state"]="enable"
            


    def create_input_fields(self,gm):
        # Store input fields as attributes
        self.mold_entry = ttk.Entry(self.master)
        ttk.Label(self.master, text=f"Mold:").grid(row=1, column=0, padx=10, pady=10)
        self.mold_entry.grid(row=1, column=1, padx=10, pady=10)

        self.place_x_entry = ttk.Entry(self.master)
        ttk.Label(self.master, text=f"Place X:").grid(row=2, column=0, padx=10, pady=10)
        self.place_x_entry.grid(row=2, column=1, padx=10, pady=10)

        self.place_y_entry = ttk.Entry(self.master)
        ttk.Label(self.master, text=f"Place Y:").grid(row=3, column=0, padx=10, pady=10)
        self.place_y_entry.grid(row=3, column=1, padx=10, pady=10)

        self.sides_entry = ttk.Entry(self.master)
        ttk.Label(self.master, text=f"Sides:").grid(row=4, column=0, padx=10, pady=10)
        self.sides_entry.grid(row=4, column=1, padx=10, pady=10)

    def create_plots(self,gm):
        """Create plots for random arrays."""
        arrays = [gm.target_board, gm.initial_board, gm.board_diffrent,gm.marking_board]
        #arrays = [gm.target_board, gm.initial_board, gm.board_diffrent]
        array_labels = ["Target Board", "Working Board", "Board Different","Match Row Different"]
        self.canvas_list = []

        for i in range(4):
            canvas = FigureCanvasTkAgg(Figure(figsize=(4, 4), dpi=100), master=self.master)
            canvas.get_tk_widget().grid(row=1, rowspan=4, column=i, padx=10, pady=10)
            self.graph.append(self.plot_graph(arrays[i], canvas, array_labels[i],i))  # array[i] is the array
            self.canvas_list.append(canvas)

    def plot_update(self, gm):
        """Plot a graph for a given 2D array with a label."""
        gm.compareboard()
        self.graph[1].clear()
        self.graph[1].imshow(gm.working_board, cmap='viridis')
        self.graph[1].set_title("Working Board")
        self.canvas_list[1].draw_idle()
        self.graph[2].clear()
        self.graph[2].imshow(gm.board_diffrent, cmap='viridis')
        self.graph[2].set_title("Board Different")
        self.canvas_list[2].draw_idle()
    
    

    def plot_graph(self, data, canvas, label_text,i):
        """Plot a graph for a given 2D array with a label."""
        fig = canvas.figure
        colors = [['white','blue', 'yellow', 'green'],['white','blue', 'yellow', 'green'],['red', 'green'],['red', 'yellow', 'green']]  # Define your colors
        cmap = mcolors.ListedColormap(colors[i])
        plot = fig.add_subplot(111)
        plot.imshow(data, cmap=cmap, interpolation='nearest')

        # Add label to the plot
        plot.set_title(label_text)

        canvas.draw()
        return plot

    def toggle_fullscreen(self, event=None):
        """Toggle full-screen mode."""
        self.master.attributes("-fullscreen", not self.master.attributes("-fullscreen"))

    def on_algorithm_button_click(self, algorithm_index):
        """Handle algorithm button clicks."""
        if algorithm_index == 0:
            self.state = 1

    def get_input_data(self):
        """Retrieve and print the data from input fields."""
        mold = self.mold_entry.get()
        place_x = self.place_x_entry.get()
        place_y = self.place_y_entry.get()
        sides = self.sides_entry.get()
        
        # Print or process the retrieved data as needed
      #  print(f"Mold: {mold}, Place X: {place_x}, Place Y: {place_y}, Sides: {sides}")

    def on_bottom_button_click(self, button_index):
        """Handle bottom button clicks."""
        if button_index == 0:
            self.state=2
        if button_index == 4:
            self.state = 999
            self.post_btns[5]["state"]="enable"
            self.post_btns[4]["state"]="disabled"
        if button_index == 5:
            self.animation_step += 1
            self.state = 9997
# Import the necessary libraries/modules for creating GUI elements
import tkinter as tk
from tkinter import *
from tkinter import ttk,Label,Entry
from tkcalendar import Calendar
#Import libraries for choosing date
from tkcalendar import DateEntry
from views.window import WindowController
from views.modules.elements import *

class AnalyseWindow():
    
    m_class_name = 'Window Analyse'

    def __init__(self, root, show_button):
        self.main = tk.Toplevel(root)
        self.main.title('Analyse Window')
        self.main.withdraw()
        self.main.protocol("WM_DELETE_WINDOW", lambda: WindowController.show_hide_subwindow(self.main,show_button))

        #Frame
        self.top_frame = tk.Frame(self.main)
        self.top_frame.pack()

        self.create_date_entry("Start Date:", "lightpink", "cal1", "textbox1", 0, 5, 10)
        self.create_date_entry("End Date:", "lightblue", "cal2", "textbox2", 1, 10, 5)

        self.create_label("Total Task:", 2)
        self.create_label("Total Time:", 3)
        self.create_label("Average Time per Task:", 4)

        self.create_ok_button()

    #Define a function to entry Dates
    def create_date_entry(self, label_text, bg_color, cal_variable, textbox_variable, row, px1, px2):
        # Create frames for each label
        frame_label = tk.Frame(self.top_frame)
        frame_label.pack(side=tk.TOP, padx=10, pady=5, anchor="nw")

        # Create each label in corresponding frames
        label = tk.Label(frame_label, text=label_text)
        label.pack(side=tk.LEFT, padx=10, pady=5, anchor="w")

        # Create textboxes to entry Dates
        entry = tk.Entry(frame_label, bg=bg_color, width=20)
        entry.pack(side=tk.LEFT, padx=px1, pady=5, anchor="center")

        # Set an attribute on cal_variable (cal1, cal2) and assign "Date Entry" widgets to that attribute
        setattr(self, cal_variable, DateEntry(frame_label, width=7, background='darkblue', foreground='white', borderwidth=2))
        
        # Retrieve that attribute 
        getattr(self, cal_variable).pack(side=tk.RIGHT, padx=px2, pady=5, anchor="e")

        # set an attribute on textbox_variable and assign "entry" widgets to that attribute
        setattr(self, textbox_variable, entry)

    # Define function to create widgets having labels only
    def create_label(self, label_text, row):
        # Create frames for each label
        frame_label = tk.Frame(self.top_frame)
        frame_label.pack(side=tk.TOP, padx=10, pady=5, anchor="nw")

        # Create label for each widget
        label = tk.Label(frame_label, text=label_text)
        label.pack(side=tk.TOP, padx=10, pady=5, anchor="w")

    # Define button function
    def create_ok_button(self):
        button_ok = tk.Button(self.top_frame, text="OK", width=3, height=2, bg="yellow", command=self.show_selected_dates)
        button_ok.pack(side=tk.BOTTOM, padx=10, pady=5, anchor="sw")

    # Define Selection Dates function to integrate to OK_Button
    def show_selected_dates(self):
        # Get data from cal1, cal 2
        selected_start_date = self.cal1.get_date()
        selected_end_date = self.cal2.get_date()

        # Delete old things in textbox1 first
        self.textbox1.delete(0, tk.END)

        # Insert data getting from selected_start_date
        self.textbox1.insert(0, selected_start_date)

        # Delete old things in textbox2 first
        self.textbox2.delete(0, tk.END)

        ## Insert data getting from selected_end_date
        self.textbox2.insert(0, selected_end_date)
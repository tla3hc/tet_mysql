# Import the necessary libraries/modules for creating GUI elements
import tkinter as tk
from tkinter import *
from tkinter import ttk
from utils.user import User

class AddTasksFeature(Toplevel):
    def __init__(self,master):
        super().__init__(master=master)
        # Create the title for main application window
        self.title("Add tasks")
        self.geometry("500x300")
        user = User()
        self.project = user.get_project()  
        # Use create_widgets definition
        self.create_widgets()
    
    def create_widgets(self):
        # Top frame
        self.top_frame = Frame(self)
        self.top_frame.pack(fill=NONE, anchor=CENTER)

        # Project label
        self.project_name_label = Label(self.top_frame, text = 'Project name', font=('calibre',10, 'bold'))
        self.selected_project = StringVar()
        

        # Project combobox
        self.project_name_combobox = ttk.Combobox(self.top_frame, width= 25, textvariable = self.selected_project, state='readonly')
        # self.project_name_combobox.current(self.project)
        self.project_name_label.grid(row=0, column=0, padx=5, pady=10)
        self.project_name_combobox.grid(row=0, column=1, padx=5, pady=10)

        # Main frame
        self.main_frame = Frame(self, highlightbackground="light gray", highlightthickness=1)
        self.main_frame.pack(fill=BOTH, side=TOP, expand=1, padx=5)
        self.main_frame.grid_rowconfigure(0, weight = 1)
        self.main_frame.grid_columnconfigure(0, weight = 1)

        # Button frame
        self.button_frame = Frame(self)
        self.button_frame.pack(fill=X, anchor=CENTER)

        # Add button
        self.add_button = Button(self.button_frame, text="Add task", height=2, width=10)
        self.add_button.pack(anchor=E, side=RIGHT,padx=10, pady=10)

        # Cancel
        self.cancel_button = Button(self.button_frame, text="Cancel", height=2, width=10)
        self.cancel_button.pack(anchor=E,side=RIGHT, pady=10)
        


# Initial frame class
class StartFrame(Frame):
    def __init__(self,parent, controller):
        Frame.__init__(self, parent)
        # Label
        self.task_des_label = Label(self, text = 'Choose a project to start', font=('calibre',10, 'bold'))
        self.task_des_label.pack(anchor=CENTER, padx=10, pady=40)   

# Common task frame class
class Common(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        # Label
        self.task_des_label = Label(self, text = 'Task description ', font=('calibre',10, 'bold'))
        self.task_des_label.pack(anchor=CENTER, padx=20, pady=10, side=LEFT)

        # Entry
        self.task_des_entry = Entry(self,width=30, font=('calibre',10, 'bold'))
        self.task_des_entry.pack(anchor=CENTER, side=LEFT)

# Project A task frame class
class ProjectA(Frame):
    def __init__(self,parent, controller):
        Frame.__init__(self, parent)
        # Label
        self.task_des_label = Label(self, text = 'Task description ', font=('calibre',10, 'bold'))
        self.task_des_label.pack(anchor=CENTER, padx=20, pady=10, side=LEFT)

        # Entry
        self.task_des_entry = Entry(self,width=30, font=('calibre',10, 'bold'))
        self.task_des_entry.pack(anchor=CENTER, side=LEFT)


# Project B task frame class
class ProjectB(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # Task type frame
        self.type_frame = Frame(self)
        self.type_frame.pack(fill=NONE, anchor = CENTER)
        
        # Task type label
        self.type_label = Label(self.type_frame, text = 'Task type', font=('calibre',10, 'bold'))
        self.type_label.grid(row=0, column=0, padx=5, pady=10)

        # Task type combobox
        self.selected_type = StringVar(value='Development')
        self.type = ttk.Combobox(self.type_frame, width= 25, textvariable = self.selected_type, state='readonly')
        self.type['values'] = ('Development', 'Unit Test', "Common", "N/A")
        self.type.grid(row=0, column=1, padx=5, pady=10)

        # Main frame
        self.main_frame = Frame(self)
        self.main_frame.pack(fill=BOTH, expand=1, anchor=S)
        self.main_frame.grid_rowconfigure(0, weight = 1)
        self.main_frame.grid_columnconfigure(0, weight = 1)

# Project B Development frame class
class ProjectBDevelopment(Frame):
    def __init__(self ,parent, controller):
        Frame.__init__(self, parent)
        # Label
        self.label = Label(self, text = 'Description for development', font=('calibre',10, 'bold'))
        self.label.grid(row=0, column=0, padx=10, pady=20)
        # Entry
        self.entry = Entry(self,width=30, font=('calibre',10, 'bold'))
        self.entry.grid(row=0, column=1, padx=10, pady=20)


# Project B Unit test frame class
class ProjectBUnitTest(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        # Main frame
        self.type_frame = Frame(self)
        self.type_frame.pack(side=TOP, fill=X, padx=5, pady=5)
        
        # Type frame label
        self.type_label = Label(self.type_frame, text = 'Type', font=('calibre',10, 'bold'))
        self.type_label.grid(row=0, column=0,padx=5, pady=5, sticky=W)

        # Type frame combobox
        self.selected_type=StringVar()
        self.type = ttk.Combobox(self.type_frame, width= 10, textvariable = self.selected_type, state='readonly')
        self.type['values'] = ('NEW', 'REG', 'REVIEW')
        self.type.grid(row=0, column=1, padx=10, pady=5, columnspan=2, sticky=W)

        # Test type radio label
        self.radio_button_label = Label(self.type_frame, text = 'Test type', font=('calibre',10, 'bold'))
        self.radio_button_label.grid(row=1, column=0, sticky=W, padx=5, pady=5)

        # Test type radio button
        self.checkvarTV = IntVar()
        self.checkvarTS = IntVar()
        self.checkvarTE = IntVar()
        self.checkvarTestID = IntVar()
        self.TV = Checkbutton(self.type_frame, text='TV', variable=self.checkvarTV, onvalue=1, offvalue=0)
        self.TV.grid(row=1, column=1, padx=4, pady=5)
        self.TS = Checkbutton(self.type_frame, text='TS', variable=self.checkvarTS, onvalue=1, offvalue=0)
        self.TS.grid(row=1, column=2, padx=4, pady=5)
        self.TE = Checkbutton(self.type_frame, text='TE', variable=self.checkvarTE, onvalue=1, offvalue=0)
        self.TE.grid(row=1, column=3, padx=4, pady=5)
        self.TestID = Checkbutton(self.type_frame, text='TestID', variable=self.checkvarTestID, onvalue=1, offvalue=0)
        self.TestID.grid(row=1, column=4, padx=4, pady=5)

        # Unit name label
        self.unit_name_label = Label(self.type_frame, text = 'Unit name', font=('calibre',10, 'bold'))
        self.unit_name_label.grid(row=2, column=0, padx=5, pady=5, sticky=W)
        
        # Unit name entry
        self.unit_name_entry = Entry(self.type_frame,width=30, font=('calibre',10, 'bold'))
        self.unit_name_entry.grid(row=2, column=1, padx=5, pady=5, columnspan=4, sticky=W)

        # Version label
        self.version_label = Label(self.type_frame, text = 'Version', font=('calibre',10, 'bold'))
        self.version_label.grid(row=3, column=0, padx=5, pady=5, sticky=W)

        # Version entry
        
        self.version_entry = Entry(self.type_frame,width=10, font=('calibre',10, 'bold'))
        self.version_entry.grid(row=3, column=1, padx=5, pady=5, columnspan=4, sticky=W)

# Project C frame class
class ProjectC(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        # Label
        self.task_frame = Frame(self, )
        self.task_frame.place(anchor=CENTER, relx=.4, rely=.5)

        self.task_des_label = Label(self.task_frame, text = 'Task description ', font=('calibre',10, 'bold'))
        self.task_des_label.grid(column=0, row=0, padx=5, pady=5)

        # Entry
        self.task_des_entry = Entry(self.task_frame,width=30, font=('calibre',10, 'bold'))
        self.task_des_entry.grid(column=1, row=0, padx=5, pady=5)

        # Label
        self.task_cat_label = Label(self.task_frame, text = 'Category ', font=('calibre',10, 'bold'))
        self.task_cat_label.grid(column=0, row=1, padx=5, pady=5, )

        # Entry
        self.selected_cat=StringVar()
        self.task_cat_entry = ttk.Combobox(self.task_frame, width= 30, textvariable = self.selected_cat, state='readonly')
        self.task_cat_entry.grid(column=1, row=1, padx=5, pady=5)

class ProjectLabVIEW(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        # Label
        self.task_des_label = Label(self, text = 'Task description ', font=('calibre',10, 'bold'))
        self.task_des_label.pack(anchor=CENTER, padx=20, pady=10, side=LEFT)
        # Entry
        self.task_des_entry = Entry(self,width=30, font=('calibre',10, 'bold'))
        self.task_des_entry.pack(anchor=CENTER, side=LEFT)
    
class ProjectCANoe(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        # Label
        self.task_des_label = Label(self, text = 'Task description ', font=('calibre',10, 'bold'))
        self.task_des_label.pack(anchor=CENTER, padx=20, pady=10, side=LEFT)
        # Entry
        self.task_des_entry = Entry(self,width=30, font=('calibre',10, 'bold'))
        self.task_des_entry.pack(anchor=CENTER, side=LEFT)

class ProjectSound2Light(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        # Label
        self.task_des_label = Label(self, text = 'Task description ', font=('calibre',10, 'bold'))
        self.task_des_label.pack(anchor=CENTER, padx=20, pady=10, side=LEFT)
        # Entry
        self.task_des_entry = Entry(self,width=30, font=('calibre',10, 'bold'))
        self.task_des_entry.pack(anchor=CENTER, side=LEFT)

class ProjectUnassigned(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        # Label
        self.task_des_label = Label(self, text = 'Task description ', font=('calibre',10, 'bold'))
        self.task_des_label.pack(anchor=CENTER, padx=20, pady=10, side=LEFT)

        # Entry
        self.task_des_entry = Entry(self,width=30, font=('calibre',10, 'bold'))
        self.task_des_entry.pack(anchor=CENTER, side=LEFT)
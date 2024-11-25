from tkinter import *
import sys

from controllers.controller import Controller
from views.addtasks_window import *
import configs.config_headings as heading
from utils.user import User

'''
    AddTaskController: This class is responsible for creating, closing Add new task popup, binding functionality,
    control switching between different frames in popup

'''

class AddTasksController:
    def __init__(self,master):
        # Call new Add tasks Toplevel
        self.addtasks_window = AddTasksFeature(master)
        list = heading.ConfigListBox().project_List[1:len(heading.ConfigListBox().project_List)]  
        user = User()
        self.proj = user.get_project()
        index_num = list.index(self.proj)
        # Load current projects
        self.addtasks_window.project_name_combobox['values'] = list
        self.addtasks_window.project_name_combobox.current(index_num)
        

        # Binding fucntions
        self.addtasks_window.grab_set()

        self.project_switch_frame()
        self.prjb_switch_frame()
        self.binding()

    # Binding function
    def binding(self):
        # When select project combobox, switching frame according to user's selection
        self.addtasks_window.project_name_combobox.bind('<<ComboboxSelected>>',lambda e: self.show_frame())

        # When left click "Cancel" button, close the popup
        self.addtasks_window.cancel_button.bind('<Button-1>',lambda e: self.cancel())

        # This binding is for Project B frame only
            # In Project B frame, when select task type combobox, switching frame according to user's selection
        self.frames[ProjectB].type.bind('<<ComboboxSelected>>', lambda e: self.show_prjb_frame())

            # In Project B frame, when select type (NEW, REG, REVIEW), disable testing type radiobox accordingly
        self.prjb_frames[ProjectBUnitTest].type.bind('<<ComboboxSelected>>', lambda e: self.select_type())

        vcmd = self.prjb_frames[ProjectBUnitTest].register(self.callback)
        self.prjb_frames[ProjectBUnitTest].version_entry.config(validate='all', validatecommand=(vcmd, '%S'))
        # End Project B frame binding

    def callback(self, S):
        if str.isdigit(S) or S == "." or S == "":
            return True
        else:
            return False
    # Closing popup
    def cancel(self):
        self.addtasks_window.destroy()

    # Function for switching project frame
    def project_switch_frame(self):
        self.frames = {}
        for f in (StartFrame, Common, ProjectA, ProjectB, ProjectC, ProjectLabVIEW, ProjectCANoe, ProjectSound2Light, ProjectUnassigned):
            frame = f(self.addtasks_window.main_frame, self)
            self.frames[f] = frame
            frame.grid(row = 0, column = 0, sticky ="nsew")        
        ## TODO1 in version 1.1.4: Optimized this if else
        if self.proj == "Project B":
            self.current_project = ProjectB
        elif self.proj == " Project C":
            self.current_project = ProjectC
        elif self.proj == "Project A":
            self.current_project = ProjectA
        elif self.proj == " Project LabVIEW":
            self.current_project = ProjectLabVIEW
        elif self.proj == "Project Sound2Light":
            self.current_project = ProjectSound2Light
        elif self.proj == "Project CANoe":
            self.current_project = ProjectCANoe
        else:
            self.current_project = StartFrame
        frame = self.frames[self.current_project]
        frame.tkraise()

        self.frames[ProjectC].task_cat_entry['values'] = heading.ConfigCategory().projectC

    # Function for switching ProjectB task frame
    def prjb_switch_frame(self):
        self.prjb_frames = {}
        for f in (ProjectBDevelopment, ProjectBUnitTest):
            prjb_frame = f(self.frames[ProjectB].main_frame, self)
            self.prjb_frames[f] = prjb_frame
            prjb_frame.grid(row = 0, column = 0, sticky ="nsew")
        self.current_prjb_type = ProjectBDevelopment
        prjb_frame = self.prjb_frames[self.current_prjb_type]
        prjb_frame.tkraise()

    # Show chosen project frame function
    def show_frame(self):
        # Get current chosen frame
        self.current_project = getattr(sys.modules[__name__],self.addtasks_window.selected_project.get().replace(" ",""))
        frame = self.frames[self.current_project]

        #Switching to frame
        frame.tkraise()


    # Show chosen ProjectB task frame function
    def show_prjb_frame(self):
        # Get current chosen frame, if "Development"
        if (self.frames[ProjectB].selected_type.get() in ['Development', "Common", "N/A"] ):
            self.current_prjb_type = ProjectBDevelopment

        # If Unit Test
        else:
            self.current_prjb_type = ProjectBUnitTest
        prjb_frame = self.prjb_frames[self.current_prjb_type]

        # Switching to frame
        prjb_frame.tkraise()
        

    # Get current project frame function
    def get_frame(self, frame_class):
        return self.frames[frame_class]
    
    # Disable or active testing type according to NEW, REG, REVIEW selection
    def select_type(self):
        self.choose_type = self.prjb_frames[ProjectBUnitTest].type.get()
        if (self.choose_type != 'REVIEW'):
            self.prjb_frames[ProjectBUnitTest].TV.config(state=ACTIVE)
            self.prjb_frames[ProjectBUnitTest].TS.config(state=ACTIVE)
            self.prjb_frames[ProjectBUnitTest].TE.config(state=ACTIVE)
            self.prjb_frames[ProjectBUnitTest].TestID.config(state=ACTIVE)
        else:
            self.prjb_frames[ProjectBUnitTest].TV.config(state=DISABLED)
            self.prjb_frames[ProjectBUnitTest].TS.config(state=DISABLED)
            self.prjb_frames[ProjectBUnitTest].TE.config(state=DISABLED)
            self.prjb_frames[ProjectBUnitTest].TestID.config(state=DISABLED)
            self.prjb_frames[ProjectBUnitTest].checkvarTV.set(0)
            self.prjb_frames[ProjectBUnitTest].checkvarTS.set(0)
            self.prjb_frames[ProjectBUnitTest].checkvarTE.set(0)
            self.prjb_frames[ProjectBUnitTest].checkvarTestID.set(0)
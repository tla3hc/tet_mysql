from tkinter import *
from utils.date import Date

class WindowController:

    def show_hide_subwindow(subwindow, show_button):
        if subwindow.winfo_viewable():
            subwindow.withdraw()  # Hide the subwindow
        else:
            subwindow.deiconify()  # Show the subwindow

    def init_elements(self, table,combobox_week, combobox_year):
        self.table = table
        self.combobox_week = combobox_week
        self.combobox_year = combobox_year

    def change_date_headings(self, event):
        new_headings = ('Project','Task description','Category', 'Comment','Estimation Effort','No.Reqs','Deadline','Review Finding','Priority','Start Date','End Date','Status','Effort by month','Total Actual Effort', 'Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday')
        self.table["columns"] = new_headings
        self.table.heading("#0",text = "No.")
        for idx, heading_text in enumerate(new_headings):
            if heading_text in ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']:
                self.table.heading("#{}".format(idx+1), text=Date.get_date(heading_text, self.combobox_week.get(), self.combobox_year.get()))
            else:
                self.table.heading("#{}".format(idx+1), text=heading_text)
        # Set the column widths dynamically based on the headings
        for idx in range(len(new_headings)+1):
            self.table.set_column_width(idx)
# Import the necessary libraries/modules for creating GUI elements
import tkinter as tk
from tkinter.font import Font
from tkinter import ttk,Label,Entry, messagebox
from datetime import *
from configs.config_user import *


# Define a class for creating an input field with a label

class CSInput(tk.Frame):
    def __init__(self, parent, label_text, **kwargs):
        super().__init__(parent)
        
        self.label = Label(self, text=label_text)
        self.label.pack(side=tk.LEFT)
        
        self.entry = Entry(self, **kwargs)
        self.entry.pack(side=tk.LEFT)
    
    def get(self):
        return self.entry.get()
    
    def set(self, value):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, value)

class CSCombobox(tk.Frame):
    def __init__(self, parent, label_text, values, **kwargs):
        super().__init__(parent)
        
        self.label = Label(self, text=label_text)
        self.label.pack(side=tk.LEFT)
        
        self.combobox = ttk.Combobox(self, values=values, **kwargs)
        self.combobox.pack(side=tk.LEFT)
    
    def get(self):
        return self.combobox.get()
    
    def set(self, value):
        self.combobox.set(value)
        
    def set_width(self, width):
        self.combobox.config(width = width)

    
    
# Define a class for creating a Treeview element
class WindowTreeview(ttk.Treeview):
    def __init__(self, master=None, columns=(), **kw):
        super().__init__(master, columns=columns, **kw)
        self.setup_columns(columns)
        self.bind("<Double-1>", self.on_double_click)

    def setup_columns(self, columns):
        self.heading("#0",text = "No.")
        for idx, heading_text in enumerate(columns):
            self.heading("#{}".format(idx+1), text=heading_text)

        # Initialize a font to measure text width
        self.font = Font()

        # Set the column widths dynamically based on the headings
        for idx in range(len(columns)+1):
            self.set_column_width(idx)

    def set_column_width(self, idx):
        text = self.heading("#{}".format(idx), "text")
        width = self.font.measure(text) + 20  # Add some padding
        min_width = max(width, 20)  # Minimum width (adjust as needed)
        self.column("#{}".format(idx), width=width, minwidth=min_width)

    def insert_value(self, value):
        self.insert(parent="",
                    index=tk.END,
                    text=self.get_row_count(),
                    values = value)
        
    def get_row_count(self):
        return len(self.get_children())    

    def on_double_click(self, event):
        region_clicked = self.identify_region(event.x, event.y)
        print(region_clicked)
   
        if region_clicked not in ("tree", "cell"):
            self.entry_edit.destroy()
            return
        
        column_clicked = self.identify_column(event.x)
        column_clicked_index = int(column_clicked[1:]) - 1

        selected_iid = self.focus()
        selected_values = self.item(selected_iid)

        if column_clicked =="#0":
            selected_text = selected_values.get("text")
        else:
            selected_text = selected_values.get("values")[column_clicked_index]

        self.column_box = self.bbox(selected_iid, column_clicked)

        self.entry_edit = ttk.Entry(self.master,width=self.column_box[2])

        self.entry_edit.editing_column_index = column_clicked_index
        self.entry_edit.editing_item_iid = selected_iid

        self.entry_edit.insert(0, selected_text)
        self.entry_edit.select_range(0, tk.END)

        self.entry_edit.focus()
        self.bind("<Leave>", self.on_focus_out_1)
        self.entry_edit.bind("<FocusOut>", self.on_focus_out_2)
        self.entry_edit.place(x=self.column_box[0],
                         y=self.column_box[1],
                         w=self.column_box[2],
                         h=self.column_box[3])
        print(self.column_box)

    def on_focus_out_1(self, event):
        if (((self.column_box[0] <= event.x) & (event.x < (self.column_box[0] + self.column_box[2]))) & ((self.column_box[1] <= event.y) & (event.y < (self.column_box[1] + self.column_box[3])))):
            return
        else:
            self.entry_edit.destroy()

    def on_focus_out_2(self, event):
        self.entry_edit.destroy()

class CSTreeView(ttk.Treeview):
    index = 0
    selected_row = ''
    selected_col = ''
    cell_edited = False
    cell_value = ''
    
    def __init__(self, master=None, columns=(), **kw):
        super().__init__(master, columns=columns, **kw)
        self.init_column(columns)
        self.bind("<Double-1>", self.on_double_click)
        # self.bind("<Button-1>", self.save_edited_value, add= "+")
        self.edited_values = {}

    def init_column(self, columns):
        self.heading("#0",text = "No.")
        for idx, heading_text in enumerate(columns):
            self.heading("#{}".format(idx+1), text=heading_text)
        # Initialize a font to measure text width
        self.font = Font()
        # Set the column widths dynamically based on the headings
        for idx in range(len(columns)+1):
            self.set_column_width(idx)

    def set_column_width(self, idx):
        # Check if this column is "Task description" (assuming it's the second column, adjust if needed)
        if idx == 1:  # Assuming "Task description" is the second column; change if it’s another index
            text = self.heading(f"#{idx}", "text")
            width = self.font.measure(text) + 150  # Adjust initial width as needed
            self.column(f"#{idx}", width=width, minwidth=200, stretch=False)  # Allow resizing
        else:
            text = self.heading(f"#{idx}", "text")
            width = self.font.measure(text) + 20  # Fixed width with padding
            self.column(f"#{idx}", width=width, minwidth=width, stretch=True)

    def insert_value(self, value, tag='normal'):
        self.insert(parent="",
                    index=tk.END,
                    iid=self.index,
                    text=self.get_row_count(),
                    values = value,
                    tags=tag)
        self.index += 1
    
    def clear_index(self):
        self.index = 0
        
    # Delete value
    def delete_value(self, value):
        pass
                
    def get_row_count(self):
        return len(self.get_children())
    
    def on_double_click(self, event):
        self.invalid_effort = False
        region_clicked = self.identify_region(event.x, event.y)
        if region_clicked not in ("tree", "cell"):
        # if region_clicked not in ("cell"):
            self.entry_edit.destroy()
            return
        
        column_clicked = self.identify_column(event.x)
        column_clicked_index = int(column_clicked[1:]) - 1

        selected_iid = self.focus()
        selected_values = self.item(selected_iid)

        if column_clicked =="#0":
            selected_text = selected_values.get("text")
        else:
            selected_text = selected_values.get("values")[column_clicked_index]

        self.original_value = selected_text  # Store the old value
        
        self.column_box = self.bbox(selected_iid, column_clicked)

        self.entry_edit = ttk.Entry(self.master,width=self.column_box[2])

        self.entry_edit.editing_column_index = column_clicked_index
        self.entry_edit.editing_item_iid = selected_iid

        self.entry_edit.insert(0, selected_text)
        self.entry_edit.select_range(0, tk.END)

        self.entry_edit.focus()
        self.bind("<Leave>", self.on_focus_out_1)          
        self.entry_edit.bind("<FocusOut>", self.on_focus_out_2)
        self.entry_edit.bind("<Leave>", self.on_focus_out_2, add= "+") 
        self.entry_edit.bind("<Return>", self.on_focus_out_2, add= "+")
        # self.entry_edit.bind("<Button-1>", self.on_focus_out_1, add= "+")        
        self.entry_edit.place(x=self.column_box[0],
                         y=self.column_box[1],
                         w=self.column_box[2],
                         h=self.column_box[3])
                
        self.selected_row = selected_iid
        self.selected_col = column_clicked_index        
        self.cell_edited = True                        
        
    def save_edited_value(self):
        try:
            if hasattr(self, 'entry_edit'):
                edited_text = self.entry_edit.get()
                edited_text = edited_text.replace(",", ".")
                self.cell_value = edited_text
                if edited_text == self.original_value:
                    self.entry_edit.destroy() 
                    return
                selected_iid = self.entry_edit.editing_item_iid
                # self.selected_row = selected_iid
                column_index = self.entry_edit.editing_column_index
                # self.selected_col = column_index
                values = self.item(selected_iid, option='values')
                values = list(values)
                # print(values)                                
                
                if column_index in [1, 3]:
                    self.entry_edit.destroy() 
                    return
                elif column_index in [4, 5, 6, 7, 8]:
                    if not self.is_num(edited_text):
                        self.invalid_effort = 1
                        self.entry_edit.destroy() 
                        return

                    if float(edited_text) > 8:
                        self.invalid_effort = 2 
                        self.entry_edit.destroy()  
                        return

                    if values[2] == 'Leave':
                        if edited_text == '0' or edited_text == '4' or edited_text == '8':
                            pass
                        else:
                            self.invalid_effort = 3
                            self.entry_edit.destroy()  
                            return
                        
                elif column_index in [9, 10, 11, 12]:
                    # if (values[1] == "Project B" and values[2] != 'Development') or values[1] == "Project C" :
                    if (values[1] == "Project B" and values[2] in ["NEW_TS", "NEW_TV", "NEW_TE", "REG_TS", "REG_TV", "REG_TE", "REVIEW"]) or values[1] == "Project C" :
                        pass
                    else:
                        self.invalid_effort = 4
                        self.entry_edit.destroy() 
                        return

                    if not self.is_num(edited_text):
                        self.invalid_effort = 1
                        self.entry_edit.destroy() 
                        return
                elif column_index in [13, 14]:
                    try:
                        date = datetime.strptime(edited_text, '%d/%m/%Y').strftime('%d/%m/%Y')
                    except:
                        print('Wrong datetime format, must be DD/MM/YYYY')
                        self.invalid_effort = 5
                        self.entry_edit.destroy()
                        return
                    else:
                        edited_text = str(date)[0:10]
                values[column_index] = edited_text
                self.item(selected_iid, values=values)
                self.edited_values[selected_iid] = True
                      # Mark the item as edited
        except Exception:
            pass
        self.entry_edit.destroy()    
    
        
    def on_focus_out_1(self, event):
        # Check if it is outside the cell (x,y)
        if (((self.column_box[0] <= event.x) & (event.x < (self.column_box[0] + self.column_box[2]))) & ((self.column_box[1] <= event.y) & (event.y < (self.column_box[1] + self.column_box[3])))):
            return
        else:
            self.save_edited_value()

    def on_focus_out_2(self, event):
        self.save_edited_value()
        if self.invalid_effort == 1:
            messagebox.showinfo("Error", "This field must be a number !")     
        elif self.invalid_effort == 2:
            messagebox.showinfo("Error", "Effort hours in 1 day must equal or less than 8 hours !")
        elif self.invalid_effort == 3:
            messagebox.showinfo("Error", "Invalid effort for Leave. Only allow 4 or 8 hours !")
        elif self.invalid_effort == 4:
            messagebox.showinfo("Error", "This project do not have this field !")
        elif self.invalid_effort == 5:
            messagebox.showinfo("Error", "Invalid date format (DD/MM/YYYY) !")

        self.invalid_effort == 0
        
    def is_num(self, input_str):
        if input_str.isdigit():
            return True
        elif input_str.replace(".","").replace(",","").isnumeric():
            return True
        else:
            return False
        
    def get_cell(self):
        store_row = self.selected_row
        store_col = self.selected_col
        store_val = self.cell_value
        self.selected_row = None
        self.selected_col = None
        return store_row, store_col, store_val
    
    def detect_cell_edit(self):
        return self.cell_edited
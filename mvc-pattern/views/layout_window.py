import tkinter as tk
from views.window import WindowController

class LayoutWindow:
    def __init__(self,root,labels,show_button,padx=10, pady=1):

        self.root = tk.Toplevel(root)
        self.root.title('Change Layout')
        self.root.withdraw()
        self.root.protocol("WM_DELETE_WINDOW", lambda: WindowController.show_hide_subwindow(self.root,show_button))

        self.checkbuttons = []
        self.vars = []

        # Loop through each label to create and place Label and Checkbutton widgets
        for idx, label in enumerate(labels):
            var = tk.IntVar()
            label_widget = tk.Label(self.root, text=label)
            checkbutton = tk.Checkbutton(self.root, variable=var)

            # Left-justify labels and right-justify checkboxes
            label_widget.grid(row=idx, column=1, padx=padx, pady=pady, sticky='w')
            checkbutton.grid(row=idx, column=0, padx=padx, pady=pady, sticky='e')

            self.checkbuttons.append(checkbutton)
            self.vars.append(var)

        # Create an OK button and place it
        ok_button = tk.Button(self.root, text='OK', command=self.print_values_and_close)
        ok_button.grid(row=len(labels), columnspan=2, padx=10, pady=10)

    # Function to print checkbox values and close the window
    def print_values_and_close(self):
        print(f"Checkbox Values: {self.get_values()}")
        self.root.destroy()

    # Function to get the checkbox values
    def get_values(self):
        return [var.get() for var in self.vars]
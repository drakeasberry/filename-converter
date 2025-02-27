# Imports
import os
import glob
import logging
from lib.Scripts._common_os import close_action
import tkinter as tk
from tkinter import filedialog, messagebox

# Set up logging format
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class FileSearchUI:
    """Handle tkinter UI setup."""

    def __init__(self,root):
        """Initialize UI components"""

        self.root = root
        self.controller = None
        self.root.title("File Search")

    def setup(self, controller):
        """Assign the controller after initialization"""
        self.controller = controller
        self.create_widgets()
        self.update_commands()

    def create_widgets(self):
        """Creates and places UI components in tkinter window"""

        # Directory Input
        tk.Label(self.root, text="Directory to search:").grid(row=0, column=0, padx=10, pady=5)
        self.entry_directory = tk.Entry(self.root, width=50)
        self.entry_directory.grid(row=0, column=1, padx=10, pady=5)
        self.browse_button = (tk.Button(self.root, text="Browse", command=lambda: print("Controller not set yet")))
        self.browse_button.grid(row=0, column=2, padx=10, pady=5)

        # File Extension Input
        tk.Label(self.root, text="File extension to search for:").grid(row=1, column=0, padx=10, pady=5)
        self.entry_extension = tk.Listbox(self.root,selectmode=tk.MULTIPLE, height=6, width=20)
        self.entry_extension.grid(row=1, column=1, padx=10, pady=5)

        # Set options for extensions
        self.allowable_extensions = ['.txt', '.json', '.dwg', '.*']
        for ext in self.allowable_extensions:
            self.entry_extension.insert(tk.END, ext)

        # Buttons
        self.search_button = tk.Button(self.root, text="Start Search", command=lambda: print("Controller not set yet"))
        self.search_button.grid(row=2, column=0, columnspan=3, pady=10)
        tk.Button(self.root, text="Close Script", command=close_action).grid(row=2, column=1, columnspan=3, pady=10)

    def update_commands(self):
        """Update button commands now that controller is available"""
        if self.controller:
            self.browse_button.config(command=self.controller.browse_directory)
            self.search_button.config(command=self.controller.start_search)

class FileSearchController:
    """Handles event logic and interactions between tkinter UI and functions"""

    def __init__(self,ui):
        """Stores reference to UI"""
        self.ui = ui

    def browse_directory(self):
        """Opens file explorer and sets the selected directory in the entry box"""
        directory = filedialog.askdirectory()
        if directory:
            self.ui.entry_directory.delete(0, tk.END)
            self.ui.entry_directory.insert(0, directory)

    def search_files(self,entry_directory, entry_extension):
        """Takes the user input from dialog box and validates directory. It then searches the files in the
        directory for matches to the file extension given by user. It then displays results."""

        directory = entry_directory
        file_extension = entry_extension.curselection()  # Get 1 or more selected extensions from user

        # Check to see that directory exists
        if not os.path.isdir(directory):
            messagebox.showerror("Error", f"The directory '{directory}' does not exist.")
            return

        # Ensure at least one extension is selected
        if not file_extension:
            messagebox.showerror("Error", "Please select at least one extension to search for.")

        # Get selected extensions
        selected_extension = [entry_extension.get(i) for i in file_extension]

        # Collect files in dictionary when multiple selection is enabled
        files_found = {ext: [] for ext in selected_extension}

        # Adds values to dictionary value list based on extension being key
        file_count = 0
        for ext in selected_extension:
            search_pattern = os.path.join(directory, f"*{ext}")
            files = glob.glob(search_pattern)
            print(files)
            files_found[ext].extend(files)
            file_count += len(files_found[ext])

        print(file_count)
        # Prepare Display for the results of search
        if files_found:
            result_text = ""
            for ext, files in files_found.items():
                count = len(files)
                if count > 0:
                    if ext != '.*':
                        result_text += f"Extension: {count} {ext} file(s) were found\n"
                        result_text += "\n".join(files) + "\n\n"
                    else:
                        total_files = f"Total Files: {count} file(s) were found in the directory with any extension through wildcard selection."
                else:
                    result_text += f"Extension: No {ext} files were not found.\n\n"

        # Dispaly the formatted results
        if result_text:
            try:
                all_file_option_omitted = total_files
            except NameError:
                result_text += f"\nTotal Files: " + str(
                    file_count) + " file(s) were found matching selection criteria where wildcard was not used."
                messagebox.showinfo("Search Results", result_text)
            else:
                result_text += f"\nTotal Files: " + str(
                    file_count - count) + " file(s) were found matching selection criteria where wildcard was not used."
                result_text += "\n" + total_files
                messagebox.showinfo("Search Results", result_text)
        else:
            messagebox.showinfo("No Results", "No files were found for the selected extension")

    def start_search(self):
        """Triggers file search based on user input"""
        directory = self.ui.entry_directory.get().strip()
        extensions = self.ui.entry_extension
        self.search_files(directory, extensions)

# Function to create and return the Tkinter UI Instance
def tkinter_ui():
    root = tk.Tk()
    ui = FileSearchUI(root)
    controller = FileSearchController(ui)
    ui.setup(controller)
    return ui
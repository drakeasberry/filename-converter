# Imports
from lib.Scripts._file_finder import search_files, browse_directory
from lib.Scripts._common_os import close_action
import tkinter as tk

def main_ui_file_extension():
    """Sets up the UI"""
    # Set global variables
    global entry_directory
    global entry_extension

    # Set up the main window
    root = tk.Tk()
    root.title("File Search")

    # Label for Directory input
    label_directory = tk.Label(root, text="Directory to search:")
    label_directory.grid(row=0, column=0, padx=10, pady=5)

    # Entry for Directory Path
    entry_directory = tk.Entry(root, width=50)
    entry_directory.grid(row=0, column=1, padx=10, pady=5)

    # Search button for user
    button_browse = tk.Button(root, text="Browse", command=lambda: browse_directory(entry_directory))
    button_browse.grid(row=0, column=2, padx=10, pady=5)

    # Label for file extension
    label_extension = tk.Label(root, text="File extension to search for:")
    label_extension.grid(row=1, column=0, padx=10, pady=5)

    # Entry for File Extension
    #entry_extension = tk.Entry(root, width=20) # User types extension
    #entry_extension = ttk.Combobox(root, values=allowable_extensions,) #User can select single value from drop-down
    entry_extension = tk.Listbox(root,selectmode=tk.MULTIPLE, height=6, width=20)
    entry_extension.grid(row=1, column=1, padx=10, pady=5)

    # Set options for extensions
    allowable_extensions = ['.txt', '.json', '.dwg', '.*']
    for ext in allowable_extensions:
        entry_extension.insert(tk.END, ext)

    # Search button for user
    button_search = tk.Button(root, text="Start Search", command=lambda: search_files(entry_directory,entry_extension))
    button_search.grid(row=2, column=0, columnspan=3, pady=10)

    # Close button for user
    button_close = tk.Button(root, text="Close Script", command=close_action)
    button_close.grid(row=2, column=1, columnspan=3, pady=10)

    root.mainloop()

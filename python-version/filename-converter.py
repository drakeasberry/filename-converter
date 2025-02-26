# filename converter
# Import Libraries
import os
import glob
import tkinter as tk
from tkinter import messagebox, filedialog


def manual_find():
    """This allows user to type responses and find files matching the description given.
    Note: Do not use quotation marks on file path or extension."""
    # Ask user for input
    directory = input("What directory do you want to search?: ")
    file_extension = input("Enter the filetype extension that you would like to search for: ")

    # Check if the directory exists
    if not os.path.isdir(directory):
        print(f"The directory '{directory}' does not exist")
    else:
        # Use glob to find files matching the extension given by user in valid directory
        search_pattern = os.path.join(directory, f"*{file_extension}")
        files_found = glob.glob(search_pattern)

        # Check to see if any files match the search parameters
        if files_found:
            print(f"Found the following files with the '{file_extension}' extension:")
            for file in files_found:
                print(file)
        else:
            print(f"No files with the '{file_extension}' extension were found in {directory}.")

# Uncomment to find files by manually entering search criteria
#find_files = manual_find()

# Utilize UI to interact with user
def browse_directory():
    """Opens a dialog box for user to select directory of interest."""
    directory = filedialog.askdirectory()
    if directory:
        entry_directory.delete(0,tk.END)
        entry_directory.insert(0,directory)

def search_files():
    """Takes the user input from dialog box and validates directory. It then searches the files in the
    directory for matches to the file extension given by user. It then displays results."""
    directory = entry_directory.get().strip()
    file_extension = entry_extension.get().strip()

    # Check to see that directory exists
    if not os.path.isdir(directory):
        messagebox.showerror("Error", f"The directory '{directory}' does not exist.")
        return

    # Use glob to find files with user extension
    search_pattern = os.path.join(directory, f"*{file_extension}")
    files_found = glob.glob(search_pattern)

    # Display the results of search
    if files_found:
        result_text = "\n".join(files_found)
        messagebox.showinfo("Search Results", f"Found the following {len(files_found)} files:\n\n{result_text}")
    else:
        messagebox.showinfo("No Results", f"No files with the '{file_extension}' extension were found in {directory}")

def main_ui():
    """Sets up the UI"""
    # Set up the main window
    root = tk.Tk()
    root.title("File Search")

    # Label for Directory input
    label_directory = tk.Label(root, text="Directory to search:")
    label_directory.grid(row=0, column=0, padx=10, pady=5)

    # Entry for Directory Path
    global entry_directory
    entry_directory = tk.Entry(root, width=50)
    entry_directory.grid(row=0, column=1, padx=10, pady=5)

    # Search button for user
    button_browse = tk.Button(root, text="Browse", command=browse_directory)
    button_browse.grid(row=0, column=2, padx=10, pady=5)

    # Label for file extension
    label_extension = tk.Label(root, text="File extension to search for:")
    label_extension.grid(row=1, column=0, padx=10, pady=5)

    # Entry for File Extension
    global entry_extension
    entry_extension = tk.Entry(root, width=20)
    entry_extension.grid(row=1, column=1, padx=10, pady=5)

    # Search button for user
    button_search = tk.Button(root, text="Start Search", command=search_files)
    button_search.grid(row=2, column=0, columnspan=3, pady=10)

    root.mainloop()

main_ui()
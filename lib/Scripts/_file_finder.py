# filename converter
# Import Libraries
import os
import glob
import tkinter as tk
from tkinter import messagebox, filedialog, ttk

# Run in manual mode (Advanced User or Testing)
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
    #file_extension = entry_extension.get().strip() # For use with typed user input or single drop-down selection
    file_extension = entry_extension.curselection() # Get 1 or more selected extensions from user

    # Check to see that directory exists
    if not os.path.isdir(directory):
        messagebox.showerror("Error", f"The directory '{directory}' does not exist.")
        return

    # Ensure at least one extension is selected
    if not file_extension:
        messagebox.showerror("Error", "Please select at least one extension to search for.")

    # Use glob to find files with user extension when typed or selected from single select drop-down
    #search_pattern = os.path.join(directory, f"*{file_extension}")
    #files_found = glob.glob(search_pattern)

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
                    #messagebox.showinfo("Search Results", f"Found the following {len(files_found)} files:\n\n{result_text}")
                else:
                    total_files = f"Total Files: {count} file(s) were found in the directory with any extension through wildcard selection."
            else:
                #messagebox.showinfo("No Results", f"No files with the '{file_extension}' extension were found in {directory}")
                result_text += f"Extension: No {ext} files were not found.\n\n"

    # Dispaly the formatted results
    if result_text:
        try:
            all_file_option_omitted = total_files
        except NameError:
            result_text += f"\nTotal Files: " + str(file_count) + " file(s) were found matching selection criteria where wildcard was not used."
            messagebox.showinfo("Search Results", result_text)
        else:
            result_text += f"\nTotal Files: " + str(file_count-count) + " file(s) were found matching selection criteria where wildcard was not used."
            result_text += "\n" + total_files
            messagebox.showinfo("Search Results", result_text)
    else:
        messagebox.showinfo("No Results", "No files were found for the selected extension")

def close_action():
    root.destroy()

def main_ui():
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
    button_browse = tk.Button(root, text="Browse", command=browse_directory)
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
    button_search = tk.Button(root, text="Start Search", command=search_files)
    button_search.grid(row=2, column=0, columnspan=3, pady=10)

    # Close button for user
    button_close = tk.Button(root, text="Close Script", command=close_action)
    button_close.grid(row=2, column=1, columnspan=3, pady=10)

    root.mainloop()

main_ui()
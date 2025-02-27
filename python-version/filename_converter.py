# Imports
from lib.Scripts._tkinter_setup import tkinter_ui

# Main
def main():
    """Starts the Tkinter UI"""
    window = tkinter_ui()
    window.root.mainloop()

if __name__ == "__main__":
    main()

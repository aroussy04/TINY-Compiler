"""
TINY Compiler - Main Entry Point

This module serves as the main entry point for the TINY compiler application.
It launches the GUI interface for the TINY compiler.
"""

import tkinter as tk
from gui import TinyCompilerGUI

def main():
    """
    Main function to start the application.
    """
    root = tk.Tk()
    app = TinyCompilerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 
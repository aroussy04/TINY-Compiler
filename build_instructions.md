# Building the TINY Compiler Executable

This document contains instructions for building the TINY compiler as a Windows executable (.exe) file using PyInstaller.

## Prerequisites

Make sure you have PyInstaller installed:

```
pip install pyinstaller
```

## Building the Executable

To build the standalone executable, open a command prompt in the project directory and run:

```
pyinstaller --onefile --windowed --icon=icon.ico --name=TINY_Compiler main.py
```

This will create a single executable file in the `dist` folder.

### Options Explained

- `--onefile`: Create a single executable file instead of a directory.
- `--windowed`: Don't show a console window when running the application.
- `--icon=icon.ico`: Use the specified icon file for the executable (you need to create or provide an icon file first).
- `--name=TINY_Compiler`: Name the output executable "TINY_Compiler.exe".

## Adding an Icon

You can create or download an icon file (.ico) and place it in the project directory, then reference it in the PyInstaller command.

## Distributing the Application

After building, you can distribute the `TINY_Compiler.exe` file from the `dist` folder. Users will need to have the following to run your application:

- Windows operating system
- No additional dependencies (PyInstaller packages everything needed)

## Troubleshooting

If you encounter errors during build:

1. Make sure all required packages are installed.
2. Try running `pyinstaller --onefile --name=TINY_Compiler main.py` without the windowed option first to see any error messages.
3. Check the PyInstaller log files in the `build` directory.

## Example Usage

Once built, users can:

1. Double-click on `TINY_Compiler.exe` to launch the application.
2. Use the application's GUI to load, edit, and compile TINY language programs.
3. View the token list, syntax status, and syntax tree visualization. 
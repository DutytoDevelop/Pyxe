# Pyxe 🧚
***Python Tkinter GUI  + PyInstaller = Easy to use auto-compiler for your Python projects*** ▶️
 

## Table of Contents: 🤖
 - Compatibility
 - Project Folder Structure
 - Installing Requirements.txt List
 - How to Use
 - To-Do List
 - Credits

---

### Compatibility: ✔️
***Please review this section to see if you'll be able to use Pyxe on your machine.***
Because of my current setup, and the fact that PyInstaller only lets you compile executables on the same operating system you run it on which is understandable, I'll go ahead and inform the Mac and Linux users out there that Pyxe is now partially ready for use, but the ability to create an executable using the 'One Dir' option is not operable yet, so use the 'One File' in the Pyxe script and ensure you have the packages installed that lets PyInstaller run smoothly.

Message from the developers of PyInstaller:

> PyInstaller runs on Windows 8 and newer, Mac OS X 10.7 (Lion) and
> newer, and GNU/Linux requires the ***ldd*** terminal application
> 
> [PyInstaller] works out-of-the-box with any Python version 3.6-3.9
>
> A list of supported packages that PyInstaller is compatible with can be found [here](https://github.com/pyinstaller/pyinstaller/wiki/Supported-Packages), although most 
> packages will work out of the box with PyInstaller even if it's not listed.

*Source: [GitHub.com/PyInstaller/PyInstaller](https://github.com/pyinstaller/pyinstaller/tree/e20e74c03768d432d48665b8ef1e02511b16e4be)*
 
All PyInstaller requirements are located on the official website [PyInstaller.ReadTheDocs.io](https://pyinstaller.readthedocs.io/en/stable/requirements.html). As far as I know, there should not be any compatibility issues with using Tkinter, although I personally recommend using Python version 3+.

Both Tkinter and PyInstaller do run on Mac and Linux, so if you're interested and would like to jump into this project yourself, then you'll definitely want to start by heading to [http://www.pyinstaller.org/](http://www.pyinstaller.org/) to begin getting familiar with PyInstaller and check out the Tkinter GUI module at [https://docs.python.org/3/library/tkinter.html](https://docs.python.org/3/library/tkinter.html) if that interests you as well.

---

#### Project Folder Structure: 🐍
    (Folder | Filename):    Description:
    Pyxe:               Root project folder  
    -build_folder\:      Default build directory for PyInstaller  
    -ico\:               Favicon.ico that tkinter looks for when Pyxe starts  
    -temp\:              Default directory for the temp files PyInstaller creates  
    -test_scripts\:      Directory of test scripts you can compile to test Pyxe out  
    -requirements.txt:  Python modules required to run Pyxe  
    -main.py:           Pyxe auto-compiler program

---

#### How to Install Modules and Create Virtual Environment: ✨
After ensuring your using the desired Python installation, use a terminal to install the modules listed in the `requirements.txt` file provided within the project:

Setting Up Virtual Environment:
 1. Open up a terminal and set the current directory to where you'll be to creating the virtual environment. 
 2. Run `python3 -m venv pyxe-env` ('pyxe-env' can be anything you choose).
 3. On Windows, run: \
    `pyxe-env\Scripts\activate.bat` (again, replace 'pyxe-env' with the name of your virtual environment) \
    On Unix or MacOS, run: \
    `source tutorial-env/bin/activate`
 4. `pip install -r requirements.txt`

Install Modules Without Virtual Environment:
   NOTE: If you have a Linux system, please ensure that you have some packages installed that are not available through downloading the modules listed in 'requirements.txt'. Here are the packages you will need to install:
 ```
 sudo apt update
 sudo apt install python3-pip python3-tk python3-pil.imagetk
 ```
 1. `pip install -r requirements.txt`

---

### How to Use Pyxe 💫:

 1. Download or clone the Pyxe repository onto a machine.
 2. Set up a virtualenv configuration or use a global Python installation and install the required Python modules listed above.
 3. Run the '*main.py*' file in the project root directory and you should see a GUI that looks like the one below:

**Pyxe Screenshot:**

![Screenshot of the Pyxe GUI](https://github.com/DutytoDevelop/Pyxe/blob/main/test_scripts/Successful%20Builds/Pyxe_v2.PNG)

4. Before you begin compiling your Python project, please review the documentation online for PyInstaller to ensure you're bundling data into the executable correctly.


  **⚠️ IMPORTANT: ⚠️**
  --
If you're referencing a file or folder in your Python project and you plan on using the '-onefile' option, please use the following code snippet in your project so that PyInstaller can find the file and package it into the executable file correctly. Failing to do this may lead to your code not being able to run as desired.  

_Please see: https://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile for more details._

    # Code Snippet: Grabs the absolute path from the relative path (for packaging external files INTO the executable)  
    # Place or import this function in your project and be sure to use it when referencing a filepath. 
    
    import os, sys  
    def resource_path(relative_path):  
          """ Get absolute path to resource, works for dev and for PyInstaller """  
          base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))  
          return os.path.join(base_path, relative_path)
    
5. You may now begin compiling your Python file/project into an executable. The only required information that Pyxe needs is the filepath to the Python file. The remaining information is optional to input as PyInstaller has default values if no value is retrieved.
6. You'll either see green text notifying you that Pyxe is compiling the project or that an error occurred. If there's a problem with Pyxe and not PyInstaller itself, and you would like to point it out, then certainly do so by sending me a direct message. My GitHub is [DutytoDevelop](https://www.GitHub.com/DutytoDevelop/).
7. The executable will be placed in the designated 'build' folder located in the project root directory unless provided an alternative directory to place the executable in! 
8. If you're trying to package multiple files into the program, please include all files inside one data folder and ensure that you're using the while I work to implement the feature that'll allow being able to package data from multiple directories. Happy Compiling!

Successful compilation of test Python script I've provided in Pyxe repository:

![Successfully compiled PyGame example script](https://github.com/DutytoDevelop/Pyxe/blob/main/test_scripts/Successful%20Builds/Pyxe_Success_v2.PNG)
_Note: _

---

## To-Do:

 - 🚧 Implement system to be compatible with multiple operating systems
 - 🚧 Fix code to allow importing bundled data from multiple directories instead of just one

## Credit:

- Creators of [Python](https://www.python.org/)
- Creators of [PyInstaller](https://pyinstaller.readthedocs.io/) and [Tkinter](https://wiki.python.org/moin/TkInter)
- [Google](https://www.Google.com/)
- [GitHub](https://github.com/)
- [StackEdit](https://stackedit.io/) (Great online user interface to write and preview .MD files on the fly)
- Those on StackOverflow.com that help people every day with troubleshooting programming issues
- Everyone else who collaborated with me and assisted me ❤️


# Happy Compiling! 🎅

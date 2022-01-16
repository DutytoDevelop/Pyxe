#  ⚠ IMPORTANT ⚠:
#  If you're referencing a file or folder in your Python project, please use the following code snippet in your project
#  so that PyInstaller can find the file and package it into the executable file correctly. Failing to do this may lead
#  to your code not being able to run as desired.
#
#  Please see: https://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile for more details
#
#  Code Snippet: Grabs the absolute path from the relative path (for packaging external files INTO the executable)

# Modules that help tie the PyInstaller and Tkinter modules together 
import os
import platform
import logging
import webbrowser
import shutil
import sys
from threading import Thread

# GUI-related modules
import tkinter
from tkinter import filedialog, Tk, Grid, Radiobutton, BooleanVar, LabelFrame, END, Text, Toplevel, Menu, Canvas, messagebox
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Entry, Label, Button, Frame, OptionMenu
from win32api import GetSystemMetrics
import PIL.Image
from PIL import Image, ImageTk

# PyInstaller module that does the compiling
from PyInstaller.__main__ import run as pyxe_compiler


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


#  Global variables that can be accessed by any function in this Python file
project_dir = os.getcwd()
ico_directory = resource_path("ico")
pyxe_favicon = os.path.join(ico_directory, "favicon.ico")

#  Make GUI elements
class GUI:

    # Initialize GUI here
    def __init__(self):

        #  Modify root title & prevent empty Tkinter GUI window from appearing
        self.root = Tk()
        self.root.title("Pyxe Auto-Compiler")
        self.root.withdraw()

        # Popup that gets created when you click the 'About' menu option
        def about_popup():
            top = Toplevel()
            top.title("About Me")
            top.geometry = "500x400"
            top.resizable(False,False)
            top.iconbitmap(pyxe_favicon)

            about_labelframe = LabelFrame(top,labelanchor="nw",text="Developer Profile:",width=600,height=200,font=('',10))
            about_labelframe.pack(fill="both",expand=True,padx=3,pady=3)

            profile_photo = Image.open(resource_path(r"pyxe_resources\data\DutytoDevelop_Profile_Pic.png"))
            resized = profile_photo.resize((150,150))
            profile_photo_resize = ImageTk.PhotoImage(resized)

            canvas = Canvas(about_labelframe,height=150,width=150)
            canvas.create_image(75,75,image=profile_photo_resize)
            canvas.image = profile_photo_resize
            canvas.grid(row=1,column=1,padx=3,pady=(3,0),sticky="nsew")

            about_label = Label(about_labelframe,text="Name: Nicholas H.\nGitHub: DutytoDevelop",font=('',10,'bold'))
            about_label.configure(anchor="center", justify='center')
            about_label.grid(row=2,column=1,padx=3,pady=(0,3),sticky="nsew")
            return

        # Open default web browser to the Pyxe GitHub repository page
        def open_help_page():
            help_page_url = "https://GitHub.com/DutytoDevelop/Pyxe"
            webbrowser.open_new(help_page_url)

        self.menubar = Menu(self.root)
        self.optionmenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Options", menu=self.optionmenu)
        self.optionmenu.add_command(label="About...", command=about_popup)
        self.optionmenu.add_command(label="Help", command=open_help_page)
        self.optionmenu.add_separator()
        self.optionmenu.add_command(label="Exit", command=self.exit_compiler)
        self.root.config(menu=self.menubar)

        #  A grid frame that helps layout the widgets on the root window
        self.frame = Frame(self.root)
        Grid.rowconfigure(self.root, 0, weight=1)
        Grid.columnconfigure(self.root, 0, weight=1)
        self.frame.grid_columnconfigure(2, weight=1)

        #  These widgets make up the function allowing you to select a Python file to compile
        Label(self.frame, text='Python File:').grid(row=1, column=1, sticky="E")

        #  Variable that connects that's being typed to the textbox
        self.program_filepath_textbox = Entry(self.frame)
        self.program_filepath_textbox.configure(width=80, state="disabled")
        self.program_filepath_textbox.grid(row=1, column=2, sticky='EW', padx=(0, 5), pady=5, ipadx=5)

        self.file_selection_button = Button(self.frame, text='Select Python File',
                                            command=lambda: self.python_get_filepath_of_file(
                                                title="Select Python File",
                                                initialdir=project_dir,
                                                filetypes=[("Python File", "*.py")],
                                                element=self.program_filepath_textbox))
        self.file_selection_button.configure(width=20)
        self.file_selection_button.grid(row=1, column=3, padx=5, pady=5, sticky="EW")

        #  These widgets make up the function allowing you to select a picture to be the program's favicon
        Label(self.frame, text='Program Icon:').grid(row=2, column=1, sticky="E")

        self.icon_filepath_textbox = Entry(self.frame)
        self.icon_filepath_textbox.configure(width=80, state="disabled")
        self.icon_filepath_textbox.grid(row=2, column=2, sticky='EW', padx=(0, 5), pady=5, ipadx=5)

        self.python_icon_selector = Button(self.frame, text='Select Program Icon',
                                           command=lambda: self.python_get_filepath_of_file(
                                               title="Select Program Icon",
                                               initialdir=project_dir,
                                               filetypes=[("Pictures", "*.jpg;*.jpeg,*.png;*.svg;*.ico")],
                                               element=self.icon_filepath_textbox))
        self.python_icon_selector.configure(width=20)
        self.python_icon_selector.grid(row=2, column=3, padx=5, pady=5, sticky="EW")

        #  These widgets make up the function allowing you to give a name to the executable
        Label(self.frame, text='Program Name:').grid(row=3, column=1, sticky="E")

        self.program_name_textbox = Entry(self.frame)
        self.program_name_textbox.configure(width=80)
        self.program_name_textbox.grid(row=3, column=2, sticky='EW', padx=(0, 5), pady=5, ipadx=5)

        #  Radio button options will return a boolean and GUI converts that into '--onefile' or '--onedir' parameter
        self.radiobtn_compile_option = BooleanVar()

        self.onefile_compile = Radiobutton(self.frame, text="One File", variable=self.radiobtn_compile_option,
                                           value=True, command=None)
        self.onefile_compile.grid(row=3, column=3, sticky='W', padx=(0, 5), pady=5, ipadx=5)

        self.onedir_compile = Radiobutton(self.frame, text="One Dir", variable=self.radiobtn_compile_option,
                                          value=False, command=None)
        self.onedir_compile.grid(row=3, column=3, sticky='E', padx=(0, 5), pady=5, ipadx=5)
        self.radiobtn_compile_option.set(True)  # Set this option as the default option

        #  These widgets make up the function allowing you to select where you want to create the executable
        Label(self.frame, text='Build Folder:').grid(row=4, column=1, sticky="E")

        self.build_directory_textbox = Entry(self.frame)
        self.build_directory_textbox.configure(state='disabled')
        self.build_directory_textbox.grid(row=4, column=2, sticky='EW', padx=(0, 5), pady=5, ipadx=5)

        select_directory = Button(self.frame, text="Select Directory",
                                  command=lambda: self.set_directory_path(title="Select Directory",
                                                                          initialdir=project_dir,
                                                                          element=self.build_directory_textbox))
        select_directory.configure(width=20)
        select_directory.grid(row=4, column=3, sticky="EW", padx=10, pady=5, ipadx=5)

        #  These widgets make up the function allowing you to select where you add the data
        Label(self.frame, text='Data Folders:').grid(row=5, column=1, sticky="E")

        self.data_folder_directory_textbox = Entry(self.frame)
        self.data_folder_directory_textbox.configure(state='disabled')
        self.data_folder_directory_textbox.grid(row=5, column=2, sticky='EW', padx=(0, 5), pady=5, ipadx=5)

        add_data_folder = Button(self.frame, text="Add Folder",
                                 command=lambda: self.set_directory_path(title="Add Path",
                                                                         initialdir=project_dir,
                                                                         element=self.data_folder_directory_textbox,
                                                                         append_directory=True))
        add_data_folder.configure(width=8)
        add_data_folder.grid(row=5, column=3, sticky="W", padx=10, pady=5, ipadx=5)

        clear_data_folder = Button(self.frame, text="Clear",
                                 command=lambda: self.set_directory_path(title="Add Directory",
                                                                         initialdir=project_dir,
                                                                         element=self.data_folder_directory_textbox,
                                                                         append_directory=True))
        clear_data_folder.configure(width=8)
        clear_data_folder.grid(row=5, column=3, sticky="E", padx=10, pady=5, ipadx=5)

        #  These widgets make up the function that allows you to compile the executable
        self.compile_button = Button(self.frame, text="Compile",
                                     command=lambda: thread_function(function=self.compile_executable))
        self.compile_button.grid(row=6, column=1, columnspan=2, sticky='EW', padx=(10, 5), pady=5, ipadx=5)

        self.compilation_section = LabelFrame(self.frame, text='Console Output:', labelanchor="nw")
        self.compilation_section.configure(height=11)
        self.compilation_section.grid(row=7, column=1, columnspan=4, sticky="NESW", padx=10, pady=10)

        self.compiler_text = ScrolledText(self.compilation_section, yscrollcommand=True, bg='lightgrey', font=('Nimbus Mono L',9), fg='green')
        self.compiler_text.configure(height=11,state="disabled")
        self.compiler_text.bind("<Key>", lambda e: "break")
        self.compiler_text.yview_pickplace("end")
        self.compiler_text.pack(expand=True, fill="both", padx=5, pady=7)

        #  This widget make up the function allowing you to discontinue compiling the executable
        self.quit_button = Button(self.frame, text="Quit", command=lambda: self.exit_compiler())
        self.quit_button.grid(row=6, column=3, sticky='EW', padx=10, pady=5, ipadx=5)

        #  Expand self.frame to fit the root window
        self.frame.grid(sticky="nsew", padx=2, pady=2)

        #  GUI size and placement on the screen
        self.screen_width = GetSystemMetrics(0)
        self.screen_height = GetSystemMetrics(1)
        self.app_width = 800
        self.app_height = 430
        self.root.geometry(str(self.app_width) + "x" + str(self.app_height) + "+" + str(
            int((self.screen_width / 2) - (self.app_width / 2))) + "+" + str(
            int((self.screen_height / 2) - (self.app_height / 2))))

        #  The icon that appears in the corner of the executable
        self.root.iconbitmap(pyxe_favicon)

        #  Restricts the GUI from being resized
        self.root.resizable(False, False)

        #  Get rid of extra GUI window when creating dialog boxes
        self.root.deiconify()

    #  Grab filepath of Python file
    def python_get_filepath_of_file(self, title, initialdir, filetypes, element):
        self.title = title
        self.initialdir = initialdir
        self.filetypes = filetypes
        self.python_get_filepath = self.get_filepath_of_file(title, initialdir, filetypes)
        self.element = element
        self.element.configure(state="enabled")
        self.set_entrybox_text(element, self.python_get_filepath)
        self.element.configure(state="disabled")
        return

    #  Function that creates the PythonFile object with the data necessary to compile the executable
    def compile_executable(self):
        self.executable_info = PythonFile(python_filepath=self.get_entrybox_text(element=self.program_filepath_textbox),
                                          name=self.get_entrybox_text(element=self.program_name_textbox),
                                          favicon_path=self.get_entrybox_text(element=self.icon_filepath_textbox),
                                          build_directory=self.get_entrybox_text(element=self.build_directory_textbox),
                                          data_folder_present=self.get_entrybox_text(
                                              element=self.data_folder_directory_textbox),
                                          onefile_radiobtn_selected=self.radiobtn_compile_option.get())
        self.executable_info.make_exe()

    def exit_compiler(self):
        self.root.destroy()
        del self.executable_info
        exit()

    #  Display Tkinter GUI
    def run_autocompiler(self):
        self.root.mainloop()

    def get_radiobutton_value(self, element):
        self.element = element
        element.get()

    #  Return text inside of Tkinter Entry widget
    def get_entrybox_text(self, element):
        self.element = element
        element.configure(state="normal")
        entrybox_text = os.path.join(self.element.get())
        element.configure(state="disabled")
        return entrybox_text

    #  Set text inside of Tkinter Entry widget
    def set_entrybox_text(self, element: Text, text: str, append_text: bool = False):
        self.element = element
        self.text = text
        if (append_text is True):
            if (detected_os == 'windows'):
                seperator = ';'
            else:
                seperator = ':'
            if (self.get_entrybox_text(self.element) != ''):
                self.text = self.text
            else:
                self.text = seperator.join(self.get_entrybox_text(self.element), self.text)
            self.element.insert('end', self.text)
        else:
            self.element.delete(0, 'end')
            self.element.insert(0, self.text)
        return

    #  Return path of directory if it exists
    def get_directory_path(self, title, initialdir):
        #  If file doesn't exist, continue prompting file selection
        self.selected_directory_or_file = filedialog.askdirectory(title=title, initialdir=initialdir)
        #  Return filepath
        return self.selected_directory_or_file

    #  Set Tkinter's directory selection dialog box to given directory
    def set_directory_path(self, title, initialdir, element, append_directory=False):
        self.directory_path = self.get_directory_path(title, initialdir)
        element.configure(state="enabled")
        self.set_entrybox_text(element, self.directory_path, append_text=append_directory)
        element.configure(state="disabled")
        return

    #  Return filepath for the file
    def get_filepath_of_file(self, title, initialdir, filetypes):
        #  If file doesn't exist, continue prompting file selection
        self.title = title
        self.initialdir = initialdir
        self.filetypes = filetypes
        self.selected_file = filedialog.askopenfilename(title=title,
                                                        initialdir=initialdir,
                                                        filetypes=filetypes)

        return self.selected_file


#  PythonFile class object that contains the main components to collect the data to feed into PyInstaller
class PythonFile:

    #  Initialize the PythonFile object with the data
    def __init__(self, python_filepath, name, onefile_radiobtn_selected=True, build_directory=None,
                 favicon_path=False,
                 data_folder_present=False, hidden_imports=None):
        self.python_filepath = f'{python_filepath}'
        self.workpath = f'--workpath={os.path.join(project_dir, "temp")}'
        self.specpath = f'--specpath={os.path.join(project_dir, "dist")}'
        self.cleanbuild = '--clean'
        self.windowed = '--windowed'
        #self.log_level = '--log-level=INFO' # Commented out since it's not needed for the STDOUT redirect & it also causes errors for PyInstaller
        self.console = '--noconsole'

        #
        if (onefile_radiobtn_selected is True):
            self.onefile_onedir_option = '--onefile'
        else:
            self.onefile_onedir_option = '--onedir'

        if (build_directory is not None and build_directory != ''):
            self.distpath = f'--distpath={os.path.join(build_directory)}'
        else:
            self.distpath = f'--distpath={os.path.join(project_dir, "build")}'

        '''
        #  If a picture was selected, Pyxe specifies the filepath of the .ico file here
        if (favicon_path is True and favicon_path != ''):
            self.favicon_path = f'--icon={favicon_path}'
        '''

        if (hidden_imports is True):
            self.hidden_imports = f'--hidden-import={hidden_imports}'

        #  If data folders were selected, then Pyxe specifies the directory of the data folders here (Default: [''])
        if (data_folder_present):
            if (len(data_folder_present) > 1):
                #  Specify OS
                self.data_folder_directories = []
                if (detected_os == 'Windows'):
                    self.data_folder_directories += f'--add-data={data_folder_present};{os.path.basename(data_folder_present)[1]}'
                else:
                    self.data_folder_directories += f'--add-data={data_folder_present}:{os.path.basename(data_folder_present)[1]}'

        if (name != ''):
            self.name = f'--name={name}'
        else:
            self.name = f'--name={os.path.split(os.path.splitext(python_filepath)[0])[-1]}'

    #  Convert any picture file to a favicon.ico icon file for the compiled executable
    def convert_to_ico(self, picture_filepath):
        self.picture_filepath = picture_filepath

        # If no .ico is being uploaded, then PyInstaller automatically sets its default .ico file
        if (os.path.splitext(picture_filepath)[1] == '.ico'):
            return picture_filepath

        #  Favicon filepath variable
        favicon_filepath = picture_filepath

        #  If picture_filepath is not already an .ico file, then convert file to an .ico file
        file_extension = os.path.splitext(favicon_filepath)[1]

        if (file_extension != '.ico'):
            # List comprehension creates (16,16) to (256,256) .ico file (2^n for n=4,5,6,7)
            icon_sizes = [(pow(2, size), pow(2, size)) for size in range(4, 8)]

            img = Image.open(favicon_filepath)
            favicon_filepath = os.path.join(ico_directory, "favicon.ico")
            img.save(favicon_filepath, sizes=icon_sizes)
        elif (file_extension == ""):
            return False

        return favicon_filepath

    #  Function that builds the Python project into an executable
    def make_exe(self):
        if Pyxe.get_entrybox_text(Pyxe.program_filepath_textbox) == '':
            pass
        else:
            Pyxe.compiler_text.configure(state="normal")
            Pyxe.compiler_text.delete("1.0", END)
            Pyxe.compiler_text.configure(state="disabled")
            pyxe_compiler(self.__dict__.values())
            os.startfile(Pyxe.executable_info.distpath.split("=")[1])
            shutil.rmtree(Pyxe.executable_info.specpath.split("=")[1])
        return


class IODirector(object):
    global Pyxe
    def __init__(self, text_area):
        Pyxe.compiler_text = text_area

class StdoutDirector(IODirector):
    global Pyxe
    def write(self, msg):
        Pyxe.compiler_text.configure(state="normal")
        Pyxe.compiler_text.insert(END, msg)
        Pyxe.compiler_text.see(END)
        Pyxe.compiler_text.configure(state="disabled")
    def flush(self):
        pass

#  Allows GUI to continue running when you click 'Compile'
def thread_function(function, **kwargs):
    global Pyxe
    if (isinstance(function, str)):
        compiler_thread = Thread(target=eval(function))
    else:
        compiler_thread = Thread(target=function, args=(kwargs))
    sys.stdout = StdoutDirector(Pyxe.compiler_text)
    # configure the nameless "root" logger to also write           # added
    # to the redirected sys.stdout                                 # added
    logger = logging.getLogger()  # added
    console = logging.StreamHandler(stream=sys.stdout)  # added
    logger.addHandler(console)  # added
    compiler_thread.start()
    return compiler_thread

#  Main function that runs the auto-compiler
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)  # enable logging

    #  Detect operating system so PyInstaller knows whether to compile for Windows, MacOS, or Linux
    detected_os = platform.system()

    #  Pyxe currently supports Windows only since I haven't set up a linux or Mac computer to handle different OS'es
    if (detected_os == 'Windows'):
        
        #  Main process for Pyxe
        Pyxe = GUI()
        Pyxe.run_autocompiler()

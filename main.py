import platform
from threading import Thread
from tkinter import filedialog, Tk, Grid, ttk, StringVar
from tkinter.ttk import *
import PyInstaller.__main__
from PIL import Image
from win32api import GetSystemMetrics
import os


#  PythonFile class object that contains the main components to compile a program
class PythonFile:

    #  Initialize the object with the data
    def __init__(self, python_filepath, name, favicon_path, compile_directory, extra_data=False):
        self.python_filepath = python_filepath
        self.name = name
        self.favicon = convert_to_ico(favicon_path)
        self.compile_directory = compile_directory
        self.extra_data = extra_data

    #  Function that builds the Python project into an executable
    def make_exe(self):
        PyInstaller.__main__.run([
            '--name=%s' % self.name,
            '--onefile',
            '--windowed',
            '--distpath=%s' % self.compile_directory,
            # '--add-binary=%s' % os.path.join('resource', 'path', '*.png'),
            # '--add-data=%s' % os.path.join('resource', 'path', '*.txt'),
            '--icon=%s' % os.path.join('resources', 'ico', self.favicon),
            self.python_filepath
        ])


#  Convert selected photo to .ico image
def convert_to_ico(picture_filepath):
    favicon = "favicon.ico"

    # List comprehension creates (16,16) to (256,256) .ico file (2^n for n=4,5,6,7)
    icon_sizes = [(pow(2, size), pow(2, size)) for size in range(4, 8)]

    img = Image.open(picture_filepath)
    img.save(os.path.join('resources', 'ico', favicon), sizes=icon_sizes)

    return favicon


#  Allows GUI to continue running when you click 'Compile'
def thread_function(function, **kwargs):
    if (isinstance(function, str)):
        Thread(target=eval(function)).start()
    else:
        Thread(target=function, args=(kwargs)).start()
    return


#  Return filepath
def get_filepath_of_file(title, initialdir, filetypes):
    selected_file = ""

    #  If file doesn't exist, continue prompting file selection
    selected_file = filedialog.askopenfilename(title=title,
                                               initialdir=initialdir,
                                               filetypes=filetypes)
    #  Return filepath
    return selected_file


#  Set Tkinter's directory selection dialog box to given directory
def set_directory_path(title, initialdir, element):
    directory_path = ""
    directory_path = get_directory_path(title, initialdir)
    # print(directory_path)
    element.configure(state="enabled")
    set_entrybox_text(element, directory_path)
    element.configure(state="disabled")
    return


#  Return path of directory if it exists
def get_directory_path(title, initialdir):

    selected_directory = ""

    #  If file doesn't exist, continue prompting file selection
    selected_directory = filedialog.askdirectory(title=title,
                                                 initialdir=initialdir)
    #  Return filepath
    return selected_directory


#  Return text inside of Tkinter Entry widget
def get_entrybox_text(element):
    text = ""
    text = element.get()
    return text


#  Set text inside of Tkinter Entry widget
def set_entrybox_text(element, text):
    element.insert(0, text)
    return


#  Grab filepath of Python file
def python_get_filepath_of_file(title, initialdir, filetypes, element):
    filepath = get_filepath_of_file(title, initialdir, filetypes)
    element.configure(state="enabled")
    set_entrybox_text(element, filepath)
    element.configure(state="disabled")

    return


#  Make GUI elements
def make_GUI():

    #  Modify root title
    root.title("Pyxe Auto-Compiler")

    #  A grid frame that helps layout the widgets on the root window
    frame = ttk.Frame(root)
    Grid.rowconfigure(root, 0, weight=1)
    Grid.columnconfigure(root, 0, weight=1)
    frame.grid_columnconfigure(2, weight=1)

    #  These widgets make up the function allowing you to select a Python file to compile
    Label(frame, text='Select Python File:').grid(row=1, column=1, sticky="E")

    filepath_string = StringVar()

    program_filepath_textbox = Entry(frame, textvariable=filepath_string)
    program_filepath_textbox.configure(width=80, state="disabled")
    program_filepath_textbox.grid(row=1, column=2, sticky='EW', padx=(0, 5), pady=5, ipadx=5)

    file_selection_button = Button(frame, text='Select Python File', command=lambda: python_get_filepath_of_file(
        title="Select Python File",
        initialdir=project_dir,
        filetypes=[("Python File", "*.py")],
        element=program_filepath_textbox))
    file_selection_button.configure(width=20)
    file_selection_button.grid(row=1, column=3, padx=5, pady=5, sticky="EW")

    #  These widgets make up the function allowing you to select a picture to be the program's favicon
    Label(frame, text='Select Program Icon:').grid(row=2, column=1, sticky="E")

    icon_filepath_textbox = Entry(frame)
    icon_filepath_textbox.configure(width=80, state="disabled")
    icon_filepath_textbox.grid(row=2, column=2, sticky='EW', padx=(0, 5), pady=5, ipadx=5)

    python_icon_selector = Button(frame, text='Select Program Icon', command=lambda: python_get_filepath_of_file(
        title="Select Program Icon",
        initialdir=project_dir,
        filetypes=[("Pictures", "*.jpg;*.jpeg,*.png;*.svg;*.ico")],
        element=icon_filepath_textbox))
    python_icon_selector.configure(width=20)
    python_icon_selector.grid(row=2, column=3, padx=5, pady=5, sticky="EW")

    #  These widgets make up the function allowing you to give a name to the executable
    Label(frame, text='Program Name:').grid(row=3, column=1, sticky="E")

    program_name_textbox = Entry(frame)
    program_name_textbox.configure(width=80)
    program_name_textbox.grid(row=3, column=2, sticky='EW', padx=(0, 5), pady=5, ipadx=5)

    #  These widgets make up the function allowing you to select where you want to create the executable
    Label(frame, text='Build Folder:').grid(row=4, column=1, sticky="E")

    directory = Entry(frame)
    directory.configure(state='disabled')
    directory.grid(row=4, column=2, sticky='EW', padx=(0, 5), pady=5, ipadx=5)

    select_directory = Button(frame, text="Select Directory",
                              command=lambda: set_directory_path(title="Select Directory",
                                                                 initialdir=project_dir,
                                                                 element=directory))
    select_directory.configure(width=20)
    select_directory.grid(row=4, column=3, sticky="EW", padx=10, pady=5, ipadx=5)

    #  Function that creates the PythonFile object with the data necessary to compile the executable
    def compile_exe():
        status_text.grid(row=6, column=1, columnspan=3, sticky="EW", padx=10, pady=5, ipadx=5)
        status_text.configure(foreground="green", anchor="center")
        exe_info = PythonFile(get_entrybox_text(program_filepath_textbox),
                              get_entrybox_text(program_name_textbox),
                              get_entrybox_text(icon_filepath_textbox),
                              get_entrybox_text(directory),
                              False)
        exe_info.make_exe()

    #  These widgets make up the function that allows you to compile the executable
    compile_button = Button(frame, text="Compile", command=lambda: thread_function(compile_exe))
    compile_button.grid(row=5, column=1, columnspan=2, sticky='EW', padx=10, pady=5, ipadx=5)

    status_text = Label(frame, text='Compiling Project...')
    status_text.grid(row=6, column=1, columnspan=3, sticky="EW", padx=10, pady=5, ipadx=5)
    status_text.grid_remove()

    #  This widget make up the function allowing you to discontinue compiling the executable
    quit_button = Button(frame, text="Quit", command=lambda: root.destroy())
    quit_button.grid(row=5, column=3, sticky='EW', padx=10, pady=5, ipadx=5)

    #  Expand frame to fit the root window
    frame.grid(sticky="nsew", padx=2, pady=2)

    #  GUI size and placement on the screen
    screen_width = GetSystemMetrics(0)
    screen_height = GetSystemMetrics(1)
    app_width = 800
    app_height = 220

    root.geometry(str(app_width) + "x" + str(app_height) + "+" + str(
        int((screen_width / 2) - (app_width / 2))) + "+" + str(
        int((screen_height / 2) - (app_height / 2))))

    #  The icon that appears in the corner of the executable
    root.iconbitmap(project_dir + r'\resources\ico\favicon.ico')

    #  Restricts the GUI from being resized
    root.resizable(False, False)
    root.deiconify()  # Get rid of extra GUI window
    # root.protocol("WM_DELETE_WINDOW", close_browser())  # Close chrome browser on exit


#  Display Tkinter GUI
def display_GUI():
    root.mainloop()


#  Main function that runs the whole
if __name__ == '__main__':

    #  Global variables that can be accessed by any function in this Python file
    project_dir = os.getcwd()
    root = None
    filepath = ""
    program_name = ""
    icon_path = ""


    #  Detect operating system so PyInstaller knows whether to compile for Windows or Mac OS X
    detected_os = platform.system()

    if (detected_os == 'Windows'):
        #  Make Tkinter GUI
        root = Tk()

        #  Withdrawal useless window
        root.withdraw()

        #  Main process for Pyxe
        make_GUI()
        display_GUI()

import tkinter as tk
from tkinter import ttk as ttk
from pandastable import Table
from CreatePlot import *
from CreateMap import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class GUI:

    def __init__(self, root, collection):
        '''
        Constructor builds GUI widgets.
        :param root: root name imported from main
        :param collection: MongpDB collection
        '''

        # Initializing MongoDB collection and creating Canvas
        self.collection = collection
        self.canvas = tk.Canvas(root, width=1100, height=450)
        self.canvas.pack()

        # Creating left and right frames
        self.frm_left = tk.Frame(root, bg='gray')
        self.frm_left.place(relheight=1, relwidth=0.15)              # Left Frame

        self.frm_right = tk.Frame(root, bg='white')
        self.frm_right.place(relx=0.15, relheight=1, relwidth=0.85)  # Right Frame

        # Left frame widgets
        self.lbl_type = tk.Label(self.frm_left, text='Type:', bg='gray')
        self.lbl_type.pack(fill='x')                                                               # Type Label

        self.combo_type = ttk.Combobox(self.frm_left, values=['Traffic', 'Incidents'])
        self.combo_type.pack(fill='x')                                                             # Type Combobox

        self.lbl_year = tk.Label(self.frm_left, text='Year:', bg='gray')
        self.lbl_year.pack(fill='x')                                                               # Year Label

        self.combo_year = ttk.Combobox(self.frm_left, values=['2016', '2017', '2018'])
        self.combo_year.pack(fill='x')                                                             # Year Combobox

        self.btn_read = tk.Button(self.frm_left, text='Read', command=self.db_read)
        self.btn_read.pack(fill='x')                                                               # Read Button

        self.btn_sort = tk.Button(self.frm_left, text='Sort', command=self.db_sort)
        self.btn_sort.pack(fill='x')                                                               # Sort Button

        self.btn_analysis = tk.Button(self.frm_left, text='Analysis', command=self.db_analysis)
        self.btn_analysis.pack(fill='x')                                                           # Analysis Button

        self.btn_map = tk.Button(self.frm_left, text='Map', command=self.db_map)
        self.btn_map.pack(fill='x')                                                                # Map Button

        self.lbl_status = tk.Label(self.frm_left, text='Status:', bg='gray')
        self.lbl_status.pack(fill='x')                                                             # Status Label

        self.txt_status = tk.Text(self.frm_left, bg='white', wrap='word')
        self.txt_status.pack(fill='both')                                                          # Status Text

    def db_read(self):
        '''
        Command for 'Read' button to execute ReadSort's read_db method and display
        '''
        try:
            # Destroying old sub frame and adding a new one in frm_right
            for widget in self.frm_right.winfo_children():
                widget.destroy()
            self.frm_right.pack_forget()
            self.frm_sub = tk.Frame(self.frm_right, bg='white')
            self.frm_sub.pack(fill='both')

            # Getting input ID and using it to execute read_db
            input_id = self.combo_type.get() + self.combo_year.get()
            rs = ReadSort(self.collection, input_id)
            df = rs.read_db()

            # Creating table and placing it in frame
            pt = Table(self.frm_sub, dataframe=df)
            pt.show()

            # Message for successful execution
            self.txt_status.delete(1.0, tk.END)
            message = 'Read executed successfully.'
            self.txt_status.insert(tk.INSERT, message)

        except:
            # Message for failed execution
            self.txt_status.delete(1.0, tk.END)
            message = 'An error occurred, please ensure all fields are filled.'
            self.txt_status.insert(tk.INSERT, message)

    def db_sort(self):
        try:
            # Destroying old sub frame and adding a new one in frm_right
            for widget in self.frm_right.winfo_children():
                widget.destroy()
            self.frm_right.pack_forget()
            self.frm_sub = tk.Frame(self.frm_right, bg='white')
            self.frm_sub.pack(fill='both')

            # Getting input ID and using it to execute sort method depending on ID
            input_id = self.combo_type.get() + self.combo_year.get()
            rs = ReadSort(self.collection, input_id)
            df = ''
            if self.combo_type.get() == 'Traffic':
                df = rs.sort_traffic()
            elif self.combo_type.get() == 'Incidents':
                df = rs.sort_incidents()

            # Creating table and placing it in frame
            pt = Table(self.frm_sub, dataframe=df)
            pt.show()

            # Message for successful execution
            self.txt_status.delete(1.0, tk.END)
            message = 'Sort executed successfully.'
            self.txt_status.insert(tk.INSERT, message)

        except:
            # Message for failed execution
            self.txt_status.delete(1.0, tk.END)
            message = 'An error occurred, please ensure all fields are filled.'
            self.txt_status.insert(tk.INSERT, message)

    def db_analysis(self):
        try:
            # Destroying old sub frame and adding a new one in frm_right
            for widget in self.frm_right.winfo_children():
                widget.destroy()
            self.frm_right.pack_forget()
            self.frm_sub = tk.Frame(self.frm_right, bg='white')
            self.frm_sub.pack(fill='both')

            # Getting type in and using it to create plot (figure)
            type_in = self.combo_type.get()
            cp = CreatePlot(self.collection, type_in + '2016', type_in + '2017', type_in + '2018', type_in).fig

            # Creating canvas for figure and placing it in frame
            fig_canvas = FigureCanvasTkAgg(cp, master=self.frm_sub)
            fig_canvas.draw()
            fig_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

            # Message for successful execution
            self.txt_status.delete(1.0, tk.END)
            message = 'Analysis executed successfully.'
            self.txt_status.insert(tk.INSERT, message)

        except:
            # Message for failed execution
            self.txt_status.delete(1.0, tk.END)
            message = 'An error occurred, please ensure all fields are filled.'
            self.txt_status.insert(tk.INSERT, message)


    def db_map(self):
        try:
            # Destroying old sub frame and adding a new one in frm_right
            for widget in self.frm_right.winfo_children():
                widget.destroy()
            self.frm_right.pack_forget()
            self.frm_sub = tk.Frame(self.frm_right, bg='white')
            self.frm_sub.pack(fill='both')

            # Getting input ID and using it to create map.html
            input_id = self.combo_type.get() + self.combo_year.get()
            CreateMap(self.collection, input_id, self.combo_type.get())

            # Creating label to prompt user
            lbl = tk.Label(self.frm_sub, text='Map created, check folder for HTML file.', bg='white')
            lbl.pack()

            # Message for successful execution
            self.txt_status.delete(1.0, tk.END)
            message = 'Map creation executed successfully.'
            self.txt_status.insert(tk.INSERT, message)

        except:
            # Message for failed execution
            self.txt_status.delete(1.0, tk.END)
            message = 'An error occurred, please ensure all fields are filled.'
            self.txt_status.insert(tk.INSERT, message)

import datetime
import time
import pandas as pd
from dateutil.relativedelta import relativedelta
from tkinter import TclError, NO, END, DoubleVar, filedialog, Checkbutton
from tkinter import Tk, Label, Frame, Entry, FLAT, Canvas, Button, StringVar, CENTER, Toplevel, messagebox, IntVar
from tkinter.ttk import Combobox, Treeview, Style, Notebook
from PIL import Image, ImageTk
from os import getcwd, path
from sqlite3 import connect
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ctypes import windll as window_dpi
from screeninfo import get_monitors
from time import strftime
from collections import Counter
from hashlib import md5
from fpdf import FPDF

window_dpi.shcore.SetProcessDpiAwareness(1)

# ====================== Locating files and folders ============================
db_name = 'Qwe390snnskeyy46snckalkjdn872209102 - Copy.db'
current_directory = getcwd()
path_to_icons = current_directory + '\\' + 'assets' + '\\' + 'icons' + '\\'
path_to_images = current_directory + '\\' + 'assets' + '\\' + 'images' + '\\'
path_to_database = current_directory + '\\' + 'assets' + '\\' + 'informational' + '\\' + db_name
account_types = ['Admin', 'Cashier']
tables = ['Users', 'Products', 'Sales', 'Transactions']
font = "yu gothic ui"
monitor = get_monitors()


def center(win):
    """
    centers a tkinter window
    :param win: the main window or Toplevel window to center
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()


class LoginMainPage:
    def __init__(self, login_window):
        # ======================== Window Settings =============================
        self.window_initializer = login_window
        self.window_initializer.geometry('500x600')
        self.window_initializer.title("POS Terminal Login")
        self.window_initializer.resizable(0, 0)
        center(self.window_initializer)

        # ======================= Window Variables =============================
        self.username_value = StringVar()
        self.password_value = StringVar()
        self.account_type_value = StringVar()

        # ====================== Creating Login Frame Window ==================
        self.login_frame = Frame(self.window_initializer, bg='#040405')
        self.login_frame.place(x=0, y=0, width=500, height=600)

        self.heading = Label(self.login_frame, text='WELCOME')
        self.heading.configure(font=('yu gothic ui', 25, 'bold'), bg='#040405', fg='white')
        self.heading.place(x=170, y=130)

        # ==================== Sign-in Image ================================
        self.signin_image = Image.open(path_to_images + 'sign.png')

        signin_photo = ImageTk.PhotoImage(self.signin_image)
        self.signin_image_label = Label(self.login_frame, image=signin_photo, bg='#040405')
        self.signin_image_label.image = signin_photo
        self.signin_image_label.place(x=180, y=10)

        # =================== Sign-in Label ================================
        self.signin_label = Label(self.login_frame, text='Sign-In')
        self.signin_label.configure(bg='#040405', fg='white', font=('yu gothic ui', 17, 'bold'))
        self.signin_label.place(x=210, y=180)

        # =================== Username Label ===============================
        self.username_label = Label(self.login_frame, text='Username')
        self.username_label.configure(bg='#040405', fg='white', font=('yu gothic ui', 13, 'bold'))
        self.username_label.place(x=100, y=240)

        self.username_entry = Entry(self.login_frame, highlightthickness=0, relief=FLAT)
        self.username_entry.configure(bg='#040405', fg='#cad8eb', font=('yu gothic ui', 12, 'bold'))
        self.username_entry.config(textvariable=self.username_value, insertbackground='#cad8eb')
        self.username_entry.place(x=100, y=270, width=300)

        self.username_line = Canvas(self.login_frame, width=300, height=2.0, bg='#bdb9b1', highlightthickness=0)
        self.username_line.place(x=100, y=298)
        
        # =================== password Label ===============================
        self.password_label = Label(self.login_frame, text='Password')
        self.password_label.configure(bg='#040405', fg='white', font=('yu gothic ui', 13, 'bold'))
        self.password_label.place(x=100, y=310)

        self.password_entry = Entry(self.login_frame, highlightthickness=0, relief=FLAT, show="*")
        self.password_entry.configure(bg='#040405', fg='#cad8eb', font=('yu gothic ui', 12, 'bold'))
        self.password_entry.config(textvariable=self.password_value, insertbackground='#cad8eb')
        self.password_entry.place(x=100, y=340, width=300)

        self.password_line = Canvas(self.login_frame, width=300, height=2.0, bg='#bdb9b1', highlightthickness=0)
        self.password_line.place(x=100, y=368)
        
        # =================== account_type Label ===============================
        self.account_type_label = Label(self.login_frame, text='Account Type')
        self.account_type_label.configure(bg='#040405', fg='white', font=('yu gothic ui', 12, 'bold'))
        self.account_type_label.place(x=100, y=380)

        self.account_type_combo = Combobox(self.login_frame, font=('yu gothic ui', 12, 'bold'))
        self.account_type_combo.config(state='readonly')
        self.account_type_combo['values'] = account_types
        self.account_type_combo.config(textvariable=self.account_type_value)
        self.account_type_combo.place(x=100, y=415, width=300)

        self.account_type_line = Canvas(self.login_frame, width=300, height=2.0, bg='#bdb9b1', highlightthickness=0)
        self.account_type_line.place(x=100, y=440)

        # =================== Login Button ======================================
        self.login_button = Image.open(path_to_images + 'button.png')
        button_photo = ImageTk.PhotoImage(self.login_button)
        self.login_button_label = Label(self.login_frame, image=button_photo, bg='#040405')
        self.login_button_label.image = button_photo
        self.login_button_label.place(x=100, y=460)

        self.login_btn = Button(self.login_frame, text='LOGIN')
        self.login_btn.configure(font=('yu gothic ui', 13, 'bold'), width=25, bd=0, bg='#2047ff',
                                 activebackground='#3047ff', fg='white')
        self.login_btn.config(command=self.get_window_values)
        self.login_btn.place(x=125, y=475)

        # ================= Error Label ========================================
        self.error_label = Label(self.login_frame, bg='green')

    def get_window_values(self):
        username = self.username_value.get().strip()
        password = self.password_value.get().strip()
        account_type = self.account_type_value.get().strip()

        if account_type == '':
            self.error_label.place(x=150, y=530)
            self.error_label.config(text="Account type must be filled!", bg='#040405', fg='red')
            self.error_label.config(font=('yu gothic ui', 12, 'bold'))

        else:
            if path.isfile(path_to_database):
                db_connection = connect(path_to_database)
                writer = db_connection.cursor()
                lookup_command = "SELECT * FROM {} WHERE username='{}'".format("accounts", username)
                writer.execute(lookup_command)
                result = writer.fetchone()
                db_connection.close()

                try:
                    lookup_username = result[6]
                    lookup_password = result[7]

                    string_to_hash = str(password)
                    hashing_function = md5(string_to_hash.encode())
                    hashed_password = hashing_function.hexdigest()

                    if lookup_username == username and lookup_password == hashed_password and account_type == 'Admin' and len(lookup_username.strip()) > 3:
                        self.window_initializer.destroy()
                        load_admin_page()

                    elif lookup_username == username and lookup_password == hashed_password and account_type == 'Cashier':
                        self.window_initializer.destroy()
                        load_cashier_page()

                    else:
                        self.error_label.place(x=95, y=530)
                        self.error_label.config(text="Login failed! Wrong Username or Password!")
                        self.error_label.config(font=('yu gothic ui', 12, 'bold'), bg='#040405', fg='red')

                except TypeError:
                    self.error_label.place(x=95, y=530)
                    self.error_label.config(text="Login failed! Wrong Username or Password!")
                    self.error_label.config(font=('yu gothic ui', 12, 'bold'), bg='#040405', fg='red')

            else:
                messagebox.showerror("Database cannot be found!")


class AdminPage:
    def __init__(self, window_init):
        self.category_code = None
        self.window_initializer = window_init
        self.screen_width = self.window_initializer.winfo_screenwidth()
        self.screen_height = self.window_initializer.winfo_screenheight()
        screen_height = self.screen_height - 200
        self.window_initializer.geometry("{}x{}".format(self.screen_width, screen_height))
        self.window_initializer.state('zoomed')
        self.window_initializer.title('ADMIN ACCOUNT')
        self.window_initializer.resizable(False, True)

        # ==================================== Banner Frame =====================================
        self.menu_frame = Frame(self.window_initializer)
        self.menu_frame.configure(background="#9e3a3a", height=self.widget_height(90), width=self.screen_width)
        self.menu_frame.place(x=0, y=0)

        self.admin_icon = Image.open(path_to_icons + 'sales.png').resize(
            (self.widget_width(80), self.widget_height(80)))
        admin_photo = ImageTk.PhotoImage(self.admin_icon)
        self.admin_icon_label = Label(self.menu_frame, image=admin_photo, bg='#9e3a3a')
        self.admin_icon_label.image = admin_photo
        self.admin_icon_label.place(x=self.widget_width(20), y=self.widget_height(5))

        def cash():
            self.window_initializer.destroy()
            load_cashier_page()

        def load_cash(event):
            cash()

        self.window_initializer.bind("<KeyPress-F11>", load_cash)

        cashier_page_btn = Button(self.menu_frame, fg="white", bg="#9e3a3a", relief="solid")
        cashier_page_btn.configure(text="Cashier", font=(font, 14), command=cash)
        cashier_page_btn.place(x=self.widget_width(1450), y=self.widget_height(20))

        admin_header = Label(self.menu_frame, fg="white", bg="#9e3a3a")
        admin_header.configure(text="HUDUMIA CYBER ADMIN", font=(font, 25, "bold"))
        admin_header.place(x=self.widget_width(600), y=self.widget_height(15))

        self.side_menu = Frame(self.window_initializer)
        self.side_menu.configure(width=self.widget_width(241), height=self.widget_height(710), bg='#323231')
        self.side_menu.place(x=0, y=self.widget_height(90))

        def changeOnHover(button, colorOnHover, colorOnLeave):
            button.bind("<Enter>", func=lambda e: button.config(background=colorOnHover))
            button.bind("<Leave>", func=lambda e: button.config(background=colorOnLeave))

        self.dashboard_button = Button(self.side_menu, command=self.dashboard_frame_window)
        self.dashboard_button.configure(text='DASHBOARD', font=(font, self.font_adjust(15), 'bold'), fg='white',
                                        bg='#323231')
        self.dashboard_button.configure(width=self.widget_width(21), relief='flat')
        self.dashboard_button.place(x=0, y=self.widget_height(10))

        line_seperator1 = Canvas(self.side_menu, width=self.widget_width(300), height=self.widget_height(2.0),
                                 bg='#bdb9b1', highlightthickness=0)
        line_seperator1.place(x=0, y=self.widget_height(70))

        self.category_button = Button(self.side_menu, command=self.category_frame_window)
        self.category_button.configure(text='CATEGORY', font=(font, self.font_adjust(15), 'bold'), fg='white',
                                       bg='#323231')
        self.category_button.configure(width=self.widget_width(21), relief='flat')
        self.category_button.place(x=0, y=self.widget_height(80))

        line_seperator2 = Canvas(self.side_menu, width=self.widget_width(300), height=self.widget_height(2.0),
                                 bg='#bdb9b1', highlightthickness=0)
        line_seperator2.place(x=0, y=self.widget_height(140))

        self.product_button = Button(self.side_menu, command=self.products_frame_window)
        self.product_button.configure(text='PRODUCTS', font=(font, self.font_adjust(15), 'bold'), fg='white',
                                      bg='#323231')
        self.product_button.configure(width=self.widget_width(21), relief='flat')
        self.product_button.place(x=0, y=self.widget_height(150))

        line_seperator3 = Canvas(self.side_menu, width=self.widget_width(300), height=self.widget_height(2.0),
                                 bg='#bdb9b1', highlightthickness=0)
        line_seperator3.place(x=0, y=self.widget_height(210))

        self.stock_button = Button(self.side_menu, command=self.stock_frame_window)
        self.stock_button.configure(text='STOCKS', font=(font, self.font_adjust(15), 'bold'), fg='white', bg='#323231')
        self.stock_button.configure(width=self.widget_width(21), relief='flat')
        self.stock_button.place(x=0, y=self.widget_height(220))

        line_seperator4 = Canvas(self.side_menu, width=self.widget_width(300), height=self.widget_height(2.0),
                                 bg='#bdb9b1', highlightthickness=0)
        line_seperator4.place(x=0, y=self.widget_height(280))

        self.services_button = Button(self.side_menu, command=self.services_frame_window)
        self.services_button.configure(text='SERVICES', font=(font, self.font_adjust(15), 'bold'), fg='white',
                                       bg='#323231')
        self.services_button.configure(width=self.widget_width(21), relief='flat')
        self.services_button.place(x=0, y=self.widget_height(290))

        line_seperator5 = Canvas(self.side_menu, width=self.widget_width(300), height=self.widget_height(2.0),
                                 bg='#bdb9b1', highlightthickness=0)
        line_seperator5.place(x=0, y=self.widget_height(350))

        self.accounts_button = Button(self.side_menu)
        self.accounts_button.configure(text='ACCOUNTS', font=(font, self.font_adjust(15), 'bold'), fg='white',
                                       bg='#323231')
        self.accounts_button.configure(width=self.widget_width(21), relief='flat', command=self.accounts_frame_window)
        self.accounts_button.place(x=0, y=self.widget_height(360))

        line_seperator6 = Canvas(self.side_menu, width=self.widget_width(300), height=self.widget_height(2.0),
                                 bg='#bdb9b1', highlightthickness=0)
        line_seperator6.place(x=0, y=self.widget_height(420))

        self.reports_button = Button(self.side_menu)
        self.reports_button.configure(text='REPORTS', font=(font, self.font_adjust(15), 'bold'), fg='white',
                                      bg='#323231')
        self.reports_button.configure(width=self.widget_width(21), relief='flat', command=self.reports_frame_window)
        self.reports_button.place(x=0, y=self.widget_height(430))

        line_seperator7 = Canvas(self.side_menu, width=self.widget_width(300), height=self.widget_height(2.0),
                                 bg='#bdb9b1', highlightthickness=0)
        line_seperator7.place(x=0, y=self.widget_height(490))

        changeOnHover(self.dashboard_button, "#3232f0", "#323231")
        changeOnHover(self.category_button, "#3232f0", "#323231")
        changeOnHover(self.product_button, "#3232f0", "#323231")
        changeOnHover(self.stock_button, "#3232f0", "#323231")
        changeOnHover(self.services_button, "#3232f0", "#323231")
        changeOnHover(self.accounts_button, "#3232f0", "#323231")
        changeOnHover(self.reports_button, "#3232f0", "#323231")
        self.dashboard_frame_window()

    def widget_width(self, expected_value):
        monitor_width = monitor[0].width_mm
        window_width = self.window_initializer.winfo_screenwidth()
        resolution = window_width + (monitor_width / 25.4)
        optimal_resolution = 1600 + (309 / 25.4)
        new_value = (resolution * expected_value) / optimal_resolution

        return int(round(new_value, 0))

    def widget_height(self, expected_value):
        monitor_height = monitor[0].height_mm
        window_height = self.window_initializer.winfo_screenheight()
        resolution = window_height + (monitor_height / 25.4)
        optimal_resolution = 900 + (174 / 25.4)
        new_value = (resolution * expected_value) / optimal_resolution

        return int(round(new_value, 0))

    def font_adjust(self, expected_value):
        text_width = self.widget_width(expected_value=expected_value)
        text_height = self.widget_height(expected_value=expected_value)

        optimal_font = (text_width + text_height) / 2

        return int(round(optimal_font))

    def accounts_frame_window(self):
        search_entry_value = StringVar()
        combobox_search = StringVar()

        staff_id_value = IntVar()
        last_name_value = StringVar()
        middle_initial_value = StringVar()
        first_name_value = StringVar()
        id_number_value = IntVar()
        contact_value = IntVar()
        username_value = StringVar()
        password_value = StringVar()
        retyped_password_value = StringVar()
        role_value = StringVar()
        status_value = StringVar()

        accounts_style = Style()
        accounts_style.theme_use('clam')

        accounts_frame = Frame(self.window_initializer, bg='white')
        accounts_frame.configure(width=self.screen_width - self.widget_width(241), height=self.widget_height(710))
        accounts_frame.place(x=self.widget_width(241), y=self.widget_height(90))

        advanced_search_frame = Frame(accounts_frame)
        advanced_search_frame.configure(bg="white", width=self.screen_width - self.widget_width(320),
                                        height=self.widget_height(90))
        advanced_search_frame.configure(highlightbackground="#c2c2c0", highlightthickness=2)
        advanced_search_frame.place(x=self.widget_width(40), y=self.widget_height(34))

        advanced_search_label = Label(accounts_frame)
        advanced_search_label.configure(text="ADVANCED SEARCH", fg='#007bdf')
        advanced_search_label.configure(font=(font, self.font_adjust(13), 'bold'), bg='white')
        advanced_search_label.place(x=self.widget_width(80), y=self.widget_height(20))

        accounts_treeview_columns = ['c1', 'c2', 'c3', 'c4', 'c5', 'c6']
        accounts_treeview = Treeview(accounts_frame, show='headings', columns=accounts_treeview_columns)

        accounts_treeview.heading("# 1", text='ST. ID', anchor='w')
        accounts_treeview.column("# 1", stretch=NO, minwidth=self.widget_width(80), width=self.widget_width(80))
        accounts_treeview.heading("# 2", text='Name', anchor='w')
        accounts_treeview.column("# 2", stretch=NO, minwidth=self.widget_width(200), width=self.widget_width(200))
        accounts_treeview.heading("# 3", text='ID Number', anchor='w')
        accounts_treeview.column("# 3", stretch=NO, minwidth=self.widget_width(120), width=self.widget_width(120))
        accounts_treeview.heading("# 4", text='Contact No.', anchor='w')
        accounts_treeview.column("# 4", stretch=NO, minwidth=self.widget_width(140), width=self.widget_width(140))
        accounts_treeview.heading("# 5", text='Role', anchor='w')
        accounts_treeview.column("# 5", stretch=NO, minwidth=self.widget_width(120), width=self.widget_width(120))
        accounts_treeview.heading("# 6", text='Username', anchor='w')
        accounts_treeview.column("# 6", stretch=NO, minwidth=self.widget_width(120), width=self.widget_width(120))

        accounts_style.configure('Treeview.Heading', background="#3e3f3f", foreground='white',
                                 font=(font, self.font_adjust(12), 'bold'))
        accounts_style.configure('Treeview.Heading', relief='none')
        accounts_style.configure('Treeview', font=(font, self.font_adjust(12)))

        accounts_treeview.place(x=self.widget_width(40), y=self.widget_height(160), height=self.widget_height(520))

        staff_info_frame = Frame(accounts_frame)
        staff_info_frame.configure(bg="white", width=self.widget_width(459), height=self.widget_height(520))
        staff_info_frame.configure(highlightbackground="#c2c2c0", highlightthickness=2)
        staff_info_frame.place(x=self.widget_width(860), y=self.widget_height(160))

        staff_info_label = Label(accounts_frame)
        staff_info_label.configure(text="STAFF INFORMATION", fg='#007bdf')
        staff_info_label.configure(font=(font, self.font_adjust(13), 'bold'), bg='white')
        staff_info_label.place(x=self.widget_width(880), y=self.widget_height(145))

        staff_id_label = Label(staff_info_frame)
        staff_id_label.configure(text="Staff ID:*", font=(font, self.font_adjust(13)), bg='white')
        staff_id_label.place(x=self.widget_width(20), y=self.widget_height(20))

        staff_id_entry = Entry(staff_info_frame, textvariable=staff_id_value)
        staff_id_entry.configure(relief='solid', font=(font, self.font_adjust(13)), width=self.widget_width(30),
                                 state='disabled')
        staff_id_entry.place(x=self.widget_width(150), y=self.widget_height(20))

        last_name_label = Label(staff_info_frame)
        last_name_label.configure(text="Last Name:*", font=(font, self.font_adjust(13)), bg='white')
        last_name_label.place(x=self.widget_width(20), y=self.widget_height(55))

        last_name_entry = Entry(staff_info_frame, textvariable=last_name_value)
        last_name_entry.configure(relief='solid', font=(font, self.font_adjust(13)), width=self.widget_width(30),
                                  state='disabled')
        last_name_entry.place(x=self.widget_width(150), y=self.widget_height(55))

        middle_initial_label = Label(staff_info_frame)
        middle_initial_label.configure(text="Middle Initial:", font=(font, self.font_adjust(13)), bg='white')
        middle_initial_label.place(x=self.widget_width(20), y=self.widget_height(90))

        middle_initial_entry = Entry(staff_info_frame, textvariable=middle_initial_value)
        middle_initial_entry.configure(relief='solid', font=(font, self.font_adjust(13)), width=self.widget_width(30),
                                       state='disabled')
        middle_initial_entry.place(x=self.widget_width(150), y=self.widget_height(90))

        first_name_label = Label(staff_info_frame)
        first_name_label.configure(text="First Name:*", font=(font, self.font_adjust(13)), bg='white')
        first_name_label.place(x=self.widget_width(20), y=self.widget_height(125))

        first_name_entry = Entry(staff_info_frame, textvariable=first_name_value)
        first_name_entry.configure(relief='solid', font=(font, self.font_adjust(13)), width=self.font_adjust(25),
                                   state='disabled')
        first_name_entry.place(x=self.widget_width(150), y=self.widget_height(125))

        id_number_label = Label(staff_info_frame)
        id_number_label.configure(text="ID Number:*", font=(font, self.font_adjust(13)), bg='white')
        id_number_label.place(x=self.widget_width(20), y=self.widget_height(160))

        id_number_entry = Entry(staff_info_frame, textvariable=id_number_value)
        id_number_entry.configure(relief='solid', font=(font, self.font_adjust(13)), width=self.font_adjust(25),
                                  state='disabled')
        id_number_entry.place(x=self.widget_width(150), y=self.widget_height(160))

        contact_label = Label(staff_info_frame)
        contact_label.configure(text="ID Number:*", font=(font, self.font_adjust(13)), bg='white')
        contact_label.place(x=self.widget_width(20), y=self.widget_height(195))

        contact_entry = Entry(staff_info_frame, textvariable=contact_value)
        contact_entry.configure(relief='solid', font=(font, self.font_adjust(13)), width=self.font_adjust(25),
                                state='disabled')
        contact_entry.place(x=self.widget_width(150), y=self.widget_height(195))

        username_label = Label(staff_info_frame)
        username_label.configure(text="Username:*", font=(font, self.font_adjust(13)), bg='white')
        username_label.place(x=self.widget_width(20), y=self.widget_height(230))

        username_entry = Entry(staff_info_frame, textvariable=username_value)
        username_entry.configure(relief='solid', font=(font, self.font_adjust(13)), width=self.font_adjust(25),
                                 state='disabled')
        username_entry.place(x=self.widget_width(150), y=self.widget_height(230))

        password_label = Label(staff_info_frame)
        password_label.configure(text="Password:*", font=(font, self.font_adjust(13)), bg='white')
        password_label.place(x=self.widget_width(20), y=self.widget_height(265))

        password_entry = Entry(staff_info_frame, textvariable=password_value)
        password_entry.configure(relief='solid', font=(font, self.font_adjust(13)), width=self.font_adjust(25),
                                 state='disabled')
        password_entry.place(x=self.widget_width(150), y=self.widget_height(265))

        retype_password_label = Label(staff_info_frame)
        retype_password_label.configure(text="Re-type Pass:*", font=(font, self.font_adjust(13)), bg='white')
        retype_password_label.place(x=self.widget_width(20), y=self.widget_height(300))

        retype_password_entry = Entry(staff_info_frame, textvariable=retyped_password_value)
        retype_password_entry.configure(relief='solid', font=(font, self.font_adjust(13)), width=self.font_adjust(25),
                                        state='disabled')
        retype_password_entry.place(x=self.widget_width(150), y=self.widget_height(300))

        role_label = Label(staff_info_frame)
        role_label.configure(text="Role:*", font=(font, self.font_adjust(13)), bg='white')
        role_label.place(x=self.widget_width(20), y=self.widget_height(335))

        role_entry = Combobox(staff_info_frame, textvariable=role_value)
        role_entry.configure(state='readonly', font=(font, self.font_adjust(13)), width=self.widget_width(29))
        roles_values = ['Administrator', 'Cashier']
        role_entry.configure(state='disabled', values=roles_values)
        role_entry.current(0)
        role_entry.place(x=self.widget_width(150), y=self.widget_height(335))

        status_label = Label(staff_info_frame)
        status_label.configure(text="Status:*", font=(font, self.font_adjust(13)), bg='white')
        status_label.place(x=self.widget_width(20), y=self.widget_height(370))

        status_entry = Combobox(staff_info_frame, textvariable=status_value)
        status_entry.configure(font=(font, self.font_adjust(13)), state='readonly', width=self.widget_width(29))
        status_values = ['Active', 'Inactive']
        status_entry.configure(state='disabled', values=status_values)
        status_entry.current(0)
        status_entry.place(x=self.widget_width(150), y=self.widget_height(370))

        def save_user():
            counter = []
            try:
                staff_id = staff_id_value.get()

            except TclError:
                messagebox.showerror("Database Error", "Staff ID should be numbers only! \nDon't start with 0")
                staff_id = 0

            last_name = last_name_value.get().strip()
            middle_initial = middle_initial_value.get().strip()
            first_name = first_name_value.get().strip()

            try:
                id_number = id_number_value.get()

            except TclError:
                messagebox.showerror("Database Error", "ID number should be numbers only! \nDon't start with 0")
                id_number = 0

            try:
                contact = contact_value.get()

            except TclError:
                messagebox.showerror("Database Error", "Contact number should be numbers only! \nDon't start with 0")
                contact = 0

            username = username_value.get().strip()
            password = password_value.get().strip()
            retyped_password = retyped_password_value.get().strip()
            role = role_value.get()
            status = status_value.get()

            def collect_values(field, value):
                connection = connect(path_to_database)
                write = connection.cursor()
                lk_command = "SELECT * FROM {} WHERE {}='{}'".format("accounts", field, value)
                write.execute(lk_command)
                values = write.fetchall()
                connection.close()

                return values

            if len(str(staff_id)) > 20 or staff_id == 0 or staff_id < 1 or len(collect_values("staffid", staff_id)) > 0:
                staff_id_entry.configure(highlightbackground="red", highlightthickness=2)
                counter.append(0)

            if len(collect_values("username", username)) > 0 or username == "":
                username_entry.configure(highlightbackground="red", highlightthickness=2)
                counter.append(0)

            if password != retyped_password or retyped_password == "":
                retype_password_entry.configure(highlightbackground="red", highlightthickness=2)
                counter.append(0)

            if password == "" or len(password) < 4:
                password_entry.configure(highlightbackground="red", highlightthickness=2)
                counter.append(0)

            if last_name == "" or len(last_name) > 50:
                last_name_entry.configure(highlightbackground="red", highlightthickness=2)
                counter.append(0)

            if first_name == "" or len(first_name) > 50:
                first_name_entry.configure(highlightbackground="red", highlightthickness=2)
                counter.append(0)

            if len(middle_initial) > 1:
                middle_initial_entry.configure(highlightbackground="red", highlightthickness=2)
                counter.append(0)

            if len(str(id_number)) > 20 or id_number == 0 or len(str(id_number)) < 3:
                id_number_entry.configure(highlightbackground="red", highlightthickness=2)
                counter.append(0)

            if len(str(contact)) > 20 or contact == 0 or len(str(contact)) < 3:
                contact_entry.configure(highlightbackground="red", highlightthickness=2)
                counter.append(0)

            if len(counter) > 0:
                messagebox.showwarning("Database Warning!",
                                       "Fix {} error(s) found in the form".format(str(len(counter))))

            else:
                today = datetime.datetime.today()
                current_time = today.strftime("%d/%B/%Y %H:%M")

                string_to_hash = str(password)
                hashing_function = md5(string_to_hash.encode())
                hashed_password = hashing_function.hexdigest()

                conn = connect(path_to_database)
                c = conn.cursor()
                params = (staff_id, last_name, middle_initial, first_name, id_number, contact, username,
                          hashed_password, role, status, str(current_time))
                c.execute("INSERT INTO accounts VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", params)
                conn.commit()

                db_connect = connect(path_to_database)
                writ = db_connect.cursor()
                ld = "SELECT * FROM {}".format("accounts")
                writ.execute(ld)
                resu = writ.fetchall()
                db_connect.close()

                for items in accounts_treeview.get_children():
                    accounts_treeview.delete(items)

                for X in range(0, len(result)):
                    accounts_treeview.insert("", 'end', text="1",
                                             values=(resu[X][0], resu[X][1] + " " + resu[X][2] + ". "
                                                     + resu[X][3], resu[X][4], resu[X][5],
                                                     resu[X][8], resu[X][6]))
                    accounts_treeview.update_idletasks()

                staff_id_entry.delete(0, END)
                last_name_entry.delete(0, END)
                middle_initial_entry.delete(0, END)
                first_name_entry.delete(0, END)
                id_number_entry.delete(0, END)
                contact_entry.delete(0, END)
                username_entry.delete(0, END)
                password_entry.delete(0, END)
                retype_password_entry.delete(0, END)

                staff_id_entry.configure(highlightbackground="black", highlightthickness=0)
                last_name_entry.configure(highlightbackground="black", highlightthickness=0)
                middle_initial_entry.configure(highlightbackground="black", highlightthickness=0)
                first_name_entry.configure(highlightbackground="black", highlightthickness=0)
                id_number_entry.configure(highlightbackground="black", highlightthickness=0)
                contact_entry.configure(highlightbackground="black", highlightthickness=0)
                username_entry.configure(highlightbackground="black", highlightthickness=0)
                password_entry.configure(highlightbackground="black", highlightthickness=0)
                retype_password_entry.configure(highlightbackground="black", highlightthickness=0)

        save_button = Button(staff_info_frame, bg='#007bdf', command=save_user, state='disabled')
        save_button.configure(text="SAVE", font=(font, self.font_adjust(13)), relief='solid',
                              width=self.widget_width(12))
        save_button.place(x=self.widget_width(300), y=self.widget_height(410))

        def create_user():
            staff_id_entry.configure(state='normal')
            last_name_entry.configure(state='normal')
            middle_initial_entry.configure(state='normal')
            first_name_entry.configure(state='normal')
            id_number_entry.configure(state='normal')
            contact_entry.configure(state='normal')
            username_entry.configure(state='normal')
            password_entry.configure(state='normal')
            retype_password_entry.configure(state='normal')
            save_button.configure(state='normal')
            role_entry.configure(state='normal')
            role_entry.configure(state='readonly')
            status_entry.configure(state='normal')
            status_entry.configure(state='readonly')

            staff_id_entry.delete(0, END)
            last_name_entry.delete(0, END)
            middle_initial_entry.delete(0, END)
            first_name_entry.delete(0, END)
            id_number_entry.delete(0, END)
            contact_entry.delete(0, END)
            username_entry.delete(0, END)
            password_entry.delete(0, END)
            retype_password_entry.delete(0, END)

        create_button = Button(staff_info_frame, bg='#f0bc00', fg='white', command=create_user)
        create_button.configure(text="CREATE NEW", font=(font, self.font_adjust(13)), relief='solid',
                                width=self.widget_width(13))
        create_button.place(x=self.widget_width(150), y=self.widget_height(410))

        def update_user_function():
            username = username_value.get().strip()
            password = password_value.get().strip()
            retyped_password = retyped_password_value.get().strip()
            role = role_value.get()
            status = status_value.get()

            try:
                connection = connect(path_to_database)
                write = connection.cursor()
                lk_command = "SELECT * FROM {} WHERE {}='{}'".format("accounts", "staffid", staff_id_value.get())
                write.execute(lk_command)
                values = write.fetchall()
                connection.close()

                connection = connect(path_to_database)
                write = connection.cursor()
                lk_command = "SELECT * FROM {} WHERE {}='{}'".format("accounts", "staffid", staff_id_value.get())
                write.execute(lk_command)
                values = write.fetchall()
                connection.close()

                staff_id = values[0][0]
                roles = values[0][8]
                statuses = values[0][9]

                def update_table():
                    db_connect = connect(path_to_database)
                    writ = db_connect.cursor()
                    ld = "SELECT * FROM {}".format("accounts")
                    writ.execute(ld)
                    resu = writ.fetchall()
                    db_connect.close()

                    for items in accounts_treeview.get_children():
                        accounts_treeview.delete(items)

                    for X in range(0, len(result)):
                        accounts_treeview.insert("", 'end', text="1",
                                                 values=(resu[X][0], resu[X][1] + " " + resu[X][2] + ". "
                                                         + resu[X][3], resu[X][4], resu[X][5],
                                                         resu[X][8], resu[X][6]))
                        accounts_treeview.update_idletasks()

                def updates(field, new_value, staff):
                    conn = connect(path_to_database)
                    writes = conn.cursor()
                    lk_comm = "UPDATE {} SET {}='{}' WHERE staffid='{}'".format("accounts", field, new_value, staff)
                    writes.execute(lk_comm)
                    conn.commit()
                    conn.close()

                def collect_values(field, value):
                    connection = connect(path_to_database)
                    write = connection.cursor()
                    lk_command = "SELECT * FROM {} WHERE {}='{}'".format("accounts", field, value)
                    write.execute(lk_command)
                    values = write.fetchall()
                    connection.close()

                    return values

                if len(collect_values("username",
                                      username)) != 0 and password == "" and role == roles and status == statuses:
                    cancel_function()

                elif len(collect_values("username",
                                        username)) == 0 and password == "" and role == roles and status == statuses:
                    updates("username", username, staff_id)
                    update_table()
                    cancel_function()

                elif len(collect_values("username",
                                        username)) == 0 and password == "" and role != roles and status == statuses:
                    updates("username", username, staff_id)
                    updates("role", role, staff_id)
                    update_table()
                    cancel_function()

                elif len(collect_values("username",
                                        username)) == 0 and password == "" and role != roles and status != statuses:
                    updates("username", username, staff_id)
                    updates("role", role, staff_id)
                    updates("status", status, staff_id)
                    update_table()
                    cancel_function()

                elif len(collect_values("username",
                                        username)) == 0 and password == "" and role == roles and status != statuses:
                    updates("username", username, staff_id)
                    updates("status", status, staff_id)
                    update_table()
                    cancel_function()

                elif len(collect_values("username",
                                        username)) != 0 and password == "" and role != roles and status != statuses:
                    updates("role", role, staff_id)
                    updates("status", status, staff_id)
                    update_table()
                    cancel_function()

                elif len(collect_values("username",
                                        username)) != 0 and password == "" and role != roles and status == statuses:
                    updates("role", role, staff_id)
                    update_table()
                    cancel_function()

                elif len(collect_values("username",
                                        username)) != 0 and password == "" and role == roles and status != statuses:
                    updates("status", status, staff_id)
                    update_table()
                    cancel_function()

                elif len(collect_values("username",
                                        username)) != 0 and password != "" and role == roles and status == statuses:
                    if len(password) < 4 or retyped_password != password:
                        password_entry.configure(highlightbackground="red", highlightthickness=2)
                        retype_password_entry.configure(highlightbackground="red", highlightthickness=2)
                        messagebox.showerror("Password Error", "Password length is too short min length is 4\n"
                                                               "Retype-Password must be same as password")

                    else:
                        string_to_hash = str(password)
                        hashing_function = md5(string_to_hash.encode())
                        hashed_password = hashing_function.hexdigest()

                        updates("password", hashed_password, staff_id)
                        cancel_function()

                elif len(collect_values("username",
                                        username)) == 0 and password != "" and role == roles and status == statuses:
                    if len(password) < 4 or retyped_password != password:
                        password_entry.configure(highlightbackground="red", highlightthickness=2)
                        retype_password_entry.configure(highlightbackground="red", highlightthickness=2)
                        messagebox.showerror("Password Error", "Password length is too short min length is 4\n"
                                                               "Retype-Password must be same as password")

                    else:
                        string_to_hash = str(password)
                        hashing_function = md5(string_to_hash.encode())
                        hashed_password = hashing_function.hexdigest()

                        updates("username", username, staff_id)
                        updates("password", hashed_password, staff_id)
                        cancel_function()

                elif len(collect_values("username",
                                        username)) == 0 and password != "" and role != roles and status == statuses:
                    if len(password) < 4 or retyped_password != password:
                        password_entry.configure(highlightbackground="red", highlightthickness=2)
                        retype_password_entry.configure(highlightbackground="red", highlightthickness=2)
                        messagebox.showerror("Password Error", "Password length is too short min length is 4\n"
                                                               "Retype-Password must be same as password")

                    else:
                        string_to_hash = str(password)
                        hashing_function = md5(string_to_hash.encode())
                        hashed_password = hashing_function.hexdigest()

                        updates("username", username, staff_id)
                        updates("role", role, staff_id)
                        updates("password", hashed_password, staff_id)
                        cancel_function()

                elif len(collect_values("username",
                                        username)) == 0 and password != "" and role != roles and status != statuses:
                    if len(password) < 4 or retyped_password != password:
                        password_entry.configure(highlightbackground="red", highlightthickness=2)
                        retype_password_entry.configure(highlightbackground="red", highlightthickness=2)
                        messagebox.showerror("Password Error", "Password length is too short min length is 4\n"
                                                               "Retype-Password must be same as password")

                    else:
                        string_to_hash = str(password)
                        hashing_function = md5(string_to_hash.encode())
                        hashed_password = hashing_function.hexdigest()

                        updates("username", username, staff_id)
                        updates("role", role, staff_id)
                        updates("password", hashed_password, staff_id)
                        updates("status", status, staff_id)
                        cancel_function()

                elif len(collect_values("username",
                                        username)) != 0 and password != "" and role != roles and status != statuses:
                    if len(password) < 4 or retyped_password != password:
                        password_entry.configure(highlightbackground="red", highlightthickness=2)
                        retype_password_entry.configure(highlightbackground="red", highlightthickness=2)
                        messagebox.showerror("Password Error", "Password length is too short min length is 4\n"
                                                               "Retype-Password must be same as password")

                    else:
                        string_to_hash = str(password)
                        hashing_function = md5(string_to_hash.encode())
                        hashed_password = hashing_function.hexdigest()

                        updates("role", role, staff_id)
                        updates("password", hashed_password, staff_id)
                        updates("status", status, staff_id)
                        cancel_function()

                elif len(collect_values("username",
                                        username)) != 0 and password != "" and role != roles and status == statuses:
                    if len(password) < 4 or retyped_password != password:
                        password_entry.configure(highlightbackground="red", highlightthickness=2)
                        retype_password_entry.configure(highlightbackground="red", highlightthickness=2)
                        messagebox.showerror("Password Error", "Password length is too short min length is 4\n"
                                                               "Retype-Password must be same as password")

                    else:
                        string_to_hash = str(password)
                        hashing_function = md5(string_to_hash.encode())
                        hashed_password = hashing_function.hexdigest()

                        updates("role", role, staff_id)
                        updates("password", hashed_password, staff_id)
                        cancel_function()

                elif len(collect_values("username",
                                        username)) == 0 and password != "" and role == roles and status != statuses:
                    if len(password) < 4 or retyped_password != password:
                        password_entry.configure(highlightbackground="red", highlightthickness=2)
                        retype_password_entry.configure(highlightbackground="red", highlightthickness=2)
                        messagebox.showerror("Password Error", "Password length is too short min length is 4\n"
                                                               "Retype-Password must be same as password")

                    else:
                        string_to_hash = str(password)
                        hashing_function = md5(string_to_hash.encode())
                        hashed_password = hashing_function.hexdigest()

                        updates("password", hashed_password, staff_id)
                        updates("status", status, staff_id)
                        cancel_function()

                elif len(collect_values("username",
                                        username)) != 0 and password != "" and role == roles and status != statuses:
                    if len(password) < 4 or retyped_password != password:
                        password_entry.configure(highlightbackground="red", highlightthickness=2)
                        retype_password_entry.configure(highlightbackground="red", highlightthickness=2)
                        messagebox.showerror("Password Error", "Password length is too short min length is 4\n"
                                                               "Retype-Password must be same as password")

                    else:
                        string_to_hash = str(password)
                        hashing_function = md5(string_to_hash.encode())
                        hashed_password = hashing_function.hexdigest()

                        updates("username", username, staff_id)
                        updates("password", hashed_password, staff_id)
                        updates("status", status, staff_id)
                        cancel_function()

            except IndexError:
                pass

            except TclError:
                pass

        update_button = Button(staff_info_frame, bg='#007bdf', command=update_user_function)
        update_button.configure(text="UPDATE", font=(font, self.font_adjust(13)), relief='solid',
                                width=self.widget_width(12))
        update_button.place(x=self.widget_width(150), y=self.widget_height(465))

        def cancel_function():
            staff_id_entry.configure(state='normal')
            last_name_entry.configure(state='normal')
            middle_initial_entry.configure(state='normal')
            first_name_entry.configure(state='normal')
            id_number_entry.configure(state='normal')
            contact_entry.configure(state='normal')
            username_entry.configure(state='normal')
            password_entry.configure(state='normal')
            retype_password_entry.configure(state='normal')

            staff_id_entry.delete(0, END)
            last_name_entry.delete(0, END)
            middle_initial_entry.delete(0, END)
            first_name_entry.delete(0, END)
            id_number_entry.delete(0, END)
            contact_entry.delete(0, END)
            username_entry.delete(0, END)
            password_entry.delete(0, END)
            retype_password_entry.delete(0, END)

            staff_id_entry.configure(highlightbackground="black", highlightthickness=0)
            last_name_entry.configure(highlightbackground="black", highlightthickness=0)
            middle_initial_entry.configure(highlightbackground="black", highlightthickness=0)
            first_name_entry.configure(highlightbackground="black", highlightthickness=0)
            id_number_entry.configure(highlightbackground="black", highlightthickness=0)
            contact_entry.configure(highlightbackground="black", highlightthickness=0)
            username_entry.configure(highlightbackground="black", highlightthickness=0)
            password_entry.configure(highlightbackground="black", highlightthickness=0)
            retype_password_entry.configure(highlightbackground="black", highlightthickness=0)

            staff_id_entry.configure(state='disabled')
            last_name_entry.configure(state='disabled')
            middle_initial_entry.configure(state='disabled')
            first_name_entry.configure(state='disabled')
            id_number_entry.configure(state='disabled')
            contact_entry.configure(state='disabled')
            username_entry.configure(state='disabled')
            password_entry.configure(state='disabled')
            retype_password_entry.configure(state='disabled')
            role_entry.configure(state='disabled')
            status_entry.configure(state='disabled')
            save_button.configure(state='disabled')

            try:
                db_connect = connect(path_to_database)
                writ = db_connect.cursor()
                ld = "SELECT * FROM {}".format("accounts")
                writ.execute(ld)
                resu = writ.fetchall()
                db_connect.close()

                for items in accounts_treeview.get_children():
                    accounts_treeview.delete(items)

                for X in range(0, len(result)):
                    accounts_treeview.insert("", 'end', text="1",
                                             values=(resu[X][0], resu[X][1] + " " + resu[X][2] + ". "
                                                     + resu[X][3], resu[X][4], resu[X][5],
                                                     resu[X][8], resu[X][6]))
                    accounts_treeview.update_idletasks()

            except TclError:
                pass

        cancel_button = Button(staff_info_frame, bg='#007bdf', command=cancel_function)
        cancel_button.configure(text="CANCEL", font=(font, self.font_adjust(13)), relief='solid',
                                width=self.widget_width(12))
        cancel_button.place(x=self.widget_width(300), y=self.widget_height(465))

        def delete_function():
            item = accounts_treeview.focus()
            items = accounts_treeview.item(item)['values']

            try:
                conn = connect(path_to_database)
                writes = conn.cursor()
                lk_comm = "DELETE FROM {} WHERE staffid='{}'".format("accounts", items[0])
                writes.execute(lk_comm)
                conn.commit()
                conn.close()

                db_connect = connect(path_to_database)
                writ = db_connect.cursor()
                ld = "SELECT * FROM {}".format("accounts")
                writ.execute(ld)
                resu = writ.fetchall()
                db_connect.close()

                for items in accounts_treeview.get_children():
                    accounts_treeview.delete(items)

                for X in range(0, len(result)):
                    accounts_treeview.insert("", 'end', text="1",
                                             values=(resu[X][0], resu[X][1] + " " + resu[X][2] + ". "
                                                     + resu[X][3], resu[X][4], resu[X][5],
                                                     resu[X][8], resu[X][6]))
                    accounts_treeview.update_idletasks()

            except IndexError:
                pass

        delete_button = Button(staff_info_frame, bg='#d94141', command=delete_function)
        delete_button.configure(text="DELETE", font=(font, self.font_adjust(13)), relief='solid',
                                width=self.widget_width(12))
        delete_button.place(x=self.widget_width(10), y=self.widget_height(465))

        search_label = Label(advanced_search_frame)
        search_label.configure(text="Search", font=(font, self.font_adjust(12), 'bold'), bg='white')
        search_label.place(x=self.widget_width(60), y=self.widget_height(28))

        def filter_function(*args):
            items_on_treeview = accounts_treeview.get_children()
            search = search_entry_value.get().lower()

            for each_itme in items_on_treeview:
                if search in accounts_treeview.item(each_itme)['values'][1].lower():
                    search_var = accounts_treeview.item(each_itme)['values']
                    accounts_treeview.delete(each_itme)

                    accounts_treeview.insert("", 0, values=search_var)

        search_entry = Entry(advanced_search_frame, textvariable=search_entry_value)
        search_entry.configure(width=self.widget_width(60), relief='solid', font=(font, self.font_adjust(13)))
        search_entry.place(x=self.widget_width(140), y=self.widget_height(30))
        search_entry_value.trace("w", filter_function)

        role_choice_label = Label(advanced_search_frame)
        role_choice_label.configure(text="Role", font=(font, self.font_adjust(12), 'bold'), bg='white')
        role_choice_label.place(x=self.widget_width(850), y=self.widget_height(28))

        search_role_combo = Combobox(advanced_search_frame, textvariable=combobox_search)
        search_role_combo.configure(font=(font, self.font_adjust(13)), width=self.widget_width(30), state='readonly')
        search_role_combo['values'] = ['All', 'Administrator', 'Cashier']
        search_role_combo.current(0)
        search_role_combo.place(x=self.widget_width(910), y=self.widget_height(28))

        db_connection = connect(path_to_database)
        writer = db_connection.cursor()
        lookup_command = "SELECT * FROM {}".format("accounts")
        writer.execute(lookup_command)
        result = writer.fetchall()
        db_connection.close()

        for i in range(0, len(result)):
            accounts_treeview.insert("", 'end', text="1",
                                     values=(result[i][0], result[i][1] + " " + result[i][2] + ". "
                                             + result[i][3], result[i][4], result[i][5],
                                             result[i][8], result[i][6]))

        def role_filter(*args):
            def roles(role):
                db_connection = connect(path_to_database)
                writer = db_connection.cursor()
                lookup_command = "SELECT * FROM {} WHERE role='{}'".format("accounts", role)
                writer.execute(lookup_command)
                result = writer.fetchall()
                db_connection.close()

                for i in range(0, len(result)):
                    accounts_treeview.insert("", 'end', text="1",
                                             values=(result[i][0], result[i][1] + " " + result[i][2] + ". "
                                                     + result[i][3], result[i][4], result[i][5],
                                                     result[i][8], result[i][6]))

            if combobox_search.get().lower() == "all":
                for items in accounts_treeview.get_children():
                    accounts_treeview.delete(items)
                db_connection = connect(path_to_database)
                writer = db_connection.cursor()
                lookup_command = "SELECT * FROM {}".format("accounts")
                writer.execute(lookup_command)
                result = writer.fetchall()
                db_connection.close()

                for i in range(0, len(result)):
                    accounts_treeview.insert("", 'end', text="1",
                                             values=(result[i][0], result[i][1] + " " + result[i][2] + ". "
                                                     + result[i][3], result[i][4], result[i][5],
                                                     result[i][8], result[i][6]))

            elif combobox_search.get().lower() == "administrator":
                for items in accounts_treeview.get_children():
                    accounts_treeview.delete(items)
                roles("Administrator")

            else:
                for items in accounts_treeview.get_children():
                    accounts_treeview.delete(items)
                roles("Cashier")

        combobox_search.trace("w", role_filter)

        def updating_values(*args):
            item = accounts_treeview.focus()
            items = accounts_treeview.item(item)['values']

            def collect_values(field, value):
                connection = connect(path_to_database)
                write = connection.cursor()
                lk_command = "SELECT * FROM {} WHERE {}='{}'".format("accounts", field, value)
                write.execute(lk_command)
                values = write.fetchall()
                connection.close()

                return values

            try:
                vals = collect_values("staffid", items[0])

                staff_id_entry.configure(state='normal')
                last_name_entry.configure(state='normal')
                middle_initial_entry.configure(state='normal')
                first_name_entry.configure(state='normal')
                id_number_entry.configure(state='normal')
                contact_entry.configure(state='normal')
                username_entry.configure(state='normal')
                password_entry.configure(state='normal')
                retype_password_entry.configure(state='normal')

                staff_id_entry.delete(0, END)
                last_name_entry.delete(0, END)
                middle_initial_entry.delete(0, END)
                first_name_entry.delete(0, END)
                id_number_entry.delete(0, END)
                contact_entry.delete(0, END)
                username_entry.delete(0, END)
                password_entry.delete(0, END)
                retype_password_entry.delete(0, END)

                staff_id_entry.insert(0, vals[0][0])
                last_name_entry.insert(0, vals[0][1])
                middle_initial_entry.insert(0, vals[0][2])
                first_name_entry.insert(0, vals[0][3])
                id_number_entry.insert(0, vals[0][4])
                contact_entry.insert(0, vals[0][5])
                username_entry.insert(0, vals[0][6])

                if vals[0][8] == roles_values[0]:
                    role_entry.current(0)
                    role_entry.update()

                else:
                    role_entry.current(1)
                    role_entry.update()

                if status_values[0] == vals[0][9]:
                    status_entry.current(0)
                    status_entry.update()

                else:
                    status_entry.current(1)
                    status_entry.update()

                staff_id_entry.configure(state='readonly')
                last_name_entry.configure(state='readonly')
                middle_initial_entry.configure(state='readonly')
                first_name_entry.configure(state='readonly')
                id_number_entry.configure(state='readonly')
                contact_entry.configure(state='normal')
                username_entry.configure(state='normal')
                password_entry.configure(state='normal')
                retype_password_entry.configure(state='normal')
                role_entry.configure(state='normal')
                role_entry.configure(state='readonly')
                status_entry.configure(state='normal')
                status_entry.configure(state='readonly')

            except IndexError:
                pass

        accounts_treeview.bind("<Double-1>", updating_values)

        def refresh():
            try:
                db_co = connect(path_to_database)
                wri = db_co.cursor()
                ll = "SELECT * FROM {}".format("accounts")
                wri.execute(ll)
                r = wri.fetchall()
                db_co.close()

                for items in accounts_treeview.get_children():
                    accounts_treeview.delete(items)

                for X in range(0, len(result)):
                    accounts_treeview.insert("", 'end', text="1",
                                             values=(r[X][0], r[X][1] + " " + r[X][2] + ". " + r[X][3], r[X][4],
                                                     r[X][5], r[X][8], r[X][6]))

            except IndexError:
                pass

        cancel_button = Button(advanced_search_frame, bg='#aaf261', command=refresh)
        cancel_button.configure(text="Refresh", font=(font, self.font_adjust(10)), relief='solid',
                                width=self.widget_width(10))
        cancel_button.place(x=self.widget_width(720), y=self.widget_height(28))

    def reports_frame_window(self):
        reports_frame = Frame(self.window_initializer)
        reports_frame.configure(width=self.screen_width - self.widget_width(241), height=self.widget_height(710),
                                bg="white")
        reports_frame.place(x=self.widget_width(241), y=self.widget_height(90))

        tabbing_widget = Notebook(reports_frame)
        tab_1 = Frame(tabbing_widget, bg="white")
        tab_3 = Frame(tabbing_widget, bg="white")

        tabbing_widget.add(tab_1, text='All Sales')
        tabbing_widget.add(tab_3, text='Perfomance')
        tabbing_widget.place(x=self.widget_width(50), y=self.widget_height(20), width=self.widget_width(1200),
                             height=self.widget_height(690))

        def all_sales_tab():
            connection = connect(path_to_database)
            write = connection.cursor()
            lk_command = "SELECT * FROM Sales"
            write.execute(lk_command)
            vals = write.fetchall()
            connection.close()

            # ===================================== Sales Section ======================================
            columns = ('TransactionId', 'TransactionDate', 'ItemDescription', 'UnitPrice', 'QuantityBought', 'SubTotal')
            style = Style()
            style.theme_use("clam")
            style.configure('Treeview.Heading', background="#3e3f3f", foreground='white',
                            font=(font, self.font_adjust(11), 'bold'),
                            relief='none')

            cart_table = Treeview(tab_1, columns=columns, show='headings')

            cart_table.heading("# 1", text='Transaction ID', anchor="w")
            cart_table.column("# 1", stretch=NO, minwidth=self.widget_width(150), width=self.widget_width(150),
                              anchor="w")
            cart_table.heading("# 2", text='Transaction Date', anchor="w")
            cart_table.column("# 2", stretch=NO, minwidth=self.widget_width(200), width=self.widget_width(200),
                              anchor="w")
            cart_table.heading("# 3", text='Item Description', anchor="w")
            cart_table.column("# 3", stretch=NO, minwidth=self.widget_width(250), width=self.widget_width(250),
                              anchor="w")
            cart_table.heading("# 4", text='Unit Price', anchor=CENTER)
            cart_table.column("# 4", stretch=NO, minwidth=self.widget_width(150), width=self.widget_width(150),
                              anchor=CENTER)
            cart_table.heading("# 5", text='Quantity Bought', anchor=CENTER)
            cart_table.column("# 5", stretch=NO, minwidth=self.widget_width(150), width=self.widget_width(150),
                              anchor=CENTER)
            cart_table.heading("# 6", text='SubTotal', anchor=CENTER)
            cart_table.column("# 6", stretch=NO, minwidth=self.widget_width(100), width=self.widget_width(100),
                              anchor=CENTER)

            cart_table.place(x=90, y=self.widget_width(80), height=self.widget_height(500))

            for i in range(0, len(vals)):
                cart_table.insert("", END, text="1", values=(
                    "`" + str(vals[i][0]), vals[i][1], vals[i][2], vals[i][3], vals[i][4], vals[i][5]))

            def export_to_csv():
                desktop_location = path.join(path.join(path.expanduser('~')), 'Desktop')
                filepath = filedialog.askdirectory(initialdir=r"{}".format(desktop_location),
                                                   title="Select File Path")

                sales = []
                for items in cart_table.get_children():
                    sales_displayed = cart_table.item(items)
                    sales.append(sales_displayed['values'])

                display_time = strftime('%d-%B-%Y %H-%M-%S %p')

                full_path = filepath + "/" + "Export data(" + display_time + ")" + ".csv"

                headers = ['TransactionId', 'TransactionDate', 'ItemDescription', 'UnitPrice', 'QuantityBought',
                           'SubTotal']
                sale_dataframe = pd.DataFrame(sales, columns=headers)
                sale_dataframe.to_csv(full_path, index=False)
                messagebox.showinfo("File Saved", "File was saved successfully to:\n"
                                                  "{}".format(full_path))

            export_button = Button(tab_1, command=export_to_csv)
            export_button.configure(text="EXPORT", font=(font, self.font_adjust(13)), relief="solid", fg="white",
                                    bg="blue")
            export_button.place(x=self.widget_width(950), y=self.widget_height(590))

            def yesterday_sales():
                last_month = datetime.datetime.now() - relativedelta(days=1)
                yesterday_time = format(last_month, '%d/%B/%Y')

                connection = connect(path_to_database)
                write = connection.cursor()
                lk_command = "SELECT * FROM Sales WHERE TransactionDate LIKE '{}'".format(str(yesterday_time) + "%")
                write.execute(lk_command)
                values = write.fetchall()
                connection.close()

                for it in cart_table.get_children():
                    cart_table.delete(it)

                for i in range(0, len(values)):
                    cart_table.insert("", END, text="1", values=(
                        "`" + str(values[i][0]), values[i][1], values[i][2], values[i][3], values[i][4], values[i][5]))

            def today_sales():
                today = datetime.datetime.today()
                current_time = today.strftime("%d/%B/%Y")

                connection = connect(path_to_database)
                write = connection.cursor()
                lk_command = "SELECT * FROM Sales WHERE TransactionDate LIKE '{}'".format(str(current_time) + "%")
                write.execute(lk_command)
                values = write.fetchall()
                connection.close()

                for it in cart_table.get_children():
                    cart_table.delete(it)

                for i in range(0, len(values)):
                    cart_table.insert("", END, text="1", values=(
                        "`" + str(values[i][0]), values[i][1], values[i][2], values[i][3], values[i][4], values[i][5]))

            def last7_days():
                try:
                    for it in cart_table.get_children():
                        cart_table.delete(it)

                    def calculate_time(day_of_week):
                        connection = connect(path_to_database)
                        write = connection.cursor()
                        lk_command = "SELECT * FROM Sales WHERE TransactionDate LIKE '{}'".format(day_of_week + "%")
                        write.execute(lk_command)
                        values = write.fetchall()
                        connection.close()

                        return values

                    week_data = []

                    for i in range(1, 7):
                        previous_date = datetime.datetime.today() - datetime.timedelta(days=i)
                        current_time = previous_date.strftime("%d/%B/%Y")
                        week_values = calculate_time(current_time)
                        week_data.append(week_values)

                    for i in range(0, len(week_data)):
                        for sub in week_data:
                            if sub:
                                cart_table.insert("", END, text="1", values=(
                                    "`" + str(sub[i][0]), sub[i][1], sub[i][2], sub[i][3], sub[i][4], sub[i][5]))
                            else:
                                pass

                except IndexError:
                    pass

            def last_months():
                last_month = datetime.datetime.now() - relativedelta(months=1)
                last_month_day = format(last_month, '%B/%Y')

                connection = connect(path_to_database)
                write = connection.cursor()
                lk_command = "SELECT * FROM Sales WHERE TransactionDate LIKE '{}'".format("%" + last_month_day + "%")
                write.execute(lk_command)
                values = write.fetchall()
                connection.close()

                for it in cart_table.get_children():
                    cart_table.delete(it)

                for i in range(0, len(values)):
                    cart_table.insert("", END, text="1", values=(
                        "`" + str(values[i][0]), values[i][1], values[i][2], values[i][3], values[i][4], values[i][5]))

            def this_months():
                last_month = datetime.datetime.now() - relativedelta(months=0)
                last_month_day = format(last_month, '%B/%Y')

                connection = connect(path_to_database)
                write = connection.cursor()
                lk_command = "SELECT * FROM Sales WHERE TransactionDate LIKE '{}'".format("%" + last_month_day + "%")
                write.execute(lk_command)
                values = write.fetchall()
                connection.close()

                for it in cart_table.get_children():
                    cart_table.delete(it)

                for i in range(0, len(values)):
                    cart_table.insert("", END, text="1", values=(
                        "`" + str(values[i][0]), values[i][1], values[i][2], values[i][3], values[i][4], values[i][5]))

            def last_year():
                last_month = datetime.datetime.now() - relativedelta(years=1)
                last_month_day = format(last_month, '%Y')

                connection = connect(path_to_database)
                write = connection.cursor()
                lk_command = "SELECT * FROM Sales WHERE TransactionDate LIKE '{}'".format("%" + last_month_day + "%")
                write.execute(lk_command)
                values = write.fetchall()
                connection.close()

                for it in cart_table.get_children():
                    cart_table.delete(it)

                for i in range(0, len(values)):
                    cart_table.insert("", END, text="1", values=(
                        "`" + str(values[i][0]), values[i][1], values[i][2], values[i][3], values[i][4], values[i][5]))

            def this_year():
                today = datetime.datetime.today()
                current_time = today.strftime("%Y")

                connection = connect(path_to_database)
                write = connection.cursor()
                lk_command = "SELECT * FROM Sales WHERE TransactionDate LIKE '{}'".format("%" + current_time + "%")
                write.execute(lk_command)
                values = write.fetchall()
                connection.close()

                for it in cart_table.get_children():
                    cart_table.delete(it)

                for i in range(0, len(values)):
                    cart_table.insert("", END, text="1", values=(
                        "`" + str(values[i][0]), values[i][1], values[i][2], values[i][3], values[i][4], values[i][5]))

            chart_timeframe_value = StringVar()

            chart_timeframe = Combobox(tab_1, textvariable=chart_timeframe_value)
            chart_times = ["Yesterday's Sales", "Today's Sales", "Last 7 Days Sales", "This Month's Sales",
                           "Last Month's Sales", "This Year's Sales", "Last Year's Sales"]
            chart_timeframe['values'] = chart_times
            chart_timeframe.configure(state="readonly", font=(font, self.font_adjust(12)))
            chart_timeframe.place(x=self.widget_width(800), y=self.widget_height(20))

            def load_respective_chart(*args):
                if chart_timeframe_value.get() == chart_times[0]:
                    yesterday_sales()

                elif chart_timeframe_value.get() == chart_times[1]:
                    today_sales()

                elif chart_timeframe_value.get() == chart_times[2]:
                    last7_days()

                elif chart_timeframe_value.get() == chart_times[3]:
                    this_months()

                elif chart_timeframe_value.get() == chart_times[4]:
                    last_months()

                elif chart_timeframe_value.get() == chart_times[5]:
                    this_year()

                elif chart_timeframe_value.get() == chart_times[6]:
                    last_year()

                else:
                    pass

            chart_timeframe_value.trace("w", load_respective_chart)

        def performance_tab():
            performance_frame = Frame(tab_3)
            performance_frame.configure(width=self.widget_width(350), height=self.widget_height(210))
            performance_frame.configure(borderwidth=2, relief='solid')
            performance_frame.place(x=self.widget_width(200), y=self.widget_height(80))

            performance_title = Label(performance_frame)
            performance_title.configure(text="PERFORMANCE DETAILS", font=(font, self.font_adjust(14), "bold"))
            performance_title.place(x=self.widget_width(45), y=self.widget_height(3))

            most_sold_label = Label(performance_frame)
            most_sold_label.configure(text="Best Product:", font=(font, self.font_adjust(12)))
            most_sold_label.place(x=self.widget_width(10), y=self.widget_height(40))

            most_sold_item = Label(performance_frame, fg="green")
            most_sold_item.configure(font=(font, self.font_adjust(12)))
            most_sold_item.place(x=self.widget_width(135), y=self.widget_height(40))

            most_sold_sales_label = Label(performance_frame)
            most_sold_sales_label.configure(text="Sales (Kshs):", font=(font, self.font_adjust(12)))
            most_sold_sales_label.place(x=self.widget_width(10), y=self.widget_height(70))

            most_sold_sales_item = Label(performance_frame, fg="green")
            most_sold_sales_item.configure(font=(font, self.font_adjust(12)))
            most_sold_sales_item.place(x=self.widget_width(135), y=self.widget_height(70))

            most_service_label = Label(performance_frame)
            most_service_label.configure(text="Best Service:", font=(font, self.font_adjust(12)))
            most_service_label.place(x=self.widget_width(10), y=self.widget_height(120))

            most_service_item = Label(performance_frame, fg="green")
            most_service_item.configure(font=(font, self.font_adjust(12)))
            most_service_item.place(x=self.widget_width(135), y=self.widget_height(120))

            most_service_sales_label = Label(performance_frame)
            most_service_sales_label.configure(text="Sales (Kshs):", font=(font, self.font_adjust(12)))
            most_service_sales_label.place(x=self.widget_width(10), y=self.widget_height(150))

            most_service_sales_item = Label(performance_frame, fg="green")
            most_service_sales_item.configure(font=(font, self.font_adjust(12)))
            most_service_sales_item.place(x=self.widget_width(135), y=self.widget_height(150))

            def find_products(list_of_names):
                product_list = []
                for product in list_of_names:
                    connection = connect(path_to_database)
                    write = connection.cursor()
                    lk_command = "SELECT * FROM products WHERE description='{}'".format(product)
                    write.execute(lk_command)
                    values = write.fetchall()
                    connection.close()

                    if not values:
                        pass

                    else:
                        product_list.append(values[0][2])

                return set(product_list)

            def find_services(list_of_names):
                services_list = []
                for product in list_of_names:
                    connection = connect(path_to_database)
                    write = connection.cursor()
                    lk_command = "SELECT * FROM services WHERE description='{}'".format(product)
                    write.execute(lk_command)
                    values = write.fetchall()
                    connection.close()

                    if not values:
                        pass

                    else:
                        services_list.append(values[0][2])

                return set(services_list)

            def update_details(most_product, most_service, product_sales, services_sales):
                most_sold_item.configure(text=most_product)
                most_service_item.configure(text=most_service)
                most_sold_sales_item.configure(text=product_sales)
                most_service_sales_item.configure(text=services_sales)

            def pie_chart(day_dates, master):
                def debt_calculator(debt_list):
                    debt_debt = 0
                    debt_discount = 0
                    debt_total_sales = 0
                    for debts_ in debt_list:
                        debt_debt = debt_debt + debts_[7]
                        debt_total_sales = debt_total_sales + debts_[3]
                        debt_discount = debt_discount + debts_[5]

                    return debt_total_sales, 0, 0, debt_discount, debt_debt

                def cash_calculator(cash_list):
                    cash_debt = 0
                    cash_discount = 0
                    cash = 0
                    cash_sales = 0

                    for cash_ in cash_list:
                        cash_debt = cash_debt + cash_[7]
                        cash_discount = cash_discount + cash_[5]
                        cash_sales = cash_sales + cash_[3]
                        cash = cash + (cash_[4] - cash_[6] - cash_[7])

                    return cash_sales, 0, cash, cash_discount, cash_debt

                def mpesa_calculator(mpesa_list):
                    mpesa_debt = 0
                    mpesa_discount = 0
                    mpesa_sales = 0
                    mpesa_amount = 0
                    mpesa_cash = 0

                    for mpesa_ in mpesa_list:
                        mpesa_debt = mpesa_debt + mpesa_[7]
                        mpesa_discount = mpesa_discount + mpesa_[5]
                        mpesa_sales = mpesa_sales + mpesa_[3]
                        mpesa_amount = mpesa_amount + abs((mpesa_[4] - mpesa_[6]))
                        mpesa_cash = mpesa_cash + mpesa_[6]

                    return mpesa_sales, mpesa_amount, mpesa_cash, mpesa_discount, mpesa_debt

                def mpesa_cash_calculator(mpesa_list):
                    mpesa_debt = 0
                    mpesa_discount = 0
                    mpesa_sales = 0
                    mpesa_amount = 0
                    mpesa_cash = 0

                    for mpesa_ in mpesa_list:
                        mpesa_debt = mpesa_debt + mpesa_[7]
                        mpesa_discount = mpesa_discount + mpesa_[5]
                        mpesa_sales = mpesa_sales + mpesa_[3]
                        mpesa_amount = mpesa_amount + mpesa_[4]
                        mpesa_cash = mpesa_cash + mpesa_[6]

                    return mpesa_sales, mpesa_amount, mpesa_cash, mpesa_discount, mpesa_debt

                def data_collection(string_):
                    connection = connect(path_to_database)
                    write = connection.cursor()
                    lk_command = "SELECT * FROM Transactions WHERE TransactionDate LIKE '{}'".format(string_)
                    write.execute(lk_command)
                    values = write.fetchall()
                    connection.close()

                    return values

                def get_data(current_time):
                    values = data_collection(current_time)
                    try:
                        connection = connect(path_to_database)
                        write = connection.cursor()
                        lk_command = "SELECT Amount FROM Expenses WHERE Date LIKE '{}'".format(str(current_time))
                        write.execute(lk_command)
                        amounts = write.fetchall()
                        connection.close()

                        today_expense = 0
                        for expense_ in amounts:
                            today_expense = today_expense + expense_[0]

                    except IndexError:
                        today_expense = 0

                    try:
                        connection = connect(path_to_database)
                        write = connection.cursor()
                        lk_command = "SELECT Float FROM Costs WHERE Date LIKE '{}'".format(str(current_time))
                        write.execute(lk_command)
                        floats_ = write.fetchall()
                        connection.close()

                        today_float = 0
                        for float_ in floats_:
                            today_float = today_float + float_[0]

                    except IndexError:
                        today_float = 0

                    mpesa_data = []
                    cash_data = []
                    debt_data = []
                    mpesa_cash_data = []

                    for vals in values:
                        if vals[8] == "debt":
                            debt_data.append(vals)

                        if vals[8] == "cash":
                            cash_data.append(vals)

                        if vals[8] == "mpesa":
                            mpesa_data.append(vals)

                        if vals[8] == "mpesa&cash":
                            mpesa_cash_data.append(vals)

                    debt_sale, debt_mpesa, debt_cash, debt_discount, debt_debt = debt_calculator(debt_data)
                    cash_sale, cash_mpesa, cash_cash, cash_discount, cash_debt = cash_calculator(cash_data)
                    mpesa_sale, mpesa_mpesa, mpesa_cash, mpesa_discount, mpesa_debt = mpesa_calculator(mpesa_data)
                    mpesa_cash_sale, mpesa_cash_mpesa, mpesa_cash_cash, mpesa_cash_discount, mpesa_cash_debt = \
                        mpesa_cash_calculator(mpesa_cash_data)

                    total_sales = debt_sale + cash_sale + mpesa_sale + mpesa_cash_sale
                    mpesa_bal = debt_mpesa + cash_mpesa + mpesa_mpesa + mpesa_cash_mpesa
                    cash_bal = debt_cash + cash_cash + mpesa_cash + mpesa_cash_cash
                    total_discount = debt_discount + cash_discount + mpesa_discount + mpesa_cash_discount
                    total_debt = debt_debt + cash_debt + mpesa_cash_debt + mpesa_debt

                    return total_sales, mpesa_bal, cash_bal, total_discount, total_debt, today_expense, today_float

                all_vals = get_data(day_dates)
                monies_list = list(all_vals)

                summary_frame = Frame(tab_3)
                summary_frame.configure(width=self.widget_width(400), height=self.widget_height(210))
                summary_frame.configure(borderwidth=2, relief='solid')
                summary_frame.place(x=self.widget_width(650), y=self.widget_height(80))

                summary_head = Label(summary_frame)
                summary_head.configure(text="SALES SUMMARY", font=(font, self.font_adjust(14), "bold"))
                summary_head.place(x=self.widget_width(130), y=self.widget_height(3))

                total_sales_label = Label(summary_frame)
                total_sales_label.configure(text="Total Sales:", font=(font, self.font_adjust(12), "bold"))
                total_sales_label.place(x=self.widget_width(20), y=self.widget_height(40))

                total_sales_value = Label(summary_frame)
                total_sales_value.configure(text=str(monies_list[0]), font=(font, self.font_adjust(12)))
                total_sales_value.place(x=self.widget_width(130), y=self.widget_height(40))

                total_mpesa_label = Label(summary_frame)
                total_mpesa_label.configure(text="Mpesa:", font=(font, self.font_adjust(12), "bold"))
                total_mpesa_label.place(x=self.widget_width(20), y=self.widget_height(70))

                total_mpesa_value = Label(summary_frame)
                total_mpesa_value.configure(text=str(monies_list[1]), font=(font, self.font_adjust(12)))
                total_mpesa_value.place(x=self.widget_width(130), y=self.widget_height(70))

                total_cash_label = Label(summary_frame)
                total_cash_label.configure(text="Cash:", font=(font, self.font_adjust(12), "bold"))
                total_cash_label.place(x=self.widget_width(20), y=self.widget_height(100))

                total_cash_value = Label(summary_frame)
                total_cash_value.configure(text=str(monies_list[2]), font=(font, self.font_adjust(12)))
                total_cash_value.place(x=self.widget_width(130), y=self.widget_height(100))

                total_discount_label = Label(summary_frame)
                total_discount_label.configure(text="Discounts:", font=(font, self.font_adjust(12), "bold"))
                total_discount_label.place(x=self.widget_width(20), y=self.widget_height(130))

                total_discount_value = Label(summary_frame)
                total_discount_value.configure(text=str(monies_list[3]), font=(font, self.font_adjust(12)))
                total_discount_value.place(x=self.widget_width(130), y=self.widget_height(130))
                
                total_debt_label = Label(summary_frame)
                total_debt_label.configure(text="Debts:", font=(font, self.font_adjust(12), "bold"))
                total_debt_label.place(x=self.widget_width(20), y=self.widget_height(160))

                total_debt_value = Label(summary_frame)
                total_debt_value.configure(text=str(monies_list[4]), font=(font, self.font_adjust(12)))
                total_debt_value.place(x=self.widget_width(130), y=self.widget_height(160))

                total_expense_label = Label(summary_frame)
                total_expense_label.configure(text="Expenses:", font=(font, self.font_adjust(12), "bold"))
                total_expense_label.place(x=self.widget_width(220), y=self.widget_height(40))

                total_expense_value = Label(summary_frame)
                total_expense_value.configure(text=str(monies_list[5]), font=(font, self.font_adjust(12)))
                total_expense_value.place(x=self.widget_width(310), y=self.widget_height(40))

                total_float_label = Label(summary_frame)
                total_float_label.configure(text="Float:", font=(font, self.font_adjust(12), "bold"))
                total_float_label.place(x=self.widget_width(220), y=self.widget_height(70))

                total_float_value = Label(summary_frame)
                total_float_value.configure(text=str(monies_list[6]), font=(font, self.font_adjust(12)))
                total_float_value.place(x=self.widget_width(310), y=self.widget_height(70))

            def daily_chart():
                today = datetime.datetime.today()
                current_time = today.strftime("%d/%B/%Y")
                pie_chart(current_time + "%", tab_3)

                connection = connect(path_to_database)
                write = connection.cursor()
                lk_command = "SELECT * FROM Sales WHERE TransactionDate LIKE '{}'".format(current_time + "%")
                write.execute(lk_command)
                values = write.fetchall()
                connection.close()

                totals = []
                times = []
                item_names = []

                for price in values:
                    item_names.append(price[2])
                    totals.append(price[5])
                    full_time = str(price[1])
                    hours = full_time[-5] + full_time[-4]
                    times.append(hours)

                products = find_products(item_names)
                services = find_services(item_names)

                combined = list(products) + list(services) + item_names

                product_counts = Counter([item for item in combined if item in products])
                service_counts = Counter([item for item in combined if item in services])

                try:
                    most_common_product = product_counts.most_common(1)[0][0]

                except IndexError:
                    most_common_product = ""

                try:
                    most_common_service = service_counts.most_common(1)[0][0]

                except IndexError:
                    most_common_service = ""

                total_sales_product = 0
                total_sales_service = 0

                for price in values:
                    if price[2] == most_common_product:
                        total_sales_product = total_sales_product + price[5]

                    elif price[2] == most_common_service:
                        total_sales_service = total_sales_service + price[5]

                    else:
                        pass

                update_details(most_common_product, most_common_service, total_sales_product, total_sales_service)

                unique_hours = set(times)
                unique_hours_total = []
                indices = []

                data = {'Totals': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        'Hours': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
                        }

                for unique_time in unique_hours:
                    unique_time_total = 0
                    for idx, value in enumerate(times):
                        if value == unique_time:
                            unique_time_total = unique_time_total + totals[idx]
                            data['Totals'][int(unique_time)] = unique_time_total
                            indices.append(idx)
                    unique_hours_total.append(unique_time_total)

                data_frame = pd.DataFrame(data)
                figure2 = plt.Figure(figsize=(self.widget_width(10), self.widget_height(3)), dpi=100)
                ax2 = figure2.add_subplot(111)
                line2 = FigureCanvasTkAgg(figure2, tab_3)
                line2.get_tk_widget().place(x=self.widget_width(140), y=self.widget_height(320))
                df2 = data_frame[['Hours', 'Totals']].groupby('Hours').sum()
                df2.plot(kind='bar', legend=True, ax=ax2, color='g', width=0.6)
                ax2.grid()
                ax2.set_title("Today's Sales Performance")

            def yesterday_chart():
                last_month = datetime.datetime.now() - relativedelta(days=1)
                yesterday_time = format(last_month, '%d/%B/%Y')
                pie_chart(str(yesterday_time) + "%", tab_3)

                connection = connect(path_to_database)
                write = connection.cursor()
                lk_command = "SELECT * FROM Sales WHERE TransactionDate LIKE '{}'".format(str(yesterday_time) + "%")
                write.execute(lk_command)
                values = write.fetchall()
                connection.close()

                item_names = []
                totals = []
                times = []

                for price in values:
                    item_names.append(price[2])
                    totals.append(price[5])
                    full_time = str(price[1])
                    hours = full_time[-5] + full_time[-4]
                    times.append(hours)

                products = find_products(item_names)
                services = find_services(item_names)

                combined = list(products) + list(services) + item_names

                product_counts = Counter([item for item in combined if item in products])
                service_counts = Counter([item for item in combined if item in services])

                try:
                    most_common_product = product_counts.most_common(1)[0][0]

                except IndexError:
                    most_common_product = ""

                try:
                    most_common_service = service_counts.most_common(1)[0][0]

                except IndexError:
                    most_common_service = ""

                total_sales_product = 0
                total_sales_service = 0

                for price in values:
                    if price[2] == most_common_product:
                        total_sales_product = total_sales_product + price[5]

                    elif price[2] == most_common_service:
                        total_sales_service = total_sales_service + price[5]

                    else:
                        pass

                update_details(most_common_product, most_common_service, total_sales_product, total_sales_service)

                unique_hours = set(times)
                unique_hours_total = []
                indices = []

                data = {'Totals': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        'Hours': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
                        }

                for unique_time in unique_hours:
                    unique_time_total = 0
                    for idx, value in enumerate(times):
                        if value == unique_time:
                            unique_time_total = unique_time_total + totals[idx]
                            data['Totals'][int(unique_time)] = unique_time_total
                            indices.append(idx)
                    unique_hours_total.append(unique_time_total)

                data_frame = pd.DataFrame(data)
                figure2 = plt.Figure(figsize=(self.widget_width(10), self.widget_height(3)), dpi=100)
                ax2 = figure2.add_subplot(111)
                line2 = FigureCanvasTkAgg(figure2, tab_3)
                line2.get_tk_widget().place(x=self.widget_width(140), y=self.widget_height(320))
                df2 = data_frame[['Hours', 'Totals']].groupby('Hours').sum()
                df2.plot(kind='bar', legend=True, ax=ax2, color='g', width=0.6)
                ax2.grid()
                ax2.set_title("Yesterday's Sales Performance")

            def last_week_chart():
                item_names = []
                week_sales = []
                data = {'Totals': [0, 0, 0, 0, 0, 0, 0],
                        'Days': [1, 2, 3, 4, 5, 6, 7]
                        }

                def calculate_time(day_of_week):
                    connection = connect(path_to_database)
                    write = connection.cursor()
                    lk_command = "SELECT * FROM Sales WHERE TransactionDate LIKE '{}'".format(day_of_week + "%")
                    write.execute(lk_command)
                    values = write.fetchall()
                    connection.close()

                    totals = []

                    for price in values:
                        week_sales.append(price)
                        item_names.append(price[2])
                        totals.append(price[5])

                    return sum(totals)

                for i in range(1, 7):
                    previous_date = datetime.datetime.today() - datetime.timedelta(days=i)
                    current_time = previous_date.strftime("%d/%B/%Y")
                    day_total = calculate_time(current_time)
                    data['Totals'][int(i) - 1] = day_total

                products = find_products(item_names)
                services = find_services(item_names)

                combined = list(products) + list(services) + item_names

                product_counts = Counter([item for item in combined if item in products])
                service_counts = Counter([item for item in combined if item in services])

                try:
                    most_common_product = product_counts.most_common(1)[0][0]

                except IndexError:
                    most_common_product = ""

                try:
                    most_common_service = service_counts.most_common(1)[0][0]

                except IndexError:
                    most_common_service = ""

                total_sales_product = 0
                total_sales_service = 0

                for price in week_sales:
                    if price[2] == most_common_product:
                        total_sales_product = total_sales_product + price[5]

                    elif price[2] == most_common_service:
                        total_sales_service = total_sales_service + price[5]

                    else:
                        pass

                update_details(most_common_product, most_common_service, total_sales_product, total_sales_service)

                data_frame = pd.DataFrame(data)
                figure2 = plt.Figure(figsize=(self.widget_width(10), self.widget_height(3)), dpi=100)
                ax2 = figure2.add_subplot(111)
                line2 = FigureCanvasTkAgg(figure2, tab_3)
                line2.get_tk_widget().place(x=self.widget_width(140), y=self.widget_height(320))
                df2 = data_frame[['Days', 'Totals']].groupby('Days').sum()
                df2.plot(kind='bar', legend=True, ax=ax2, color='g', width=0.6)
                ax2.set_title("Last 7 Days Sales Performance")
                ax2.grid()

            def last_month_chart():
                last_month = datetime.datetime.now() - relativedelta(months=1)
                last_month_day = format(last_month, '%B/%Y')
                pie_chart("%" + last_month_day + "%", tab_3)

                connection = connect(path_to_database)
                write = connection.cursor()
                lk_command = "SELECT * FROM Sales WHERE TransactionDate LIKE '{}'".format("%" + last_month_day + "%")
                write.execute(lk_command)
                values = write.fetchall()
                connection.close()

                totals = []
                times = []
                item_names = []

                for price in values:
                    item_names.append(price[2])
                    totals.append(price[5])
                    full_time = str(price[1])
                    hours = full_time[0] + full_time[1]
                    times.append(hours)

                products = find_products(item_names)
                services = find_services(item_names)

                combined = list(products) + list(services) + item_names

                product_counts = Counter([item for item in combined if item in products])
                service_counts = Counter([item for item in combined if item in services])

                try:
                    most_common_product = product_counts.most_common(1)[0][0]

                except IndexError:
                    most_common_product = ""

                try:
                    most_common_service = service_counts.most_common(1)[0][0]

                except IndexError:
                    most_common_service = ""

                total_sales_product = 0
                total_sales_service = 0

                for price in values:
                    if price[2] == most_common_product:
                        total_sales_product = total_sales_product + price[5]

                    elif price[2] == most_common_service:
                        total_sales_service = total_sales_service + price[5]

                    else:
                        pass

                update_details(most_common_product, most_common_service, total_sales_product, total_sales_service)

                unique_hours = set(times)
                unique_hours_total = []
                indices = []

                if format(last_month, '%B') == "February":
                    total_in_month = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                      0, 0]
                    days_in_month = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
                                     24, 25, 26, 27, 28, 29]

                elif format(last_month, '%B') == "September" or format(last_month, '%B') == "April" or \
                        format(last_month, '%B') == "June" or format(last_month, '%B') == "November":
                    total_in_month = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                      0, 0, 0]
                    days_in_month = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
                                     24, 25, 26, 27, 28, 29, 30]

                else:
                    total_in_month = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                      0, 0, 0, 0]
                    days_in_month = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
                                     24, 25, 26, 27, 28, 29, 30, 31]

                data = {'Totals': total_in_month,
                        'Days': days_in_month
                        }

                for unique_time in unique_hours:
                    unique_time_total = 0
                    for idx, value in enumerate(times):
                        if value == unique_time:
                            unique_time_total = unique_time_total + totals[idx]
                            data['Totals'][int(unique_time) - 1] = unique_time_total
                            indices.append(idx)
                    unique_hours_total.append(unique_time_total)

                data_frame = pd.DataFrame(data)
                figure2 = plt.Figure(figsize=(self.widget_width(10), self.widget_height(3)), dpi=100)
                ax2 = figure2.add_subplot(111)
                line2 = FigureCanvasTkAgg(figure2, tab_3)
                line2.get_tk_widget().place(x=self.widget_width(140), y=self.widget_height(320))
                df2 = data_frame[['Days', 'Totals']].groupby('Days').sum()
                df2.plot(kind='bar', legend=True, ax=ax2, color='g', width=0.6)
                ax2.set_title("Last Month's Sales Performance")
                ax2.grid()

            def this_month_chart():
                last_month = datetime.datetime.now() - relativedelta(months=0)
                last_month_day = format(last_month, '%B/%Y')
                pie_chart("%" + last_month_day + "%", tab_3)

                connection = connect(path_to_database)
                write = connection.cursor()
                lk_command = "SELECT * FROM Sales WHERE TransactionDate LIKE '{}'".format("%" + last_month_day + "%")
                write.execute(lk_command)
                values = write.fetchall()
                connection.close()

                totals = []
                times = []
                item_names = []

                for price in values:
                    item_names.append(price[2])
                    totals.append(price[5])
                    full_time = str(price[1])
                    hours = full_time[0] + full_time[1]
                    times.append(hours)

                products = find_products(item_names)
                services = find_services(item_names)

                combined = list(products) + list(services) + item_names

                product_counts = Counter([item for item in combined if item in products])
                service_counts = Counter([item for item in combined if item in services])

                try:
                    most_common_product = product_counts.most_common(1)[0][0]

                except IndexError:
                    most_common_product = ""

                try:
                    most_common_service = service_counts.most_common(1)[0][0]

                except IndexError:
                    most_common_service = ""

                total_sales_product = 0
                total_sales_service = 0

                for price in values:
                    if price[2] == most_common_product:
                        total_sales_product = total_sales_product + price[5]

                    elif price[2] == most_common_service:
                        total_sales_service = total_sales_service + price[5]

                    else:
                        pass

                update_details(most_common_product, most_common_service, total_sales_product, total_sales_service)

                unique_hours = set(times)
                unique_hours_total = []
                indices = []

                if format(last_month, '%B') == "February":
                    total_in_month = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                      0, 0]
                    days_in_month = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
                                     24, 25, 26, 27, 28, 29]

                elif format(last_month, '%B') == "September" or format(last_month, '%B') == "April" or \
                        format(last_month, '%B') == "June" or format(last_month, '%B') == "November":
                    total_in_month = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                      0, 0, 0]
                    days_in_month = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
                                     24, 25, 26, 27, 28, 29, 30]

                else:
                    total_in_month = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                      0, 0, 0, 0]
                    days_in_month = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
                                     24, 25, 26, 27, 28, 29, 30, 31]

                data = {'Totals': total_in_month,
                        'Days': days_in_month
                        }

                for unique_time in unique_hours:
                    unique_time_total = 0
                    for idx, value in enumerate(times):
                        if value == unique_time:
                            unique_time_total = unique_time_total + totals[idx]
                            data['Totals'][int(unique_time) - 1] = unique_time_total
                            indices.append(idx)
                    unique_hours_total.append(unique_time_total)

                data_frame = pd.DataFrame(data)
                figure2 = plt.Figure(figsize=(self.widget_width(10), self.widget_height(3)), dpi=100)
                ax2 = figure2.add_subplot(111)
                line2 = FigureCanvasTkAgg(figure2, tab_3)
                line2.get_tk_widget().place(x=self.widget_width(140), y=self.widget_height(320))
                df2 = data_frame[['Days', 'Totals']].groupby('Days').sum()
                df2.plot(kind='bar', legend=True, ax=ax2, color='g', width=0.6)
                ax2.set_title("This Month's Sales Performance")
                ax2.grid()

            def last_year_chart():
                last_month = datetime.datetime.now() - relativedelta(years=1)
                last_month_day = format(last_month, '%Y')
                pie_chart("%" + last_month_day + "%", tab_3)

                connection = connect(path_to_database)
                write = connection.cursor()
                lk_command = "SELECT * FROM Sales WHERE TransactionDate LIKE '{}'".format("%" + last_month_day + "%")
                write.execute(lk_command)
                values = write.fetchall()
                connection.close()

                totals = []
                times = []
                item_names = []

                for price in values:
                    item_names.append(price[2])
                    totals.append(price[5])
                    full_time = str(price[1])
                    hours = full_time[3:]
                    mon = hours[:8]
                    first_3 = mon[:3].lower()
                    times.append(datetime.datetime.strptime(first_3, '%b').month)

                products = find_products(item_names)
                services = find_services(item_names)

                combined = list(products) + list(services) + item_names

                product_counts = Counter([item for item in combined if item in products])
                service_counts = Counter([item for item in combined if item in services])

                try:
                    most_common_product = product_counts.most_common(1)[0][0]

                except IndexError:
                    most_common_product = ""

                try:
                    most_common_service = service_counts.most_common(1)[0][0]

                except IndexError:
                    most_common_service = ""

                total_sales_product = 0
                total_sales_service = 0

                for price in values:
                    if price[2] == most_common_product:
                        total_sales_product = total_sales_product + price[5]

                    elif price[2] == most_common_service:
                        total_sales_service = total_sales_service + price[5]

                    else:
                        pass

                update_details(most_common_product, most_common_service, total_sales_product, total_sales_service)

                unique_hours = set(times)
                unique_hours_total = []
                indices = []

                data = {'Totals': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        'Months': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
                        }

                for unique_time in unique_hours:
                    unique_time_total = 0
                    for idx, value in enumerate(times):
                        if value == unique_time:
                            unique_time_total = unique_time_total + totals[idx]
                            data['Totals'][int(unique_time - 1)] = unique_time_total
                            indices.append(idx)
                    unique_hours_total.append(unique_time_total)

                data_frame = pd.DataFrame(data)
                figure2 = plt.Figure(figsize=(self.widget_width(10), self.widget_height(3)), dpi=100)
                ax2 = figure2.add_subplot(111)
                line2 = FigureCanvasTkAgg(figure2, tab_3)
                line2.get_tk_widget().place(x=self.widget_width(140), y=self.widget_height(320))
                df2 = data_frame[['Months', 'Totals']].groupby('Months').sum()
                df2.plot(kind='bar', legend=True, ax=ax2, color='g', width=0.6)
                ax2.set_title("Last Year's Sales Performance")
                ax2.grid()

            def this_year_chart():
                last_month = datetime.datetime.now() - relativedelta(years=0)
                last_month_day = format(last_month, '%Y')
                pie_chart("%" + last_month_day + "%", tab_3)

                connection = connect(path_to_database)
                write = connection.cursor()
                lk_command = "SELECT * FROM Sales WHERE TransactionDate LIKE '{}'".format("%" + last_month_day + "%")
                write.execute(lk_command)
                values = write.fetchall()
                connection.close()

                totals = []
                times = []
                item_names = []

                for price in values:
                    item_names.append(price[2])
                    totals.append(price[5])
                    full_time = str(price[1])
                    hours = full_time[3:]
                    mon = hours[:8]
                    first_3 = mon[:3].lower()
                    times.append(datetime.datetime.strptime(first_3, '%b').month)

                products = find_products(item_names)
                services = find_services(item_names)

                combined = list(products) + list(services) + item_names

                product_counts = Counter([item for item in combined if item in products])
                service_counts = Counter([item for item in combined if item in services])

                try:
                    most_common_product = product_counts.most_common(1)[0][0]

                except IndexError:
                    most_common_product = ""

                try:
                    most_common_service = service_counts.most_common(1)[0][0]

                except IndexError:
                    most_common_service = ""

                total_sales_product = 0
                total_sales_service = 0

                for price in values:
                    if price[2] == most_common_product:
                        total_sales_product = total_sales_product + price[5]

                    elif price[2] == most_common_service:
                        total_sales_service = total_sales_service + price[5]

                    else:
                        pass

                update_details(most_common_product, most_common_service, total_sales_product, total_sales_service)

                unique_hours = set(times)
                unique_hours_total = []
                indices = []

                data = {'Totals': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        'Months': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
                        }

                for unique_time in unique_hours:
                    unique_time_total = 0
                    for idx, value in enumerate(times):
                        if value == unique_time:
                            unique_time_total = unique_time_total + totals[idx]
                            data['Totals'][int(unique_time - 1)] = unique_time_total
                            indices.append(idx)
                    unique_hours_total.append(unique_time_total)

                data_frame = pd.DataFrame(data)
                figure2 = plt.Figure(figsize=(self.widget_width(10), self.widget_height(3)), dpi=100)
                ax2 = figure2.add_subplot(111)
                line2 = FigureCanvasTkAgg(figure2, tab_3)
                line2.get_tk_widget().place(x=self.widget_width(140), y=self.widget_height(320))
                df2 = data_frame[['Months', 'Totals']].groupby('Months').sum()
                df2.plot(kind='bar', legend=True, ax=ax2, color='g', width=0.6)
                ax2.set_title("This Year's Sales Performance")
                ax2.grid()

            daily_chart()

            daily_chart_button = Label(tab_3)
            daily_chart_button.configure(text="Select Chart Timeframe:", font=(font, self.font_adjust(12), "bold"),
                                         bg="white")
            daily_chart_button.place(x=self.widget_width(670), y=self.widget_height(15))

            chart_timeframe_value = StringVar()

            chart_timeframe = Combobox(tab_3, textvariable=chart_timeframe_value)
            chart_times = ["Yesterday's Sales", "Today's Sales", "Last 7 Days Sales", "This Month's Sales",
                           "Last Month's Sales", "This Year's Sales", "Last Year's Sales"]
            chart_timeframe['values'] = chart_times
            chart_timeframe.configure(state="readonly", font=(font, self.font_adjust(12)))
            chart_timeframe.place(x=self.widget_width(900), y=self.widget_height(15))

            def load_respective_chart(*args):
                if chart_timeframe_value.get() == chart_times[0]:
                    yesterday_chart()

                elif chart_timeframe_value.get() == chart_times[1]:
                    daily_chart()

                elif chart_timeframe_value.get() == chart_times[2]:
                    last_week_chart()

                elif chart_timeframe_value.get() == chart_times[3]:
                    this_month_chart()

                elif chart_timeframe_value.get() == chart_times[4]:
                    last_month_chart()

                elif chart_timeframe_value.get() == chart_times[5]:
                    this_year_chart()

                elif chart_timeframe_value.get() == chart_times[6]:
                    last_year_chart()

                else:
                    pass

            chart_timeframe_value.trace("w", load_respective_chart)

        all_sales_tab()
        performance_tab()

    def category_frame_window(self):
        self.category_code = None
        search_entry_value = StringVar()
        description_value = StringVar()

        category_style = Style()
        category_style.theme_use('clam')

        category_frame = Frame(self.window_initializer, bg='white')
        category_frame.configure(width=self.screen_width - self.widget_width(241), height=self.widget_height(710))
        category_frame.place(x=self.widget_width(241), y=self.widget_height(90))

        advanced_search_frame = Frame(category_frame)
        advanced_search_frame.configure(bg="white", width=self.screen_width - self.widget_width(320),
                                        height=self.widget_height(90))
        advanced_search_frame.configure(highlightbackground="#c2c2c0", highlightthickness=2)
        advanced_search_frame.place(x=self.widget_width(40), y=self.widget_height(34))

        advanced_search_label = Label(category_frame)
        advanced_search_label.configure(text="ADVANCED SEARCH", fg='#007bdf')
        advanced_search_label.configure(font=(font, self.font_adjust(13), 'bold'), bg='white')
        advanced_search_label.place(x=self.widget_width(80), y=self.widget_height(23))

        def filter_function(*args):
            items_on_treeview = category_treeview.get_children()
            search = search_entry_value.get().lower()

            for each_itme in items_on_treeview:
                if search in category_treeview.item(each_itme)['values'][1].lower():
                    search_var = category_treeview.item(each_itme)['values']
                    category_treeview.delete(each_itme)

                    category_treeview.insert("", 0, values=search_var)

        search_label = Label(advanced_search_frame)
        search_label.configure(text="Search", font=(font, self.font_adjust(12), 'bold'), bg='white')
        search_label.place(x=self.widget_width(80), y=self.widget_height(28))

        search_entry = Entry(advanced_search_frame, textvariable=search_entry_value)
        search_entry.configure(width=self.widget_width(60), relief='solid', font=(font, self.font_adjust(13)))
        search_entry.place(x=self.widget_width(160), y=self.widget_height(30))
        search_entry_value.trace("w", filter_function)

        category_treeview_columns = ['c1', 'c2']
        category_treeview = Treeview(category_frame, show='headings', columns=category_treeview_columns)

        category_treeview.heading("# 1", text='#', anchor='center')
        category_treeview.column("# 1", stretch=NO, minwidth=self.widget_width(80), width=self.widget_width(80),
                                 anchor="center")
        category_treeview.heading("# 2", text='Description', anchor='w')
        category_treeview.column("# 2", stretch=NO, minwidth=self.widget_width(700), width=self.widget_width(700))

        category_style.configure('Treeview.Heading', background="#3e3f3f", foreground='white',
                                 font=(font, self.font_adjust(12), 'bold'))
        category_style.configure('Treeview.Heading', relief='none')
        category_style.configure('Treeview', font=(font, self.font_adjust(12)))

        category_treeview.place(x=self.widget_width(40), y=self.widget_height(160), height=self.widget_height(520))

        def updating_treeview_data():
            try:
                db_co = connect(path_to_database)
                wri = db_co.cursor()
                ll = "SELECT * FROM {}".format("category")
                wri.execute(ll)
                r = wri.fetchall()
                db_co.close()

                for items in category_treeview.get_children():
                    category_treeview.delete(items)

                for X in range(0, len(r)):
                    category_treeview.insert("", 'end', text="1", values=(r[X][0], r[X][1]))

            except IndexError:
                pass

        updating_treeview_data()

        category_info_frame = Frame(category_frame)
        category_info_frame.configure(bg="white", width=self.widget_width(459), height=self.widget_height(520))
        category_info_frame.configure(highlightbackground="#c2c2c0", highlightthickness=2)
        category_info_frame.place(x=self.widget_width(860), y=self.widget_height(160))

        category_info_label = Label(category_frame)
        category_info_label.configure(text="CATEGORY INFORMATION", fg='#007bdf')
        category_info_label.configure(font=(font, self.font_adjust(13), 'bold'), bg='white')
        category_info_label.place(x=self.widget_width(880), y=self.widget_height(145))

        description_label = Label(category_info_frame)
        description_label.configure(text="Description:*", bg="white", font=(font, self.font_adjust(13), 'bold'))
        description_label.place(x=self.widget_width(20), y=self.widget_height(30))

        description_entry = Entry(category_info_frame, state='disabled', textvariable=description_value)
        description_entry.configure(bg="white", relief='solid', width=self.widget_width(25), justify="center")
        description_entry.configure(font=(font, self.font_adjust(12)))
        description_entry.place(x=self.widget_width(150), y=self.widget_height(30), height=self.widget_height(100))

        def save_category():
            error_count = []
            description = description_value.get().strip()

            if description == "":
                description_entry.configure(highlightbackground="red", highlightthickness=2)
                error_count.append(0)

            if len(description) < 4:
                description_entry.configure(highlightbackground="red", highlightthickness=2)
                error_count.append(0)

            if len(error_count) > 0:
                messagebox.showwarning("Database Warning!",
                                       "Fix {} error(s) found in the form".format(str(len(error_count))))

            else:
                conn = connect(path_to_database)
                c = conn.cursor()
                c.execute("SELECT categoryid FROM {}".format("category"))
                category_ids = c.fetchall()
                highest_value = max(category_ids)
                code = highest_value[0] + 1
                params = (code, description)
                c.execute("INSERT INTO category VALUES (?, ?)", params)
                conn.commit()

                updating_treeview_data()
                description_entry.delete(0, END)
                description_entry.configure(highlightbackground="black", highlightthickness=0)
                description_entry.configure(state='disabled')
                cancel_function()

        save_button = Button(category_info_frame, bg='#007bdf', fg='white', state='disabled', command=save_category)
        save_button.configure(text="SAVE", font=(font, self.font_adjust(13)), relief='solid',
                              width=self.widget_width(12))
        save_button.place(x=self.widget_width(170), y=self.widget_height(410), height=self.widget_height(45))

        def create_function():
            description_entry.configure(state='normal')
            description_entry.delete(0, END)
            description_entry.configure(highlightbackground="black", highlightthickness=0)
            save_button.configure(state='normal')

        create_button = Button(category_info_frame, bg='#f0bc00', fg='white', command=create_function)
        create_button.configure(text="CREATE NEW", font=(font, self.font_adjust(13)), relief='solid',
                                width=self.widget_width(12))
        create_button.place(x=self.widget_width(20), y=self.widget_height(410), height=self.widget_height(95))

        def update_category_function():
            description = description_value.get().strip()

            try:
                connection = connect(path_to_database)
                write = connection.cursor()
                lk_command = "SELECT * FROM {} WHERE {}='{}'".format("category", "categoryid", self.category_code)
                write.execute(lk_command)
                values = write.fetchall()
                connection.close()
                code = values[0][0]

                def updates(field, new_value):
                    conn = connect(path_to_database)
                    writes = conn.cursor()
                    lk_comm = "UPDATE {} SET {}='{}' WHERE categoryid='{}'".format("category", field, new_value, code)
                    writes.execute(lk_comm)
                    conn.commit()
                    conn.close()

                if values[0][1].lower() == description:
                    messagebox.showerror("Category Duplicate", "{} already exists!".format(description))

                elif len(description) < 4:
                    messagebox.showwarning("Short Name", "{} is too short".format(description))

                else:
                    updates("description", description)
                    updating_treeview_data()
                    cancel_function()

            except IndexError:
                pass

            except TclError:
                pass

        update_button = Button(category_info_frame, bg='#007bdf', fg='white', command=update_category_function)
        update_button.configure(text="UPDATE", font=(font, self.font_adjust(13)), relief='solid',
                                width=self.widget_width(12))
        update_button.place(x=self.widget_width(310), y=self.widget_height(410), height=self.widget_height(45))

        def delete_category_function():
            item = category_treeview.focus()
            items = category_treeview.item(item)['values']

            try:
                conn = connect(path_to_database)
                writes = conn.cursor()
                lk_comm = "DELETE FROM {} WHERE categoryid='{}'".format("category", items[0])
                writes.execute(lk_comm)
                conn.commit()
                conn.close()

                updating_treeview_data()
                cancel_function()

            except IndexError:
                pass

        delete_button = Button(category_info_frame, bg='#d94141', fg='white', command=delete_category_function)
        delete_button.configure(text="DELETE", font=(font, self.font_adjust(13)), relief='solid',
                                width=self.widget_width(12))
        delete_button.place(x=self.widget_width(170), y=self.widget_height(460), height=self.widget_height(45))

        def cancel_function():
            description_entry.configure(state='normal')
            description_entry.delete(0, END)
            description_entry.configure(state='disabled')
            save_button.configure(state='disabled')

            description_entry.configure(highlightbackground="black", highlightthickness=0)
            updating_treeview_data()

        cancel_button = Button(category_info_frame, bg='#007bdf', fg='white', command=cancel_function)
        cancel_button.configure(text="CANCEL", font=(font, self.font_adjust(13)), relief='solid',
                                width=self.widget_width(12))
        cancel_button.place(x=self.widget_width(310), y=self.widget_height(460), height=self.widget_height(45))

        def updating_values(*args):
            item = category_treeview.focus()
            items = category_treeview.item(item)['values']

            def collect_values(field, value):
                connection = connect(path_to_database)
                write = connection.cursor()
                lk_command = "SELECT * FROM {} WHERE {}='{}'".format("category", field, value)
                write.execute(lk_command)
                values = write.fetchall()
                connection.close()

                return values

            try:
                vals = collect_values("description", items[1])
                description_entry.configure(state='normal')
                description_entry.delete(0, END)
                description_entry.insert(0, vals[0][1])
                self.category_code = vals[0][0]

            except IndexError:
                pass

        category_treeview.bind("<Double-1>", updating_values)

    def products_frame_window(self):
        search_entry_value = StringVar()
        combobox_search = StringVar()

        product_code_value = StringVar()
        description_value = StringVar()
        category_value = StringVar()
        unit_price_value = DoubleVar()
        re_order_level_value = IntVar()

        products_style = Style()
        products_style.theme_use('clam')

        products_frame = Frame(self.window_initializer, bg='white')
        products_frame.configure(width=self.screen_width - self.widget_width(241), height=self.widget_height(710))
        products_frame.place(x=self.widget_width(241), y=self.widget_height(90))

        advanced_search_frame = Frame(products_frame)
        advanced_search_frame.configure(bg="white", width=self.screen_width - self.widget_width(320),
                                        height=self.widget_height(90))
        advanced_search_frame.configure(highlightbackground="#c2c2c0", highlightthickness=2)
        advanced_search_frame.place(x=self.widget_width(40), y=self.widget_height(34))

        advanced_search_label = Label(products_frame)
        advanced_search_label.configure(text="ADVANCED SEARCH", fg='#007bdf')
        advanced_search_label.configure(font=(font, self.font_adjust(13), 'bold'), bg='white')
        advanced_search_label.place(x=self.widget_width(80), y=self.widget_height(23))

        products_treeview_columns = ['c1', 'c2', 'c3', 'c4', 'c5', 'c6']
        products_treeview = Treeview(products_frame, show='headings', columns=products_treeview_columns)

        products_treeview.heading("# 1", text='#', anchor='w')
        products_treeview.column("# 1", stretch=NO, minwidth=self.widget_width(40), width=self.widget_width(40))
        products_treeview.heading("# 2", text='Code', anchor='w')
        products_treeview.column("# 2", stretch=NO, minwidth=self.widget_width(120), width=self.widget_width(120))
        products_treeview.heading("# 3", text='Description', anchor='w')
        products_treeview.column("# 3", stretch=NO, minwidth=self.widget_width(230), width=self.widget_width(230))
        products_treeview.heading("# 4", text='Category', anchor='w')
        products_treeview.column("# 4", stretch=NO, minwidth=self.widget_width(180), width=self.widget_width(180))
        products_treeview.heading("# 5", text='Price', anchor='w')
        products_treeview.column("# 5", stretch=NO, minwidth=self.widget_width(100), width=self.widget_width(100))
        products_treeview.heading("# 6", text='Re-order', anchor='w')
        products_treeview.column("# 6", stretch=NO, minwidth=self.widget_width(90), width=self.widget_width(90))

        products_style.configure('Treeview.Heading', background="#3e3f3f", foreground='white',
                                 font=(font, self.font_adjust(11), 'bold'))
        products_style.configure('Treeview.Heading', relief='none')
        products_style.configure('Treeview', font=(font, self.font_adjust(11)))

        products_treeview.place(x=self.widget_width(40), y=self.widget_height(160), height=self.widget_height(520))

        connection = connect(path_to_database)
        write = connection.cursor()
        lk_command = "SELECT description FROM {}".format("category")
        write.execute(lk_command)
        values = write.fetchall()
        connection.close()
        category = ["All"]

        for categories in values:
            category.append(categories[0])

        search_role_combo = Combobox(advanced_search_frame, textvariable=combobox_search)
        search_role_combo.configure(font=(font, self.font_adjust(13)), width=self.widget_width(30), state='readonly')
        search_role_combo['values'] = category
        search_role_combo.current(0)
        search_role_combo.place(x=self.widget_width(910), y=self.widget_height(28))

        def role_filter(*args):
            updating_treeview_data()

            def roles(role):
                db_connection = connect(path_to_database)
                writer = db_connection.cursor()
                lookup_command = "SELECT * FROM {} WHERE category='{}'".format("products", role)
                writer.execute(lookup_command)
                result = writer.fetchall()
                db_connection.close()

                for item in products_treeview.get_children():
                    products_treeview.delete(item)

                for i in range(0, len(result)):
                    products_treeview.insert("", 'end', text="1",
                                             values=(result[i][0], result[i][1], result[i][2], result[i][3],
                                                     result[i][4], result[i][5]))

            if combobox_search.get().lower() == "all":
                updating_treeview_data()

            else:
                for ix in range(1, len(products_treeview.get_children())):
                    try:
                        if combobox_search.get() == \
                                products_treeview.item(products_treeview.get_children()[0])['values'][3]:
                            updating_treeview_data()
                            for item in products_treeview.get_children():
                                products_treeview.delete(item)

                            roles(combobox_search.get())

                        else:
                            roles(combobox_search.get())

                    except IndexError:
                        pass

        combobox_search.trace("w", role_filter)

        def updating_treeview_data():
            try:
                db_co = connect(path_to_database)
                wri = db_co.cursor()
                ll = "SELECT * FROM {}".format("products")
                wri.execute(ll)
                r = wri.fetchall()
                db_co.close()

                for items in products_treeview.get_children():
                    products_treeview.delete(items)

                for X in range(0, len(r)):
                    products_treeview.insert("", 'end', text="1", values=(r[X][0], r[X][1], r[X][2], r[X][3], r[X][4],
                                                                          r[X][5]))

            except IndexError:
                pass

        updating_treeview_data()

        products_info_frame = Frame(products_frame)
        products_info_frame.configure(bg="white", width=self.widget_width(459), height=self.widget_height(520))
        products_info_frame.configure(highlightbackground="#c2c2c0", highlightthickness=2)
        products_info_frame.place(x=self.widget_width(860), y=self.widget_height(160))

        products_info_label = Label(products_frame)
        products_info_label.configure(text="PRODUCTS INFORMATION", fg='#007bdf')
        products_info_label.configure(font=(font, self.font_adjust(13), 'bold'), bg='white')
        products_info_label.place(x=self.widget_width(880), y=self.widget_height(145))

        product_code_label = Label(products_info_frame)
        product_code_label.configure(text="Product Code:*", font=(font, self.font_adjust(13)), bg='white')
        product_code_label.place(x=self.widget_width(20), y=self.widget_height(20))

        product_code_entry = Entry(products_info_frame, textvariable=product_code_value)
        product_code_entry.configure(relief='solid', font=(font, self.font_adjust(13)), width=self.widget_width(30),
                                     state='disabled')
        product_code_entry.place(x=self.widget_width(170), y=self.widget_height(20))

        description_label = Label(products_info_frame)
        description_label.configure(text="Description:*", font=(font, self.font_adjust(13)), bg='white')
        description_label.place(x=self.widget_width(20), y=self.widget_height(65))

        description_entry = Entry(products_info_frame, textvariable=description_value)
        description_entry.configure(relief='solid', font=(font, self.font_adjust(11)), width=self.widget_width(30),
                                    state='disabled', justify='center')
        description_entry.place(x=self.widget_width(170), y=self.widget_height(65), height=self.widget_height(72))

        category_label = Label(products_info_frame)
        category_label.configure(text="Category:*", font=(font, self.font_adjust(13)), bg='white')
        category_label.place(x=self.widget_width(20), y=self.widget_height(155))

        try:
            category_entry = Combobox(products_info_frame, textvariable=category_value, state='readonly')
            category_entry['values'] = category[1:]
            category_entry.current(0)
            category_entry.configure(font=(font, self.font_adjust(13)), width=self.widget_width(28), state='disabled')
            category_entry.place(x=self.widget_width(170), y=self.widget_height(155))

        except TclError:
            category_entry = Combobox(products_info_frame, textvariable=category_value, state='readonly')
            category_entry['values'] = [""]
            category_entry.current(0)
            category_entry.configure(font=(font, self.font_adjust(13)), width=self.widget_width(28), state='disabled')
            category_entry.place(x=self.widget_width(170), y=self.widget_height(155))

        unit_price_label = Label(products_info_frame)
        unit_price_label.configure(text="Unit price:*", font=(font, self.font_adjust(13)), bg='white')
        unit_price_label.place(x=self.widget_width(20), y=self.widget_height(200))

        unit_price_entry = Entry(products_info_frame, textvariable=unit_price_value)
        unit_price_entry.configure(relief='solid', font=(font, self.font_adjust(13)), width=self.widget_width(30),
                                   state='disabled')
        unit_price_entry.place(x=self.widget_width(170), y=self.widget_height(200))

        re_order_level_label = Label(products_info_frame)
        re_order_level_label.configure(text="Re-Order Level:*", font=(font, self.font_adjust(13)), bg='white')
        re_order_level_label.place(x=self.widget_width(20), y=self.widget_height(245))

        re_order_level_entry = Entry(products_info_frame, textvariable=re_order_level_value)
        re_order_level_entry.configure(relief='solid', font=(font, self.font_adjust(13)), width=self.widget_width(30),
                                       state='disabled')
        re_order_level_entry.place(x=self.widget_width(170), y=self.widget_height(245))

        def save_function():
            error_counter = []
            product_code = product_code_value.get().strip()
            description = description_value.get().strip()
            category_v = category_value.get().strip()

            try:
                unit_price = unit_price_value.get()

            except TclError:
                messagebox.showerror("Database Error", "ID number should be numbers only! \nDon't start with 0")
                unit_price = 0

            try:
                re_order_level = re_order_level_value.get()

            except TclError:
                messagebox.showerror("Database Error", "ID number should be numbers only! \nDon't start with 0")
                re_order_level = 0

            def collect_values(field, value):
                connection = connect(path_to_database)
                write = connection.cursor()
                lk_command = "SELECT * FROM {} WHERE {}='{}'".format("products", field, value)
                write.execute(lk_command)
                values = write.fetchall()
                connection.close()

                return values

            if product_code == "" or len(product_code) < 3 or len(collect_values("productcode", product_code)) > 0:
                product_code_entry.configure(highlightbackground="red", highlightthickness=2)
                error_counter.append(0)

            if description == "" or len(description) < 3 or len(collect_values("description", description)) > 0:
                description_entry.configure(highlightbackground="red", highlightthickness=2)
                error_counter.append(0)

            if category == "":
                messagebox.showwarning("Category error!", "Please create a category to link to!")
                error_counter.append(0)

            if unit_price == 0.00 or unit_price > 10000000:
                unit_price_entry.configure(highlightbackground="red", highlightthickness=2)
                error_counter.append(0)

            if re_order_level == 0 or re_order_level > 10000:
                re_order_level_entry.configure(highlightbackground="red", highlightthickness=2)
                error_counter.append(0)

            if len(error_counter) > 0:
                messagebox.showwarning("Form fil error!",
                                       "Fix {} error(s) in the form first".format(len(error_counter)))

            else:
                today = datetime.datetime.today()
                current_time = today.strftime("%d/%B/%Y %H:%M")

                conn = connect(path_to_database)
                c = conn.cursor()
                c.execute("SELECT productid FROM {}".format("products"))
                product_ids = c.fetchall()
                try:
                    highest_value = max(product_ids)
                    code = highest_value[0] + 1

                except ValueError:
                    code = 0
                params = (code, product_code, description, category_v, unit_price, re_order_level, current_time)
                c.execute("INSERT INTO products VALUES (?, ?, ?, ?, ?, ?, ?)", params)
                conn.commit()

                if category_v != "Printing":
                    params2 = (code, product_code, description, 0, "")
                    c.execute("INSERT INTO stock VALUES (?, ?, ?, ?, ?)", params2)
                    conn.commit()

                updating_treeview_data()
                cancel_function()

        save_button = Button(products_info_frame, bg='#007bdf', fg='white', state='disabled', command=save_function)
        save_button.configure(text="SAVE", font=(font, self.font_adjust(13)), relief='solid',
                              width=self.widget_width(12))
        save_button.place(x=self.widget_width(170), y=self.widget_height(410), height=self.widget_height(45))

        def create_function():
            product_code_entry.configure(state='normal')
            product_code_entry.delete(0, END)
            product_code_entry.configure(highlightbackground="black", highlightthickness=0)

            description_entry.configure(state='normal')
            description_entry.delete(0, END)
            description_entry.configure(highlightbackground="black", highlightthickness=0)

            category_entry.configure(state='readonly')
            category_entry.current(0)

            unit_price_entry.configure(state='normal')
            unit_price_entry.delete(0, END)
            unit_price_entry.configure(highlightbackground="black", highlightthickness=0)

            re_order_level_entry.configure(state='normal')
            re_order_level_entry.delete(0, END)
            re_order_level_entry.configure(highlightbackground="black", highlightthickness=0)

            save_button.configure(state='normal')

        create_button = Button(products_info_frame, bg='#f0bc00', fg='white', command=create_function)
        create_button.configure(text="CREATE NEW", font=(font, self.font_adjust(13)), relief='solid',
                                width=self.widget_width(12))
        create_button.place(x=self.widget_width(20), y=self.widget_height(410), height=self.widget_height(95))

        def update_products_function():
            product_code = product_code_value.get()
            description = description_value.get()
            category_v = category_value.get()
            unit_price = unit_price_value.get()
            re_order_level = re_order_level_value.get()

            try:
                c = connect(path_to_database)
                wr = c.cursor()
                lk_c = "SELECT * FROM {} WHERE {}='{}'".format("products", "productid", self.category_code)
                wr.execute(lk_c)
                valu = wr.fetchall()
                c.close()
                code = valu[0][0]

                def updates(field, new_value):
                    conn = connect(path_to_database)
                    writes = conn.cursor()
                    lk_comm = "UPDATE {} SET {}='{}' WHERE productid='{}'".format("products", field, new_value, code)
                    writes.execute(lk_comm)
                    conn.commit()
                    conn.close()

                def stock_update(field, new_value):
                    conn = connect(path_to_database)
                    writes = conn.cursor()
                    lk_comm = "UPDATE {} SET {}='{}' WHERE stockid='{}'".format("stock", field, new_value, code)
                    writes.execute(lk_comm)
                    conn.commit()
                    conn.close()

                if product_code == "" or len(product_code) < 3:
                    messagebox.showerror("Product code error", "{} contains errors".format(product_code))

                elif description == "" or len(description) < 3:
                    messagebox.showerror("Description error", "{} contains errors".format(description))

                elif category_v == "" or len(category_v) < 3:
                    messagebox.showerror("Category error", "{} contains errors".format(category_v))

                elif unit_price == 0.00 or unit_price > 100000000.00:
                    messagebox.showerror("Price range error", "{} contains errors".format(unit_price))

                elif re_order_level < 1 or unit_price > 10000.00:
                    messagebox.showerror("Order level error", "{} contains errors".format(re_order_level))

                else:
                    if category_v != "Printing":
                        def collect_values(field, value):
                            connection = connect(path_to_database)
                            write = connection.cursor()
                            lk_command = "SELECT * FROM {} WHERE {}='{}'".format("stock", field, value)
                            write.execute(lk_command)
                            values = write.fetchall()
                            connection.close()

                            return values

                        if len(collect_values("stockid", self.category_code)) > 0:
                            stock_update("productcode", product_code)
                            stock_update("description", description)

                            updates("productcode", product_code)
                            updates("description", description)
                            updates("category", category_v)
                            updates("price", unit_price)
                            updates("reorder", re_order_level)
                            cancel_function()

                        else:
                            conn = connect(path_to_database)
                            c = conn.cursor()
                            params2 = (code, product_code, description, 0, "")
                            c.execute("INSERT INTO stock VALUES (?, ?, ?, ?, ?)", params2)
                            conn.commit()
                            conn.close()

                            updates("productcode", product_code)
                            updates("description", description)
                            updates("category", category_v)
                            updates("price", unit_price)
                            updates("reorder", re_order_level)
                            cancel_function()

                    else:
                        conn = connect(path_to_database)
                        writes = conn.cursor()
                        writes.execute("DELETE FROM {} WHERE stockid='{}'".format("stock", self.category_code))
                        conn.commit()
                        conn.close()

                        updates("productcode", product_code)
                        updates("description", description)
                        updates("category", category_v)
                        updates("price", unit_price)
                        updates("reorder", re_order_level)
                        cancel_function()

            except IndexError:
                pass

            except TclError:
                pass

        update_button = Button(products_info_frame, bg='#007bdf', fg='white', command=update_products_function)
        update_button.configure(text="UPDATE", font=(font, self.font_adjust(13)), relief='solid',
                                width=self.widget_width(12))
        update_button.place(x=self.widget_width(310), y=self.widget_height(410), height=self.widget_height(45))

        def delete_function():
            item = products_treeview.focus()
            items = products_treeview.item(item)['values']

            try:
                conn = connect(path_to_database)
                writes = conn.cursor()
                lk_comm = "DELETE FROM {} WHERE productid='{}'".format("products", items[0])
                writes.execute(lk_comm)
                conn.commit()
                writes.execute("DELETE FROM {} WHERE stockid='{}'".format("stock", items[0]))
                conn.commit()
                conn.close()

                updating_treeview_data()
                cancel_function()

            except IndexError:
                pass

        delete_button = Button(products_info_frame, bg='#d94141', fg='white', command=delete_function)
        delete_button.configure(text="DELETE", font=(font, self.font_adjust(13)), relief='solid',
                                width=self.widget_width(12))
        delete_button.place(x=self.widget_width(170), y=self.widget_height(460), height=self.widget_height(45))

        def cancel_function():
            product_code_entry.configure(state='normal')
            product_code_entry.delete(0, END)
            product_code_entry.configure(highlightbackground="black", highlightthickness=0)
            product_code_entry.configure(state='disabled')

            description_entry.configure(state='normal')
            description_entry.delete(0, END)
            description_entry.configure(highlightbackground="black", highlightthickness=0)
            description_entry.configure(state='disabled')

            category_entry.configure(state='readonly')
            category_entry.current(0)
            category_entry.configure(state='disabled')

            unit_price_entry.configure(state='normal')
            unit_price_entry.delete(0, END)
            unit_price_entry.configure(highlightbackground="black", highlightthickness=0)
            unit_price_entry.configure(state='disabled')

            re_order_level_entry.configure(state='normal')
            re_order_level_entry.delete(0, END)
            re_order_level_entry.configure(highlightbackground="black", highlightthickness=0)
            re_order_level_entry.configure(state='disabled')

            save_button.configure(state='disabled')
            updating_treeview_data()

        cancel_button = Button(products_info_frame, bg='#007bdf', fg='white', command=cancel_function)
        cancel_button.configure(text="CANCEL", font=(font, self.font_adjust(13)), relief='solid',
                                width=self.widget_width(12))
        cancel_button.place(x=self.widget_width(310), y=self.widget_height(460), height=self.widget_height(45))

        def filter_function(*args):
            items_on_treeview = products_treeview.get_children()
            search = search_entry_value.get().lower()

            for each_itme in items_on_treeview:
                if search in products_treeview.item(each_itme)['values'][2].lower():
                    search_var = products_treeview.item(each_itme)['values']
                    products_treeview.delete(each_itme)

                    products_treeview.insert("", 0, values=search_var)

        search_entry = Entry(advanced_search_frame, textvariable=search_entry_value)
        search_entry.configure(width=self.widget_width(60), relief='solid', font=(font, self.font_adjust(13)))
        search_entry.place(x=self.widget_width(140), y=self.widget_height(30))
        search_entry_value.trace("w", filter_function)

        search_label = Label(advanced_search_frame)
        search_label.configure(text="Search", font=(font, self.font_adjust(12), 'bold'), bg='white')
        search_label.place(x=self.widget_width(80), y=self.widget_height(28))

        role_choice_label = Label(advanced_search_frame)
        role_choice_label.configure(text="Category", font=(font, self.font_adjust(12), 'bold'), bg='white')
        role_choice_label.place(x=self.widget_width(820), y=self.widget_height(28))

        def updating_values(*args):
            item = products_treeview.focus()
            items = products_treeview.item(item)['values']

            def collect_values(field, value):
                conn = connect(path_to_database)
                wri = conn.cursor()
                lk_comm = "SELECT * FROM {} WHERE {}='{}'".format("products", field, value)
                wri.execute(lk_comm)
                va = wri.fetchall()
                conn.close()

                return va

            try:
                vals = collect_values("productid", items[0])

                product_code_entry.configure(state='normal')
                product_code_entry.delete(0, END)
                product_code_entry.insert(0, vals[0][1])

                description_entry.configure(state='normal')
                description_entry.delete(0, END)
                description_entry.insert(0, vals[0][2])

                try:
                    category_entry.configure(state='readonly')
                    category_entry.current(0)

                except TclError:
                    category_entry.configure(state='readonly')

                unit_price_entry.configure(state='normal')
                unit_price_entry.delete(0, END)
                unit_price_entry.insert(0, vals[0][4])

                re_order_level_entry.configure(state='normal')
                re_order_level_entry.delete(0, END)
                re_order_level_entry.insert(0, vals[0][5])

                self.category_code = vals[0][0]

            except IndexError:
                pass

        products_treeview.bind("<Double-1>", updating_values)

    def services_frame_window(self):
        search_entry_value = StringVar()
        service_code_value = StringVar()
        description_value = StringVar()
        price_value = DoubleVar()

        services_style = Style()
        services_style.theme_use('clam')

        services_frame = Frame(self.window_initializer, bg='white')
        services_frame.configure(width=self.screen_width - self.widget_width(241), height=self.widget_height(710))
        services_frame.place(x=self.widget_width(241), y=self.widget_height(90))

        advanced_search_frame = Frame(services_frame)
        advanced_search_frame.configure(bg="white", width=self.screen_width - self.widget_width(320),
                                        height=self.widget_height(90))
        advanced_search_frame.configure(highlightbackground="#c2c2c0", highlightthickness=2)
        advanced_search_frame.place(x=self.widget_width(40), y=self.widget_height(34))

        advanced_search_label = Label(services_frame)
        advanced_search_label.configure(text="ADVANCED SEARCH", fg='#007bdf')
        advanced_search_label.configure(font=(font, self.font_adjust(13), 'bold'), bg='white')
        advanced_search_label.place(x=self.widget_width(80), y=self.widget_height(20))

        services_treeview_columns = ['c1', 'c2', 'c3', 'c4']
        services_treeview = Treeview(services_frame, show='headings', columns=services_treeview_columns)

        services_treeview.heading("# 1", text='#', anchor='center')
        services_treeview.column("# 1", stretch=NO, minwidth=self.widget_width(80), width=self.widget_width(80),
                                 anchor="center")
        services_treeview.heading("# 2", text='Service Code', anchor='w')
        services_treeview.column("# 2", stretch=NO, minwidth=self.widget_width(130), width=self.widget_width(130))
        services_treeview.heading("# 3", text='Description', anchor='w')
        services_treeview.column("# 3", stretch=NO, minwidth=self.widget_width(400), width=self.widget_width(400))
        services_treeview.heading("# 4", text='Price', anchor='center')
        services_treeview.column("# 4", stretch=NO, minwidth=self.widget_width(100), width=self.widget_width(100),
                                 anchor='center')

        services_style.configure('Treeview.Heading', background="#3e3f3f", foreground='white',
                                 font=(font, self.font_adjust(12), 'bold'))
        services_style.configure('Treeview.Heading', relief='none')
        services_style.configure('Treeview', font=(font, self.font_adjust(12)))

        def updating_treeview_data():
            try:
                db_co = connect(path_to_database)
                wri = db_co.cursor()
                ll = "SELECT * FROM {}".format("services")
                wri.execute(ll)
                r = wri.fetchall()
                db_co.close()

                for items in services_treeview.get_children():
                    services_treeview.delete(items)

                for X in range(0, len(r)):
                    services_treeview.insert("", 'end', text="1", values=(r[X][0], r[X][1], r[X][2], r[X][3]))

            except IndexError:
                pass

        updating_treeview_data()

        services_treeview.place(x=self.widget_width(40), y=self.widget_height(160), height=self.widget_height(520))

        def filter_function(*args):
            items_on_treeview = services_treeview.get_children()
            search = search_entry_value.get().lower()

            for each_itme in items_on_treeview:
                if search in services_treeview.item(each_itme)['values'][2].lower():
                    search_var = services_treeview.item(each_itme)['values']
                    services_treeview.delete(each_itme)

                    services_treeview.insert("", 0, values=search_var)

        search_label = Label(advanced_search_frame)
        search_label.configure(text="Search", font=(font, self.font_adjust(12), 'bold'), bg='white')
        search_label.place(x=self.widget_width(50), y=self.widget_height(28))

        search_entry = Entry(advanced_search_frame, textvariable=search_entry_value)
        search_entry.configure(width=self.widget_width(60), relief='solid', font=(font, self.font_adjust(13)))
        search_entry.place(x=self.widget_width(140), y=self.widget_height(30))
        search_entry_value.trace("w", filter_function)

        services_info_frame = Frame(services_frame)
        services_info_frame.configure(bg="white", width=self.widget_width(459), height=self.widget_height(520))
        services_info_frame.configure(highlightbackground="#c2c2c0", highlightthickness=2)
        services_info_frame.place(x=self.widget_width(860), y=self.widget_height(160))

        services_info_label = Label(services_frame)
        services_info_label.configure(text="SERVICES INFORMATION", fg='#007bdf')
        services_info_label.configure(font=(font, self.font_adjust(13), 'bold'), bg='white')
        services_info_label.place(x=self.widget_width(880), y=self.widget_height(145))

        service_code_label = Label(services_info_frame)
        service_code_label.configure(text="Service code:*", bg="white", font=(font, self.font_adjust(13), 'bold'))
        service_code_label.place(x=self.widget_width(20), y=self.widget_height(30))

        service_code_entry = Entry(services_info_frame, state='disabled', textvariable=service_code_value)
        service_code_entry.configure(bg="white", relief='solid', width=self.widget_width(25))
        service_code_entry.configure(font=(font, self.font_adjust(12)))
        service_code_entry.place(x=self.widget_width(150), y=self.widget_height(30))

        description_label = Label(services_info_frame)
        description_label.configure(text="Description:*", bg="white", font=(font, self.font_adjust(13), 'bold'))
        description_label.place(x=self.widget_width(20), y=self.widget_height(75))

        description_entry = Entry(services_info_frame, state='disabled', textvariable=description_value)
        description_entry.configure(bg="white", relief='solid', width=self.widget_width(25), justify="center")
        description_entry.configure(font=(font, self.font_adjust(12)))
        description_entry.place(x=self.widget_width(150), y=self.widget_height(75), height=self.widget_height(100))

        price_label = Label(services_info_frame)
        price_label.configure(text="Price:*", bg="white", font=(font, self.font_adjust(13), 'bold'))
        price_label.place(x=self.widget_width(20), y=self.widget_height(200))

        price_entry = Entry(services_info_frame, state='disabled', textvariable=price_value)
        price_entry.configure(bg="white", relief='solid', width=self.widget_width(25))
        price_entry.configure(font=(font, self.font_adjust(12)))
        price_entry.place(x=self.widget_width(150), y=self.widget_height(200))

        def save_service():
            error_count = []
            service_code = service_code_value.get().strip()
            description = description_value.get().strip()
            price = price_value.get()

            def collect_values(field, value):
                connection = connect(path_to_database)
                write = connection.cursor()
                lk_command = "SELECT * FROM {} WHERE {}='{}'".format("services", field, value)
                write.execute(lk_command)
                values = write.fetchall()
                connection.close()

                return values

            if service_code == "" or len(service_code) < 4 or len(collect_values("servicecode", service_code)) > 0:
                service_code_entry.configure(highlightbackground="red", highlightthickness=2)
                error_count.append(0)

            if description == "" or len(description) < 4 or len(collect_values("description", description)) > 0:
                description_entry.configure(highlightbackground="red", highlightthickness=2)
                error_count.append(0)

            if price < 1 or price > 10000000:
                price_entry.configure(highlightbackground="red", highlightthickness=2)
                error_count.append(0)

            if len(error_count) > 0:
                messagebox.showwarning("Database Warning!",
                                       "Fix {} error(s) found in the form".format(str(len(error_count))))

            else:
                today = datetime.datetime.today()
                current_time = today.strftime("%d/%B/%Y %H:%M")

                conn = connect(path_to_database)
                c = conn.cursor()
                c.execute("SELECT serviceid FROM {}".format("services"))
                category_ids = c.fetchall()
                try:
                    highest_value = max(category_ids)
                    code = highest_value[0] + 1

                except ValueError:
                    code = 1

                params = (code, service_code, description, price, current_time)
                c.execute("INSERT INTO services VALUES (?, ?, ?, ?, ?)", params)
                conn.commit()

                updating_treeview_data()
                cancel_function()

        save_button = Button(services_info_frame, bg='#007bdf', fg='white', state='disabled', command=save_service)
        save_button.configure(text="SAVE", font=(font, self.font_adjust(13)), relief='solid',
                              width=self.widget_width(12))
        save_button.place(x=self.widget_width(170), y=self.widget_height(410), height=self.widget_height(45))

        def create_function():
            service_code_entry.configure(state='normal')
            service_code_entry.delete(0, END)
            service_code_entry.configure(highlightbackground="black", highlightthickness=0)

            description_entry.configure(state='normal')
            description_entry.delete(0, END)
            description_entry.configure(highlightbackground="black", highlightthickness=0)

            price_entry.configure(state='normal')
            price_entry.delete(0, END)
            price_entry.configure(highlightbackground="black", highlightthickness=0)

            save_button.configure(state='normal')

        create_button = Button(services_info_frame, bg='#f0bc00', fg='white', command=create_function)
        create_button.configure(text="CREATE NEW", font=(font, self.font_adjust(13)), relief='solid',
                                width=self.widget_width(12))
        create_button.place(x=self.widget_width(20), y=self.widget_height(410), height=self.widget_height(95))

        def update_service_function():
            service_code = service_code_value.get()
            description = description_value.get()
            price = price_value.get()

            try:
                c = connect(path_to_database)
                wr = c.cursor()
                lk_c = "SELECT * FROM {} WHERE {}='{}'".format("services", "serviceid", self.category_code)
                wr.execute(lk_c)
                valu = wr.fetchall()
                c.close()
                code = valu[0][0]

                def updates(field, new_value):
                    conn = connect(path_to_database)
                    writes = conn.cursor()
                    lk_comm = "UPDATE {} SET {}='{}' WHERE serviceid='{}'".format("services", field, new_value, code)
                    writes.execute(lk_comm)
                    conn.commit()
                    conn.close()

                if service_code == "" or len(service_code) < 3:
                    messagebox.showerror("Service code error", "{} contains errors".format(service_code))

                elif description == "" or len(description) < 3:
                    messagebox.showerror("Description error", "{} contains errors".format(description))

                elif price < 1 or price > 10000000:
                    messagebox.showerror("Price error", "{} contains errors".format(price))

                else:
                    updates("servicecode", service_code)
                    updates("description", description)
                    updates("price", price)
                    cancel_function()

            except IndexError:
                pass

            except TclError:
                pass

        update_button = Button(services_info_frame, bg='#007bdf', fg='white', command=update_service_function)
        update_button.configure(text="UPDATE", font=(font, self.font_adjust(13)), relief='solid',
                                width=self.widget_width(12))
        update_button.place(x=self.widget_width(310), y=self.widget_height(410), height=self.widget_height(45))

        def delete_service_function():
            item = services_treeview.focus()
            items = services_treeview.item(item)['values']

            try:
                conn = connect(path_to_database)
                writes = conn.cursor()
                lk_comm = "DELETE FROM {} WHERE serviceid='{}'".format("services", items[0])
                writes.execute(lk_comm)
                conn.commit()
                conn.close()

                updating_treeview_data()
                cancel_function()

            except IndexError:
                pass

        delete_button = Button(services_info_frame, bg='#d94141', fg='white', command=delete_service_function)
        delete_button.configure(text="DELETE", font=(font, self.font_adjust(13)), relief='solid',
                                width=self.widget_width(12))
        delete_button.place(x=self.widget_width(170), y=self.widget_height(460), height=self.widget_height(45))

        def cancel_function():
            service_code_entry.configure(state='normal')
            service_code_entry.delete(0, END)
            service_code_entry.configure(highlightbackground="black", highlightthickness=0)
            service_code_entry.configure(state='disabled')

            description_entry.configure(state='normal')
            description_entry.delete(0, END)
            description_entry.configure(highlightbackground="black", highlightthickness=0)
            description_entry.configure(state='disabled')

            price_entry.configure(state='normal')
            price_entry.delete(0, END)
            price_entry.configure(highlightbackground="black", highlightthickness=0)
            price_entry.configure(state='disabled')

            save_button.configure(state='disabled')
            updating_treeview_data()

        cancel_button = Button(services_info_frame, bg='#007bdf', fg='white', command=cancel_function)
        cancel_button.configure(text="CANCEL", font=(font, self.font_adjust(13)), relief='solid',
                                width=self.widget_width(12))
        cancel_button.place(x=self.widget_width(310), y=self.widget_height(460), height=self.widget_height(45))

        def updating_values(*args):
            item = services_treeview.focus()
            items = services_treeview.item(item)['values']

            def collect_values(field, value):
                connection = connect(path_to_database)
                write = connection.cursor()
                lk_command = "SELECT * FROM {} WHERE {}='{}'".format("services", field, value)
                write.execute(lk_command)
                values = write.fetchall()
                connection.close()

                return values

            try:
                vals = collect_values("description", items[2])
                service_code_entry.configure(state='normal')
                service_code_entry.delete(0, END)
                service_code_entry.insert(0, vals[0][1])

                description_entry.configure(state='normal')
                description_entry.delete(0, END)
                description_entry.insert(0, vals[0][2])

                price_entry.configure(state='normal')
                price_entry.delete(0, END)
                price_entry.insert(0, vals[0][3])
                self.category_code = vals[0][0]

            except IndexError:
                pass

        services_treeview.bind("<Double-1>", updating_values)

    def stock_frame_window(self):
        search_entry_value = StringVar()
        add_quantity_value = IntVar()
        date_value = StringVar()

        def filter_function(*args):
            items_on_treeview = products_treeview.get_children()
            search = search_entry_value.get().lower()

            for each_itme in items_on_treeview:
                if search in products_treeview.item(each_itme)['values'][1].lower():
                    search_var = products_treeview.item(each_itme)['values']
                    products_treeview.delete(each_itme)

                    products_treeview.insert("", 0, values=search_var)

        products_style = Style()
        products_style.theme_use('clam')

        stocks_frame = Frame(self.window_initializer, bg='white')
        stocks_frame.configure(width=self.screen_width - self.widget_width(241), height=self.widget_height(710))
        stocks_frame.place(x=self.widget_width(241), y=self.widget_height(90))

        advanced_search_frame = Frame(stocks_frame)
        advanced_search_frame.configure(bg="white", width=self.screen_width - self.widget_width(320),
                                        height=self.widget_height(120))
        advanced_search_frame.configure(highlightbackground="#c2c2c0", highlightthickness=2)
        advanced_search_frame.place(x=self.widget_width(40), y=self.widget_height(34))

        advanced_search_label = Label(stocks_frame)
        advanced_search_label.configure(text="STOCK INFORMATION", fg='#007bdf')
        advanced_search_label.configure(font=(font, self.font_adjust(13), 'bold'), bg='white')
        advanced_search_label.place(x=self.widget_width(80), y=self.widget_height(20))

        product_qua_treeview_columns = ['c1', 'c2', 'c3']
        products_treeview = Treeview(stocks_frame, show='headings', columns=product_qua_treeview_columns)

        products_treeview.heading("# 1", text='ID', anchor='w')
        products_treeview.column("# 1", stretch=NO, minwidth=self.widget_width(50), width=self.widget_width(50))
        products_treeview.heading("# 2", text='Description', anchor='w')
        products_treeview.column("# 2", stretch=NO, minwidth=self.widget_width(340), width=self.widget_width(340))
        products_treeview.heading("# 3", text='Quantity', anchor='center')
        products_treeview.column("# 3", stretch=NO, minwidth=self.widget_width(100), width=self.widget_width(100),
                                 anchor='center')

        products_style.configure('Treeview.Heading', background="#3e3f3f", foreground='white',
                                 font=(font, self.font_adjust(11), 'bold'))
        products_style.configure('Treeview.Heading', relief='none')
        products_style.configure('Treeview', font=(font, self.font_adjust(11)))

        products_treeview.place(x=self.widget_width(40), y=self.widget_height(160), height=self.widget_height(470))

        search_label = Label(advanced_search_frame)
        search_label.configure(text="Search", font=(font, self.font_adjust(12), 'bold'), bg='white')
        search_label.place(x=self.widget_width(40), y=self.widget_height(23))

        search_entry = Entry(advanced_search_frame, textvariable=search_entry_value)
        search_entry.configure(width=self.widget_width(33), relief='solid', font=(font, self.font_adjust(13)))
        search_entry.place(x=self.widget_width(180), y=self.widget_height(25))
        search_entry_value.trace("w", filter_function)

        add_quantity_label = Label(advanced_search_frame)
        add_quantity_label.configure(text="Add Quantity:", font=(font, self.font_adjust(12), 'bold'), bg='white')
        add_quantity_label.place(x=self.widget_width(40), y=self.widget_height(68))

        add_quantity_entry = Entry(advanced_search_frame, textvariable=add_quantity_value)
        add_quantity_entry.configure(width=self.widget_width(33), relief='solid', font=(font, self.font_adjust(13)))
        add_quantity_entry.place(x=self.widget_width(180), y=self.widget_height(70))

        product_code_label = Label(advanced_search_frame)
        product_code_label.configure(text="Product Code:", font=(font, self.font_adjust(12), 'bold'), bg='white')
        product_code_label.place(x=self.widget_width(560), y=self.widget_height(23))

        product_code_entry = Entry(advanced_search_frame, state='disabled')
        product_code_entry.configure(width=self.widget_width(13), relief='solid', font=(font, self.font_adjust(13)))
        product_code_entry.place(x=self.widget_width(700), y=self.widget_height(23))

        description_label = Label(advanced_search_frame)
        description_label.configure(text="Description:", font=(font, self.font_adjust(12), 'bold'), bg='white')
        description_label.place(x=self.widget_width(560), y=self.widget_height(68))

        description_entry = Entry(advanced_search_frame, state='disabled')
        description_entry.configure(width=self.widget_width(53), relief='solid', font=(font, self.font_adjust(13)))
        description_entry.place(x=self.widget_width(680), y=self.widget_height(70))

        today = datetime.datetime.today()
        current_time = today.strftime("%d/%B/%Y %H:%M")

        stock_in_label = Entry(advanced_search_frame)
        stock_in_label.configure(textvariable=date_value, state='normal', font=(font, self.font_adjust(12)),
                                 relief="solid")
        stock_in_label.place(x=self.widget_width(975), y=self.widget_height(28))
        stock_in_label.insert(0, str(current_time))
        stock_in_label.configure(state='disabled')

        def updating_products_data():
            try:
                db_co = connect(path_to_database)
                wri = db_co.cursor()
                ll = "SELECT * FROM {}".format("stock")
                wri.execute(ll)
                r = wri.fetchall()
                db_co.close()

                for items in products_treeview.get_children():
                    products_treeview.delete(items)

                for X in range(0, len(r)):
                    products_treeview.insert("", 'end', text="1", values=(r[X][0], r[X][2], r[X][3]))

            except IndexError:
                pass

        updating_products_data()

        selection_qua_treeview_columns = ['c1', 'c2', 'c3', 'c4', 'c5']
        selections_treeview = Treeview(stocks_frame, show='headings', columns=selection_qua_treeview_columns)

        selections_treeview.heading("# 1", text='ID', anchor='w')
        selections_treeview.column("# 1", stretch=NO, minwidth=self.widget_width(40), width=self.widget_width(40))
        selections_treeview.heading("# 2", text='Code', anchor='w')
        selections_treeview.column("# 2", stretch=NO, minwidth=self.widget_width(105), width=self.widget_width(105))
        selections_treeview.heading("# 3", text='Description', anchor='w')
        selections_treeview.column("# 3", stretch=NO, minwidth=self.widget_width(230), width=self.widget_width(230))
        selections_treeview.heading("# 4", text='Quantity', anchor='w')
        selections_treeview.column("# 4", stretch=NO, minwidth=self.widget_width(120), width=self.widget_width(120))
        selections_treeview.heading("# 5", text='Stock in Date', anchor='w')
        selections_treeview.column("# 5", stretch=NO, minwidth=self.widget_width(220), width=self.widget_width(220))

        products_style.configure('Treeview.Heading', background="#3e3f3f", foreground='white',
                                 font=(font, self.font_adjust(11), 'bold'))
        products_style.configure('Treeview.Heading', relief='none')
        products_style.configure('Treeview', font=(font, self.font_adjust(11)))

        selections_treeview.place(x=self.widget_width(600), y=self.widget_height(160), height=self.widget_height(470))

        count_product_in_selection = []

        def cancel_function():
            add_quantity_entry.configure(state='normal')
            add_quantity_entry.delete(0, END)
            add_quantity_entry.configure(highlightbackground="black", highlightthickness=0)

            product_code_entry.configure(state='normal')
            product_code_entry.delete(0, END)
            product_code_entry.configure(state='disabled')

            description_entry.configure(state='normal')
            description_entry.delete(0, END)
            description_entry.configure(state='disabled')

            save_button.configure(state='disabled')
            create_button.configure(state='disabled')

            for items in selections_treeview.get_children():
                selections_treeview.delete(items)

            updating_products_data()
            count_product_in_selection.clear()

        cancel_button = Button(stocks_frame, bg='#007bdf', fg='white', command=cancel_function)
        cancel_button.configure(text="CANCEL", font=(font, self.font_adjust(13)), relief='solid',
                                width=self.widget_width(10))
        cancel_button.place(x=self.widget_width(180), y=self.widget_height(650), height=self.widget_height(45))

        def save_function():
            for items in selections_treeview.get_children():
                row_values = selections_treeview.item(items)['values']

                def collect_values(field, value):
                    con = connect(path_to_database)
                    wri = con.cursor()
                    lk_com = "SELECT * FROM {} WHERE {}='{}'".format("stock", field, value)
                    wri.execute(lk_com)
                    va = wri.fetchall()
                    con.close()

                    return va

                previous_quantity = collect_values("stockid", row_values[0])[0][3]
                new_quantity = row_values[3] + previous_quantity

                conn = connect(path_to_database)
                writes = conn.cursor()
                lk_comm = "UPDATE {} SET {}='{}' WHERE stockid='{}'".format("stock", "quantity", new_quantity,
                                                                            row_values[0])
                writes.execute(lk_comm)
                conn.commit()
                conn.close()
            cancel_function()

        save_button = Button(stocks_frame, bg='#007bdf', fg='white', state='disabled', command=save_function)
        save_button.configure(text="SAVE", font=(font, self.font_adjust(13)), relief='solid',
                              width=self.widget_width(10))
        save_button.place(x=self.widget_width(940), y=self.widget_height(650), height=self.widget_height(45))

        def create_function():
            try:
                quantity = add_quantity_value.get()
                stock_date = date_value.get().strip()

                if stock_date == "":
                    messagebox.showerror("Date Error", "Please select stock in date!")

                elif quantity < 1:
                    add_quantity_entry.configure(highlightbackground="red", highlightthickness=2)
                    messagebox.showerror("Quantity Error", "Quantity value should not be 0")

                else:
                    item = products_treeview.focus()
                    items = products_treeview.item(item)['values']

                    def collect_values(field, value):
                        connection = connect(path_to_database)
                        write = connection.cursor()
                        lk_command = "SELECT * FROM {} WHERE {}='{}'".format("stock", field, value)
                        write.execute(lk_command)
                        values = write.fetchall()
                        connection.close()

                        return values

                    r = collect_values("stockid", items[0])

                    if r[0][0] in count_product_in_selection:
                        messagebox.showwarning("Duplicate", "The stock {} already in field".format(items[3]))

                    else:
                        selections_treeview.insert("", 'end', text="1",
                                                   values=(r[0][0], r[0][1], r[0][2], quantity, stock_date))

                        add_quantity_entry.configure(state='normal')
                        add_quantity_entry.delete(0, END)
                        add_quantity_entry.configure(highlightbackground="black", highlightthickness=0)

                        product_code_entry.configure(state='normal')
                        product_code_entry.delete(0, END)
                        product_code_entry.configure(state='disabled')

                        description_entry.configure(state='normal')
                        description_entry.delete(0, END)
                        description_entry.configure(state='disabled')

                        save_button.configure(state='normal')
                        count_product_in_selection.append(r[0][0])

            except IndexError:
                pass

            except TclError:
                add_quantity_entry.configure(highlightbackground="red", highlightthickness=2)
                messagebox.showerror("Quantity Error", "Quantity should be numbers only!")

        create_button = Button(stocks_frame, bg='#f0bc00', fg='white', command=create_function)
        create_button.configure(text="ADD STOCK", font=(font, self.font_adjust(13)), relief='solid',
                                width=self.widget_width(10), state='disabled')
        create_button.place(x=self.widget_width(40), y=self.widget_height(650), height=self.widget_height(45))

        def update_function():
            try:
                item = selections_treeview.focus()
                items = selections_treeview.item(item)['values']

                add_quantity_entry.delete(0, END)
                add_quantity_entry.insert(0, items[3])

                stock_in_label.delete(0, END)

                product_code_entry.configure(state='normal')
                product_code_entry.delete(0, END)
                product_code_entry.insert(0, items[1])
                product_code_entry.configure(state='disabled')

                description_entry.configure(state='normal')
                description_entry.delete(0, END)
                description_entry.insert(0, items[2])
                description_entry.configure(state='disabled')

                selections_treeview.delete(item)
                count_product_in_selection.remove(items[0])
                create_button.configure(state='normal')
                save_button.configure(state='disabled')

            except IndexError:
                pass

        update_button = Button(stocks_frame, bg='#007bdf', fg='white', command=update_function)
        update_button.configure(text="UPDATE", font=(font, self.font_adjust(13)), relief='solid',
                                width=self.widget_width(10))
        update_button.place(x=self.widget_width(1070), y=self.widget_height(650), height=self.widget_height(45))

        def delete_function():
            try:
                selected_item = selections_treeview.selection()[0]
                selections_treeview.delete(selected_item)

            except IndexError:
                pass

        delete_button = Button(stocks_frame, bg='#d94141', fg='white', command=delete_function)
        delete_button.configure(text="DELETE", font=(font, self.font_adjust(13)), relief='solid',
                                width=self.widget_width(10))
        delete_button.place(x=self.widget_width(1200), y=self.widget_height(650), height=self.widget_height(45))

        def updating_values(*args):
            item = products_treeview.focus()
            items = products_treeview.item(item)['values']

            def collect_values(field, value):
                connection = connect(path_to_database)
                write = connection.cursor()
                lk_command = "SELECT * FROM {} WHERE {}='{}'".format("stock", field, value)
                write.execute(lk_command)
                values = write.fetchall()
                connection.close()

                return values

            try:
                vals = collect_values("stockid", items[0])

                product_code_entry.configure(state='normal')
                product_code_entry.delete(0, END)
                product_code_entry.insert(0, vals[0][1])
                product_code_entry.configure(state='disabled')

                description_entry.configure(state='normal')
                description_entry.delete(0, END)
                description_entry.insert(0, vals[0][2])
                description_entry.configure(state='disabled')

                create_button.configure(state='normal')

                self.category_code = vals[0][0]

            except IndexError:
                pass

        products_treeview.bind("<Double-1>", updating_values)

    def dashboard_frame_window(self):
        dashboard_frame = Frame(self.window_initializer, bg='white')
        dashboard_frame.configure(width=self.screen_width - self.widget_width(241), height=self.widget_height(710))
        dashboard_frame.place(x=self.widget_width(241), y=self.widget_height(90))

        # ================================== Sales ========================================================
        def collect_sales():
            connection = connect(path_to_database)
            write = connection.cursor()
            lk_command = "SELECT SubTotal FROM Sales"
            write.execute(lk_command)
            values = write.fetchall()
            connection.close()

            total = []

            for totals in values:
                total.append(totals[0])

            return sum(total)

        total_sales_frame = Frame(dashboard_frame)
        total_sales_frame.configure(bg="#9e3a3a")
        total_sales_frame.place(x=self.widget_width(30), y=self.widget_height(50), width=self.widget_width(300),
                                height=self.widget_height(125))

        total_sales_count = Label(total_sales_frame)
        total_sales_count.configure(text=collect_sales(), bg="#9e3a3a", fg="white",
                                    font=(font, self.font_adjust(30), "bold"))
        total_sales_count.place(x=self.widget_width(100), y=self.widget_height(20))

        total_sales_label = Label(total_sales_frame)
        total_sales_label.configure(text="Total Sales", bg="#9e3a3a", fg="white", font=(font, self.font_adjust(12)))
        total_sales_label.place(x=self.widget_width(100), y=self.widget_height(80))

        total_sales_image = Image.open(path_to_icons + 'growth.png').resize(
            (self.widget_width(70), self.widget_height(80)))
        sales_photo = ImageTk.PhotoImage(total_sales_image)
        total_sales_image_label = Label(total_sales_frame, image=sales_photo, bg='#9e3a3a')
        total_sales_image_label.image = sales_photo
        total_sales_image_label.place(x=self.widget_width(10), y=self.widget_height(20))

        # =================================== Items ====================================================
        def collect_items():
            connection = connect(path_to_database)
            write = connection.cursor()
            lk_command = "SELECT * FROM products"
            write.execute(lk_command)
            values = write.fetchall()
            connection.close()

            return len(values)

        total_items_frame = Frame(dashboard_frame)
        total_items_frame.configure(bg="#11a75c")
        total_items_frame.place(x=self.widget_width(355), y=self.widget_height(50), width=self.widget_width(300),
                                height=self.widget_height(125))

        total_items_count = Label(total_items_frame)
        total_items_count.configure(text=collect_items(), bg="#11a75c", fg="white",
                                    font=(font, self.font_adjust(30), "bold"))
        total_items_count.place(x=self.widget_width(130), y=self.widget_height(20))

        total_items_label = Label(total_items_frame)
        total_items_label.configure(text="Total Items", bg="#11a75c", fg="white", font=(font, self.font_adjust(12)))
        total_items_label.place(x=self.widget_width(130), y=self.widget_height(80))

        total_items_image = Image.open(path_to_icons + 'trolley.png').resize(
            (self.widget_width(80), self.widget_height(80)))
        items_photo = ImageTk.PhotoImage(total_items_image)
        total_items_image_label = Label(total_items_frame, image=items_photo, bg='#11a75c')
        total_items_image_label.image = items_photo
        total_items_image_label.place(x=self.widget_width(30), y=self.widget_height(20))

        # ============================================== Critical =====================================
        def critical_items():
            return 0

        critical_items_frame = Frame(dashboard_frame)
        critical_items_frame.configure(bg="#f45a38")
        critical_items_frame.place(x=self.widget_width(680), y=self.widget_height(50), width=self.widget_width(300),
                                   height=self.widget_height(125))

        critical_items_count = Label(critical_items_frame)
        critical_items_count.configure(text=critical_items(), bg="#f45a38", fg="white",
                                       font=(font, self.font_adjust(30), "bold"))
        critical_items_count.place(x=self.widget_width(130), y=self.widget_height(20))

        critical_items_label = Label(critical_items_frame)
        critical_items_label.configure(text="Critical Items", bg="#f45a38", fg="white",
                                       font=(font, self.font_adjust(12)))
        critical_items_label.place(x=self.widget_width(130), y=self.widget_height(80))

        critical_items_image = Image.open(path_to_icons + 'danger.png').resize(
            (self.widget_width(80), self.widget_height(80)))
        critical_photo = ImageTk.PhotoImage(critical_items_image)
        critical_items_image_label = Label(critical_items_frame, image=critical_photo, bg='#f45a38')
        critical_items_image_label.image = critical_photo
        critical_items_image_label.place(x=self.widget_width(30), y=self.widget_height(20))

        # =============================================== Sold =========================================
        def sold_items():
            connection = connect(path_to_database)
            write = connection.cursor()
            lk_command = "SELECT * FROM Sales"
            write.execute(lk_command)
            values = write.fetchall()
            connection.close()

            return len(values)

        sold_items_frame = Frame(dashboard_frame)
        sold_items_frame.configure(bg="#fb9c08")
        sold_items_frame.place(x=self.widget_width(1000), y=self.widget_height(50), width=self.widget_width(300),
                               height=self.widget_height(125))

        sold_items_count = Label(sold_items_frame)
        sold_items_count.configure(text=sold_items(), bg="#fb9c08", fg="white",
                                   font=(font, self.font_adjust(30), "bold"))
        sold_items_count.place(x=self.widget_width(130), y=self.widget_height(20))

        sold_items_label = Label(sold_items_frame)
        sold_items_label.configure(text="Sold Items", bg="#fb9c08", fg="white", font=(font, self.font_adjust(12)))
        sold_items_label.place(x=self.widget_width(130), y=self.widget_height(80))

        sold_items_image = Image.open(path_to_icons + 'sold.png').resize(
            (self.widget_width(80), self.widget_height(80)))
        sold_photo = ImageTk.PhotoImage(sold_items_image)
        sold_items_image_label = Label(sold_items_frame, image=sold_photo, bg='#fb9c08')
        sold_items_image_label.image = sold_photo
        sold_items_image_label.place(x=self.widget_width(30), y=self.widget_height(20))


class CashierPage:
    def __init__(self, cashier_init):
        self.count = 0
        self.new_transaction_number = None
        self.total_pay = 0
        self.window_initializer = cashier_init
        new_quantity = IntVar()

        def widget_width(expected_value):
            monitor_width = monitor[0].width_mm
            window_width = self.window_initializer.winfo_screenwidth()
            resolution = window_width + (monitor_width / 25.4)
            optimal_resolution = 1600 + (309 / 25.4)
            new_value = (resolution * expected_value) / optimal_resolution

            return int(round(new_value, 0))

        def widget_height(expected_value):
            monitor_height = monitor[0].height_mm
            window_height = self.window_initializer.winfo_screenheight()
            resolution = window_height + (monitor_height / 25.4)
            optimal_resolution = 900 + (174 / 25.4)
            new_value = (resolution * expected_value) / optimal_resolution

            return int(round(new_value, 0))

        def font_adjust(expected_value):
            text_width = widget_width(expected_value=expected_value)
            text_height = widget_height(expected_value=expected_value)

            optimal_font = (text_width + text_height) / 2

            return int(round(optimal_font))

        x = self.window_initializer.winfo_screenwidth()
        y = self.window_initializer.winfo_screenheight()
        self.window_initializer.geometry('{}x{}'.format(x, y))
        self.window_initializer.title("CASHIER ACCOUNT")
        self.window_initializer.state('zoomed')
        self.window_initializer.resizable(0, 1)

        self.cashier_waste_frame = Frame(self.window_initializer)
        self.cashier_waste_frame.configure(width=widget_width(380), height=widget_height(230),
                                           highlightbackground="black", highlightthickness=3)
        self.cashier_waste_frame.place(x=widget_width(50), y=widget_height(80))

        self.cashier_waste_label = Label(self.cashier_waste_frame)
        self.cashier_waste_label.configure(font=(font, font_adjust(11), "bold"), text="Select Stock:")
        self.cashier_waste_label.place(x=widget_width(5), y=widget_height(20))
        stock_waste_var = StringVar()

        def get_stock_information():
            db_connection = connect(path_to_database)
            writer = db_connection.cursor()
            lookup_command = "SELECT * FROM {}".format("stock")
            writer.execute(lookup_command)
            result = writer.fetchall()
            db_connection.close()

            stock_info = []

            for stocks in result:
                stock_info.append(str(stocks[2]))

            return stock_info

        self.cashier_waste_entry = Combobox(self.cashier_waste_frame)
        self.cashier_waste_entry['values'] = get_stock_information()
        self.cashier_waste_entry.configure(font=(font, font_adjust(9)), state='readonly', textvariable=stock_waste_var)
        self.cashier_waste_entry.place(x=widget_width(150), y=widget_height(23))

        self.cashier_waste_quan_label = Label(self.cashier_waste_frame)
        self.cashier_waste_quan_label.configure(font=(font, font_adjust(11), "bold"), text="Stock Quantity:")
        self.cashier_waste_quan_label.place(x=widget_width(5), y=widget_height(60))

        self.cashier_waste_quan_entry = Entry(self.cashier_waste_frame)
        self.cashier_waste_quan_entry.configure(font=(font, font_adjust(11)), justify=CENTER, state='disabled')
        self.cashier_waste_quan_entry.place(x=widget_width(150), y=widget_height(60))

        self.cashier_waste_amnt_label = Label(self.cashier_waste_frame)
        self.cashier_waste_amnt_label.configure(font=(font, font_adjust(11), "bold"), text="Waste Amount:")
        self.cashier_waste_amnt_label.place(x=widget_width(5), y=widget_height(100))

        waste_amnt = IntVar()
        self.cashier_waste_amnt_entry = Entry(self.cashier_waste_frame, textvariable=waste_amnt)
        self.cashier_waste_amnt_entry.configure(font=(font, font_adjust(11)), justify=CENTER)
        self.cashier_waste_amnt_entry.place(x=widget_width(150), y=widget_height(100))
        self.cashier_waste_amnt_entry.delete(0, END)

        self.waste_label = Label(self.window_initializer)
        self.waste_label.configure(text="Waste", font=(font, font_adjust(11), "bold"))
        self.waste_label.place(x=widget_width(100), y=widget_height(65))

        def load_stock_waste(*args):
            stock_waste_name = stock_waste_var.get()

            db_connection = connect(path_to_database)
            writer = db_connection.cursor()
            lookup_command = "SELECT * FROM {} WHERE description='{}'".format("stock", stock_waste_name)
            writer.execute(lookup_command)
            result = writer.fetchall()
            db_connection.close()

            current_stock_amount = result[0][3]
            self.cashier_waste_quan_entry.configure(state='normal')
            self.cashier_waste_quan_entry.delete(0, END)
            self.cashier_waste_quan_entry.insert(0, str(current_stock_amount))
            self.cashier_waste_quan_entry.configure(state='disabled')

        stock_waste_var.trace("w", load_stock_waste)

        def waste_cancel():
            self.cashier_waste_quan_entry.configure(state='normal')
            self.cashier_waste_quan_entry.delete(0, END)
            self.cashier_waste_quan_entry.configure(state='disabled')

            self.cashier_waste_amnt_entry.delete(0, END)

        def update_waste():
            try:
                stock_name = stock_waste_var.get()
                db_connection = connect(path_to_database)
                writer = db_connection.cursor()
                lookup_command = "SELECT quantity FROM {} WHERE description='{}'".format("stock", stock_name)
                writer.execute(lookup_command)
                result = writer.fetchall()
                db_connection.close()

                wasted_amount = waste_amnt.get()
                current_stock = result[0][0]
                print(wasted_amount, current_stock)

                if int(current_stock) > wasted_amount:
                    today = datetime.datetime.today()
                    current_time = today.strftime("%d/%B/%Y %H:%M")
                    new_amount = int(current_stock) - int(wasted_amount)

                    conn = connect(path_to_database)
                    writes = conn.cursor()
                    lk_comm = "UPDATE stock SET quantity='{}' WHERE description='{}'".format(new_amount, stock_name)
                    lk_comm2 = "UPDATE stock SET stockindate='{}' WHERE description='{}'".format(current_time,
                                                                                                 stock_name)
                    writes.execute(lk_comm)
                    writes.execute(lk_comm2)
                    conn.commit()
                    conn.close()
                    waste_cancel()

                else:
                    messagebox.showwarning("Waste Error", "Waste quantity should less than stock quantity!")
                    waste_cancel()

            except TclError:
                messagebox.showwarning("Waste Error", "Waste quantity should be a number")
                waste_cancel()

        self.cashier_update_waste = Button(self.cashier_waste_frame, bg='light green')
        self.cashier_update_waste.configure(text="UPDATE", font=(font, font_adjust(13)), relief='solid')
        self.cashier_update_waste.configure(command=update_waste)
        self.cashier_update_waste.place(x=widget_width(130), y=widget_height(160))

        self.cashier_cancel_waste = Button(self.cashier_waste_frame, bg='light yellow')
        self.cashier_cancel_waste.configure(text="CANCEL", font=(font, font_adjust(13)), relief='solid')
        self.cashier_cancel_waste.configure(command=waste_cancel)
        self.cashier_cancel_waste.place(x=widget_width(250), y=widget_height(160))

        self.cashier_update_frame = Frame(self.window_initializer)
        self.cashier_update_frame.configure(width=widget_width(369), height=widget_height(230),
                                            highlightbackground="black", highlightthickness=3)
        self.cashier_update_frame.place(x=widget_width(880), y=widget_height(80))

        self.cashier_update_product_code_label = Label(self.cashier_update_frame)
        self.cashier_update_product_code_label.configure(font=(font, font_adjust(11), "bold"), text="Product Code:")
        self.cashier_update_product_code_label.place(x=widget_width(5), y=widget_height(20))

        self.cashier_update_product_code = Entry(self.cashier_update_frame)
        self.cashier_update_product_code.configure(state='disabled', font=(font, font_adjust(11), "bold"),
                                                   relief="solid")
        self.cashier_update_product_code.place(x=widget_width(133), y=widget_height(20))

        self.cashier_update_product_desc_label = Label(self.cashier_update_frame)
        self.cashier_update_product_desc_label.configure(font=(font, font_adjust(11), "bold"), text="Product Desc:")
        self.cashier_update_product_desc_label.place(x=widget_width(5), y=widget_height(60))

        self.cashier_update_product_desc = Entry(self.cashier_update_frame)
        self.cashier_update_product_desc.configure(state='disabled', font=(font, font_adjust(11), "bold"),
                                                   relief="solid")
        self.cashier_update_product_desc.place(x=widget_width(133), y=widget_height(60))

        self.cashier_update_product_quan_label = Label(self.cashier_update_frame)
        self.cashier_update_product_quan_label.configure(font=(font, font_adjust(11), "bold"), text="Quantity:")
        self.cashier_update_product_quan_label.place(x=widget_width(40), y=widget_height(100))

        self.cashier_update_product_quan = Entry(self.cashier_update_frame, textvariable=new_quantity)
        self.cashier_update_product_quan.configure(font=(font, font_adjust(11), "bold"), relief="solid", justify=CENTER,
                                                   state="disabled")
        self.cashier_update_product_quan.place(x=widget_width(133), y=widget_height(100))

        def change_quantity_cancel():
            self.cashier_update_product_code.configure(state='normal')
            self.cashier_update_product_code.delete(0, END)
            self.cashier_update_product_code.configure(state='disabled')

            self.cashier_update_product_desc.configure(state='normal')
            self.cashier_update_product_desc.delete(0, END)
            self.cashier_update_product_desc.configure(state='disabled')

            self.cashier_update_product_quan.configure(state='normal')
            self.cashier_update_product_quan.delete(0, END)
            self.cashier_update_product_quan.configure(state='disabled')

            self.cashier_cancel_button.configure(state='disabled')
            self.cashier_update_button.configure(state='disabled')

        def update_quantity():
            item = self.cart_table.focus()
            items = self.cart_table.item(item)['values']
            quantity = new_quantity.get()

            if quantity < 1:
                change_quantity_cancel()
                messagebox.showwarning("Quantity Error", "New Quantity must be greater than 0!")

            else:
                self.delete_cart_item()
                new_total = int(quantity) * float(items[2])
                self.cart_table.insert("", 'end', text="1", values=(items[0], items[1], items[2], quantity, new_total))
                self.total_pay = self.total_pay + new_total
                self.payment_label.configure(text=self.total_pay)
                change_quantity_cancel()

        self.cashier_update_button = Button(self.cashier_update_frame, bg='light green')
        self.cashier_update_button.configure(state='disabled', text="UPDATE", font=(font, font_adjust(13)),
                                             relief='solid')
        self.cashier_update_button.configure(command=update_quantity)
        self.cashier_update_button.place(x=widget_width(240), y=widget_height(160))

        self.cashier_cancel_button = Button(self.cashier_update_frame, bg='light yellow')
        self.cashier_cancel_button.configure(state='disabled', text="CANCEL", font=(font, font_adjust(13)),
                                             relief='solid')
        self.cashier_cancel_button.configure(command=change_quantity_cancel)
        self.cashier_cancel_button.place(x=widget_width(100), y=widget_height(160))

        self.change_quantity_label = Label(self.window_initializer)
        self.change_quantity_label.configure(text="Change Quantity", font=(font, font_adjust(11), "bold"))
        self.change_quantity_label.place(x=widget_width(930), y=widget_height(65))

        self.cashier_stock_frame = Frame(self.window_initializer)
        self.cashier_stock_frame.configure(width=widget_width(369), height=widget_height(230),
                                           highlightbackground="black", highlightthickness=3)
        self.cashier_stock_frame.place(x=widget_width(480), y=widget_height(80))

        self.cashier_stock_product_code_label = Label(self.cashier_stock_frame)
        self.cashier_stock_product_code_label.configure(font=(font, font_adjust(11), "bold"), text="Product Code:")
        self.cashier_stock_product_code_label.place(x=widget_width(5), y=widget_height(20))

        self.cashier_stock_product_code = Entry(self.cashier_stock_frame)
        self.cashier_stock_product_code.configure(state='disabled', font=(font, font_adjust(11), "bold"),
                                                  relief="solid")
        self.cashier_stock_product_code.place(x=widget_width(133), y=widget_height(20))

        self.cashier_stock_product_desc_label = Label(self.cashier_stock_frame)
        self.cashier_stock_product_desc_label.configure(font=(font, font_adjust(11), "bold"), text="Product Desc:")
        self.cashier_stock_product_desc_label.place(x=widget_width(5), y=widget_height(60))

        self.cashier_stock_product_desc = Entry(self.cashier_stock_frame)
        self.cashier_stock_product_desc.configure(state='disabled', font=(font, font_adjust(11), "bold"),
                                                  relief="solid")
        self.cashier_stock_product_desc.place(x=widget_width(133), y=widget_height(60))

        self.cashier_stock_product_quan_label = Label(self.cashier_stock_frame)
        self.cashier_stock_product_quan_label.configure(font=(font, font_adjust(11), "bold"), text="Current Stock:")
        self.cashier_stock_product_quan_label.place(x=widget_width(5), y=widget_height(100))

        self.cashier_stock_product_quan = Entry(self.cashier_stock_frame)
        self.cashier_stock_product_quan.configure(font=(font, font_adjust(11), "bold"), relief="solid", justify=CENTER,
                                                  state="disabled")
        self.cashier_stock_product_quan.place(x=widget_width(133), y=widget_height(100))

        self.cashier_stock_product_new_label = Label(self.cashier_stock_frame)
        self.cashier_stock_product_new_label.configure(font=(font, font_adjust(11), "bold"), text="New Stock:")
        self.cashier_stock_product_new_label.place(x=widget_width(28), y=widget_height(140))

        cashier_new_stock = IntVar()

        self.cashier_stock_product_new = Entry(self.cashier_stock_frame, textvariable=cashier_new_stock)
        self.cashier_stock_product_new.configure(font=(font, font_adjust(11), "bold"), relief="solid", justify=CENTER,
                                                 state="disabled")
        self.cashier_stock_product_new.place(x=widget_width(133), y=widget_height(140))

        def change_stock_cancel():
            self.cashier_stock_product_code.configure(state='normal')
            self.cashier_stock_product_code.delete(0, END)
            self.cashier_stock_product_code.configure(state='disabled')

            self.cashier_stock_product_desc.configure(state='normal')
            self.cashier_stock_product_desc.delete(0, END)
            self.cashier_stock_product_desc.configure(state='disabled')

            self.cashier_stock_product_quan.configure(state='normal')
            self.cashier_stock_product_quan.delete(0, END)
            self.cashier_stock_product_quan.configure(state='disabled')

            self.cashier_stock_product_new.configure(state='normal')
            self.cashier_stock_product_new.delete(0, END)
            self.cashier_stock_product_new.configure(state='disabled')

            self.cashier_cancel_stock.configure(state='disabled')
            self.cashier_stock_button.configure(state='disabled')

        def update_stock():
            try:
                item = self.cart_table.focus()
                items = self.cart_table.item(item)['values']
                stock = cashier_new_stock.get()
                stock_name = ""
                current_stock = 0

                if stock < 1:
                    change_stock_cancel()
                    messagebox.showwarning("Quantity Error", "New Quantity must be greater than 0!")

                else:
                    def collect_stock(desc):
                        db_co = connect(path_to_database)
                        wri = db_co.cursor()
                        ll = "SELECT * FROM {} WHERE description='{}'".format("stock", desc)
                        wri.execute(ll)
                        r = wri.fetchall()
                        db_co.close()

                        return r

                    db_co = connect(path_to_database)
                    wri = db_co.cursor()
                    ll = "SELECT category FROM {} WHERE productcode='{}'".format("products", items[0])
                    wri.execute(ll)
                    r = wri.fetchall()
                    db_co.close()

                    if r[0][0] == "Printing":
                        if items[1] == "A4 Printing B/W" or items[1] == "A4 Printing Coloured" or \
                                items[1] == "A4 Copy B/W" or items[1] == "A4 Copy Coloured":
                            stock_name = "A4 Rim Papers"
                            current_stock = collect_stock("A4 Rim Papers")

                        if items[1] == "A4 Glossy Paper Printing":
                            stock_name = "Glossy Paper"
                            current_stock = collect_stock("Glossy Paper")

                        if items[1] == "A4 150 gsm":
                            stock_name = "A4 Art Paper 150 gsm"
                            current_stock = collect_stock("A4 Art Paper 150 gsm")

                        if items[1] == "A4 Photo Paper":
                            stock_name = "A4 Photo Paper"
                            current_stock = collect_stock("A4 Photo Paper")

                        if items[1] == "Passport Photo Printing":
                            stock_name = "Passport Paper"
                            current_stock = collect_stock("Passport Paper")

                        if items[1] == "A3 Printing B/W" or items[1] == "A3 Printing Coloured" or \
                                items[1] == "A3 Copy B/W" or items[1] == "A3 Copy Coloured":
                            stock_name = "A3 Paper"
                            current_stock = collect_stock("A3 Paper")

                        if items[1] == "A5 Photo Paper":
                            stock_name = "A5 Photo Paper"
                            current_stock = collect_stock("A5 Photo Paper")

                        if items[1] == "A3 150 gsm":
                            stock_name = "A3 Art Paper 150 gsm"
                            current_stock = collect_stock("A3 Art Paper 150 gsm")

                        if items[1] == "A4 250/275/300 gsm":
                            stock_name = "A4 Art Paper 250/275/300 gsm"
                            current_stock = collect_stock("A4 Art Paper 250/275/300 gsm")

                        if items[1] == "A3 250/275/300 gsm":
                            stock_name = "A3 Art Paper 250/275/300 gsm"
                            current_stock = collect_stock("A3 Art Paper 250/275/300 gsm")

                    else:
                        current_stock = collect_stock(items[1])
                        stock_name = items[1]

                    today = datetime.datetime.today()
                    current_time = today.strftime("%d/%B/%Y %H:%M")
                    new_stock = int(stock) + int(current_stock[0][3])

                    conn = connect(path_to_database)
                    writes = conn.cursor()
                    lk_comm = "UPDATE stock SET quantity='{}' WHERE description='{}'".format(new_stock, stock_name)
                    lk_comm2 = "UPDATE stock SET stockindate='{}' WHERE description='{}'".format(current_time,
                                                                                                 stock_name)
                    writes.execute(lk_comm)
                    writes.execute(lk_comm2)
                    conn.commit()
                    conn.close()
                    change_stock_cancel()

            except ValueError:
                pass

            except TclError:
                pass

        self.cashier_stock_button = Button(self.cashier_stock_frame, bg='light green')
        self.cashier_stock_button.configure(state='disabled', text="UPDATE", font=(font, font_adjust(12)),
                                            relief='solid')
        self.cashier_stock_button.configure(command=update_stock)
        self.cashier_stock_button.place(x=widget_width(260), y=widget_height(180))

        self.cashier_cancel_stock = Button(self.cashier_stock_frame, bg='light yellow')
        self.cashier_cancel_stock.configure(state='disabled', text="CANCEL", font=(font, font_adjust(12)),
                                            relief='solid')
        self.cashier_cancel_stock.configure(command=change_stock_cancel)
        self.cashier_cancel_stock.place(x=widget_width(150), y=widget_height(180))

        self.change_stock_label = Label(self.window_initializer)
        self.change_stock_label.configure(text="Add Stock", font=(font, font_adjust(11), "bold"))
        self.change_stock_label.place(x=widget_width(530), y=widget_height(65))

        self.banner_frame = Frame(self.window_initializer)
        self.banner_frame.configure(background="#0b2971", height=widget_height(50), width=x)
        self.banner_frame.place(x=0, y=0)

        self.banner_frame_text = Label(self.banner_frame, bg='#0b2971')
        self.banner_frame_text.configure(text="HUDUMIA CYBER POS TERMINAL", font=(font, font_adjust(18), 'bold'),
                                         fg='white')
        self.banner_frame_text.place(x=x / 2 - 200, y=widget_height(7))

        # =================================== Bottom Panel =========================================
        self.bottom_frame = Frame(self.window_initializer)
        self.bottom_frame.configure(bg='#30475c', height=widget_height(50), width=x)
        self.bottom_frame.place(x=0, y=widget_height(790))
        self.after_id = None

        def collect_float():
            display_time = time.strftime('%d/%B/%Y')

            connection = connect(path_to_database)
            write = connection.cursor()
            lk_command = "SELECT Float FROM Costs WHERE Date LIKE '{}'".format(display_time)
            write.execute(lk_command)
            values = write.fetchall()
            connection.close()

            if len(values) == 0:
                self.float_warn = Label(self.bottom_frame, fg="yellow", bg="#30475c")
                self.float_warn.configure(font=(font, font_adjust(14)))
                self.float_warn.configure(text="Float balance not entered, press F8 and enter float balance!")
                self.float_warn.place(x=widget_width(50), y=widget_height(7))

        collect_float()

        def present_time():
            display_time = time.strftime('%d-%B-%Y %H:%M:%S %p')
            self.clock_label.config(text=display_time)
            self.after_id = self.clock_label.after(1000, present_time)

        self.clock_label = Label(self.bottom_frame, fg="white", bg="#30475c")
        self.clock_label.configure(font=(font, font_adjust(11)))
        self.clock_label.place(x=widget_width(1270), y=widget_height(7))

        present_time()

        self.sales_count_label = Label(self.bottom_frame, fg="white", bg="#30475c")
        self.sales_count_label.configure(text="Today's Sales:", font=(font, font_adjust(11)))
        self.sales_count_label.place(x=widget_width(945), y=widget_height(8))

        self.sales_count = Label(self.bottom_frame, fg="white", bg="#30475c")
        self.sales_count.configure(text=0, font=(font, font_adjust(11)))
        self.sales_count.place(x=widget_width(1060), y=widget_height(8))

        self.sales_label = Label(self.bottom_frame, fg="white", bg="#30475c")
        self.sales_label.configure(text="Sales: ", font=(font, font_adjust(11)))
        self.sales_label.place(x=widget_width(1125), y=widget_height(8))

        self.sales_amount = Label(self.bottom_frame, fg="white", bg="#30475c")
        self.sales_amount.configure(text=0, font=(font, font_adjust(11)))
        self.sales_amount.place(x=widget_width(1175), y=widget_height(8))

        # =================================== Right Side Panel =========================================
        self.right_frame = Frame(self.window_initializer)
        self.right_frame.configure(bg='#30475c', height=widget_height(685), width=widget_width(330))
        self.right_frame.place(x=widget_width(1270), y=widget_height(50))

        # ===================================== Right panel buttons ============================================
        self.transaction_count_frame = Frame(self.right_frame)
        self.transaction_count_frame.configure(bg='#058de2', width=widget_width(290), height=widget_height(100))
        self.transaction_count_frame.place(x=widget_width(20), y=widget_height(160))

        self.transaction = Label(self.transaction_count_frame)
        self.transaction.configure(text='TRANSACTION NO:', font=(font, font_adjust(11), 'bold'), fg='white',
                                   bg='#058de2')
        self.transaction.place(x=widget_width(10), y=widget_height(10))

        self.transaction_count = Label(self.transaction_count_frame)
        self.transaction_count.configure(text='000000000000', font=(font, font_adjust(18), 'bold'), fg='white',
                                         bg='#058de2')
        self.transaction_count.place(x=widget_width(50), y=widget_height(40))

        self.new_transaction_btn = Button(self.right_frame, font=(font, font_adjust(14), 'bold'),
                                          command=self.new_transaction_function)
        self.new_transaction_btn.configure(text='[F1] NEW TRANSACTION', fg='white', bg='#00ab78', relief='ridge',
                                           height=widget_height(2))
        self.new_transaction_btn.place(x=widget_width(22), y=widget_height(280), width=widget_width(290))

        self.add_to_cart_btn = Button(self.right_frame, font=(font, font_adjust(14), 'bold'))
        self.add_to_cart_btn.configure(text='[F2] ADD TO CART', fg='white', bg='#058de2', relief='ridge',
                                       height=widget_height(2))
        self.add_to_cart_btn.config(state='disabled', command=self.add_to_cart_function)
        self.add_to_cart_btn.place(x=widget_width(22), y=widget_height(360), width=widget_width(290))

        self.delete_cart_item_btn = Button(self.right_frame, font=(font, font_adjust(14), 'bold'))
        self.delete_cart_item_btn.configure(text='[DEL] DELETE ITEM', fg='white', bg='#058de2', relief='ridge',
                                            height=widget_height(2))
        self.delete_cart_item_btn.config(state='disabled', command=self.delete_cart_item)
        self.delete_cart_item_btn.place(x=widget_width(22), y=widget_height(440), width=widget_width(290))

        self.clear_cart_btn = Button(self.right_frame, font=(font, font_adjust(14), 'bold'))
        self.clear_cart_btn.configure(text='[END] CLEAR CART', fg='white', bg='#058de2', relief='ridge',
                                      height=widget_height(2))
        self.clear_cart_btn.config(state='disabled', command=self.clear_cart)
        self.clear_cart_btn.place(x=widget_width(22), y=widget_height(520), width=widget_width(290))

        self.payment_btn = Button(self.right_frame, font=(font, font_adjust(14), 'bold'))
        self.payment_btn.configure(text='[F12] MAKE PAYMENT', fg='white', bg='#058de2', relief='ridge',
                                   height=widget_height(2))
        self.payment_btn.config(state='disabled', command=self.make_pay)
        self.payment_btn.place(x=widget_width(22), y=widget_height(600), width=widget_width(290))

        self.total_sub_label = Label(self.right_frame)
        self.total_sub_label.configure(text='TOTAL', font=(font, font_adjust(18), 'bold'), bg='#30475c', fg='white')
        self.total_sub_label.place(x=widget_width(15), y=widget_height(13))

        self.currency_label = Label(self.right_frame)
        self.currency_label.configure(text='(Kshs.)', font=(font, font_adjust(13), 'bold'), bg='#30475c', fg='white')
        self.currency_label.place(x=widget_width(100), y=widget_height(20))

        self.payment_label = Label(self.right_frame)
        self.payment_label.configure(text='0.00', font=(font, font_adjust(50), 'bold'), bg='#30475c', fg='#00df7e')
        self.payment_label.place(x=widget_width(50), y=widget_height(50))

        columns = ('Code', 'Description', 'Price', 'Quantity', 'Subtotal')
        style = Style()
        style.theme_use('clam')
        style.configure('Treeview.Heading', background="#3e3f3f", foreground='white',
                        font=(font, font_adjust(14), 'bold'),
                        relief='none')

        self.cart_table = Treeview(self.window_initializer, columns=columns, show='headings')

        self.cart_table.heading("# 1", text='Code', anchor=CENTER)
        self.cart_table.column("# 1", stretch=NO, minwidth=widget_width(165), width=widget_width(165), anchor=CENTER)
        self.cart_table.heading("# 2", text='Description', anchor="w")
        self.cart_table.column("# 2", stretch=NO, minwidth=widget_width(450), width=widget_width(450), anchor="w")
        self.cart_table.heading("# 3", text='Price', anchor=CENTER)
        self.cart_table.column("# 3", stretch=NO, minwidth=widget_width(200), width=widget_width(200), anchor=CENTER)
        self.cart_table.heading("# 4", text='Quantity', anchor=CENTER)
        self.cart_table.column("# 4", stretch=NO, minwidth=widget_width(200), width=widget_width(200), anchor=CENTER)
        self.cart_table.heading("# 5", text='Subtotal', anchor=CENTER)
        self.cart_table.column("# 5", stretch=NO, minwidth=widget_width(250), width=widget_width(250), anchor=CENTER)

        self.cart_table.place(x=0, y=widget_width(530), height=widget_height(405))

        def selecting_items(event):
            item = self.cart_table.focus()
            items = self.cart_table.item(item)['values']

            try:
                self.cashier_update_product_code.configure(state='normal')
                self.cashier_update_product_code.delete(0, END)
                self.cashier_update_product_code.insert(0, items[0])
                self.cashier_update_product_code.configure(state='disabled')

                self.cashier_update_product_desc.configure(state='normal')
                self.cashier_update_product_desc.delete(0, END)
                self.cashier_update_product_desc.insert(0, items[1])
                self.cashier_update_product_desc.configure(state='disabled')

                self.cashier_update_product_quan.configure(state='normal')
                self.cashier_update_product_quan.delete(0, END)
                self.cashier_update_product_quan.focus_set()

                self.cashier_update_button.configure(state='normal')
                self.cashier_cancel_button.configure(state='normal')

            except IndexError:
                pass

        self.cart_table.bind("<Double-1>", selecting_items)

        def stock_update(event):
            item = self.cart_table.focus()
            items = self.cart_table.item(item)['values']
            current_stock = 0

            if items != "":
                def collect_stock(desc):
                    db_co = connect(path_to_database)
                    wri = db_co.cursor()
                    ll = "SELECT * FROM {} WHERE description='{}'".format("stock", desc)
                    wri.execute(ll)
                    r = wri.fetchall()
                    db_co.close()

                    return r

                db_co = connect(path_to_database)
                wri = db_co.cursor()
                ll = "SELECT category FROM {} WHERE productcode='{}'".format("products", items[0])
                wri.execute(ll)
                r = wri.fetchall()
                db_co.close()

                try:
                    if r[0][0] == "Printing":
                        if items[1] == "A4 Printing B/W" or items[1] == "A4 Printing Coloured" or \
                                items[1] == "A4 Copy B/W" or items[1] == "A4 Copy Coloured":
                            current_stock = collect_stock("A4 Rim Papers")

                        if items[1] == "A4 Glossy Paper Printing":
                            current_stock = collect_stock("Glossy Paper")

                        if items[1] == "A4 150 gsm":
                            current_stock = collect_stock("A4 Art Paper 150 gsm")

                        if items[1] == "A4 Photo Paper":
                            current_stock = collect_stock("A4 Photo Paper")

                        if items[1] == "Passport Photo Printing":
                            current_stock = collect_stock("Passport Paper")

                        if items[1] == "A3 Printing B/W" or items[1] == "A3 Printing Coloured" or \
                                items[1] == "A3 Copy B/W" or items[1] == "A3 Copy Coloured":
                            current_stock = collect_stock("A3 Paper")

                        if items[1] == "A5 Photo Paper":
                            current_stock = collect_stock("A5 Photo Paper")

                        if items[1] == "A3 150 gsm":
                            current_stock = collect_stock("A3 Art Paper 150 gsm")

                        if items[1] == "A4 250/275/300 gsm":
                            current_stock = collect_stock("A4 Art Paper 250/275/300 gsm")

                        if items[1] == "A3 250/275/300 gsm":
                            current_stock = collect_stock("A3 Art Paper 250/275/300 gsm")

                    else:
                        current_stock = collect_stock(items[1])

                except IndexError:
                    pass

                try:
                    self.cashier_stock_button.configure(state='normal')
                    self.cashier_cancel_stock.configure(state='normal')

                    self.cashier_stock_product_code.configure(state='normal')
                    self.cashier_stock_product_code.delete(0, END)
                    self.cashier_stock_product_code.insert(0, items[0])
                    self.cashier_stock_product_code.configure(state='disabled')

                    self.cashier_stock_product_desc.configure(state='normal')
                    self.cashier_stock_product_desc.delete(0, END)
                    self.cashier_stock_product_desc.insert(0, items[1])
                    self.cashier_stock_product_desc.configure(state='disabled')

                    self.cashier_stock_product_new.configure(state='normal')
                    self.cashier_stock_product_new.delete(0, END)
                    self.cashier_stock_product_new.focus_set()

                    self.cashier_stock_product_quan.configure(state='normal')
                    self.cashier_stock_product_quan.delete(0, END)
                    self.cashier_stock_product_quan.insert(0, current_stock[0][3])
                    self.cashier_stock_product_quan.configure(state='disabled')

                except TypeError:
                    change_stock_cancel()

                except IndexError:
                    change_stock_cancel()

            else:
                pass

        self.window_initializer.bind("<KeyPress-Insert>", stock_update)

        self.update_sales()

        def new_transaction_shortcut(event):
            btn_state = str(self.new_transaction_btn['state'])

            if btn_state == 'normal':
                self.new_transaction_function()

            else:
                pass

        def add_to_cart_shortcut(event):
            btn_state = str(self.add_to_cart_btn['state'])

            if btn_state == 'normal':
                self.add_to_cart_function()

            else:
                pass

        def delete_cart_shortcut(event):
            btn_state = str(self.delete_cart_item_btn['state'])

            if btn_state == 'normal':
                self.delete_cart_item()

            else:
                pass

        def clear_cart_shortcut(event):
            btn_state = str(self.clear_cart_btn['state'])

            if btn_state == 'normal':
                self.clear_cart()

            else:
                pass

        def make_pay_shortcut(event):
            btn_state = str(self.payment_btn['state'])

            if btn_state == 'normal':
                self.make_pay()

            else:
                pass

        self.window_initializer.bind("<KeyPress-F1>", new_transaction_shortcut)
        self.window_initializer.bind("<KeyPress-F2>", add_to_cart_shortcut)
        self.window_initializer.bind("<KeyPress-Delete>", delete_cart_shortcut)
        self.window_initializer.bind("<KeyPress-End>", clear_cart_shortcut)
        self.window_initializer.bind("<KeyPress-F12>", make_pay_shortcut)

        def debt_window(event):
            window_debt = Toplevel(self.window_initializer)
            window_debt.title("Debt Center")
            window_debt.geometry("1100x600")
            window_debt.resizable(False, False)
            center(window_debt)
            search_value = StringVar()

            search_label = Label(window_debt)
            search_label.configure(font=(font, 13), text="Search Name:")
            search_label.place(x=widget_width(400), y=widget_height(35))

            search_entry = Entry(window_debt, textvariable=search_value)
            search_entry.configure(relief="solid", font=(font, 13), justify=CENTER)
            search_entry.place(x=widget_width(555), y=widget_height(35), width=widget_width(250))
            search_entry.focus_set()

            debt_column = ('Transaction Id', 'Name', 'Contact', 'Debt Amount', 'Date')
            style.configure('Treeview.Heading', background="#3e3f3f", foreground='white',
                            font=(font, font_adjust(11), 'bold'),
                            relief='none')

            cart_table = Treeview(window_debt, columns=debt_column, show='headings')

            cart_table.heading("# 1", text='Transaction Id', anchor=CENTER)
            cart_table.column("# 1", stretch=NO, minwidth=widget_width(200), width=widget_width(200),
                              anchor=CENTER)
            cart_table.heading("# 2", text='Name', anchor="w")
            cart_table.column("# 2", stretch=NO, minwidth=widget_width(200), width=widget_width(200), anchor="w")
            cart_table.heading("# 3", text='Contact', anchor=CENTER)
            cart_table.column("# 3", stretch=NO, minwidth=widget_width(200), width=widget_width(200),
                              anchor=CENTER)
            cart_table.heading("# 4", text='Debt Amount', anchor=CENTER)
            cart_table.column("# 4", stretch=NO, minwidth=widget_width(150), width=widget_width(150),
                              anchor=CENTER)
            cart_table.heading("# 5", text='Date', anchor=CENTER)
            cart_table.column("# 5", stretch=NO, minwidth=widget_width(210), width=widget_width(210),
                              anchor=CENTER)

            cart_table.place(x=50, y=widget_width(100), height=widget_height(405))

            db_connection = connect(path_to_database)
            writer = db_connection.cursor()
            lookup_command = "SELECT * FROM {}".format("debts")
            writer.execute(lookup_command)
            result = writer.fetchall()
            db_connection.close()

            for i in range(0, len(result)):
                cart_table.insert("", 'end', text="1",
                                  values=(result[i][0], result[i][1] + ", " + result[i][2], result[i][3], result[i][4],
                                          result[i][5]))

            def search_filter(*args):
                items_on_treeview = cart_table.get_children()
                search = search_value.get().lower().strip()

                for each_itme in items_on_treeview:
                    if search in cart_table.item(each_itme)['values'][1].lower():
                        search_var = cart_table.item(each_itme)['values']
                        cart_table.delete(each_itme)

                        cart_table.insert("", 0, values=search_var)

            search_value.trace("w", search_filter)

            def close_debt_window(event):
                window_debt.destroy()

            window_debt.bind("<KeyPress-Home>", close_debt_window)

            def selecting_debt(event):
                item = cart_table.focus()
                items = cart_table.item(item)['values']
                poss_debt = IntVar()

                debt_center = Toplevel(window_debt)
                debt_center.geometry("300x300")
                debt_center.title("Debt Settlement")
                center(debt_center)

                debt_center_name = Label(debt_center)
                debt_center_name.configure(text="Name:", font=(font, font_adjust(13), "bold"))
                debt_center_name.place(x=widget_width(20), y=widget_height(20))

                debt_center_name_entry = Entry(debt_center)
                debt_center_name_entry.configure(font=(font, font_adjust(13)), justify=CENTER)
                debt_center_name_entry.delete(0, END)
                debt_center_name_entry.insert(0, items[1])
                debt_center_name_entry.configure(state="disabled")
                debt_center_name_entry.place(x=widget_width(100), y=widget_height(23))

                debt_center_owed = Label(debt_center)
                debt_center_owed.configure(text="Debt:", font=(font, font_adjust(13), "bold"))
                debt_center_owed.place(x=widget_width(20), y=widget_height(70))

                debt_center_owed_entry = Entry(debt_center)
                debt_center_owed_entry.configure(font=(font, font_adjust(13)), justify=CENTER)
                debt_center_owed_entry.delete(0, END)
                debt_center_owed_entry.insert(0, items[3])
                debt_center_owed_entry.configure(state="disabled")
                debt_center_owed_entry.place(x=widget_width(100), y=widget_height(73))

                debt_center_paid = Label(debt_center)
                debt_center_paid.configure(text="Paid:", font=(font, font_adjust(13), "bold"))
                debt_center_paid.place(x=widget_width(20), y=widget_height(120))

                debt_paid = StringVar()
                debt_center_paid_entry = Entry(debt_center, textvariable=debt_paid)
                debt_center_paid_entry.configure(font=(font, font_adjust(13)), justify=CENTER)
                debt_center_paid_entry.place(x=widget_width(100), y=widget_height(123))

                debt_included = Checkbutton(debt_center)
                debt_included.configure(text="Paid full?", variable=poss_debt, font=(font, font_adjust(11)))
                debt_included.place(x=180, y=170)

                def save_function():
                    if int(poss_debt.get()) == 0 and debt_paid.get().strip() != "":
                        try:
                            if float(debt_paid.get().strip()) < float(items[3]):
                                paid_debt = debt_paid.get().strip()
                                new_debt = float(items[3]) - float(paid_debt)

                                db_co = connect(path_to_database)
                                wri = db_co.cursor()
                                ll = "SELECT * FROM Transactions WHERE TransactionId='{}'".format(items[0])
                                wri.execute(ll)
                                r = wri.fetchall()
                                db_co.close()

                                paid_amount = r[0][4]
                                new_paid_amount = float(paid_amount) + float(paid_debt)

                                today = datetime.datetime.today()
                                current_time = today.strftime("%d/%B/%Y %H:%M")

                                conn = connect(path_to_database)
                                writes = conn.cursor()
                                lk_comm = "UPDATE debts SET debtamount='{}' WHERE TransactionId='{}'".format(new_debt,
                                                                                                             items[0])
                                lk_comm2 = "UPDATE debts SET date='{}' WHERE TransactionId='{}'".format(current_time,
                                                                                                        items[0])
                                lk_comm3 = "UPDATE Transactions SET debt='{}' WHERE TransactionId='{}'".format(new_debt,
                                                                                                               items[0])
                                lk_comm4 = "UPDATE Transactions SET AmountPaid='{}' WHERE TransactionId='{}'".format(
                                    new_paid_amount, items[0])
                                writes.execute(lk_comm)
                                writes.execute(lk_comm2)
                                writes.execute(lk_comm3)
                                writes.execute(lk_comm4)
                                conn.commit()
                                conn.close()
                                window_debt.destroy()

                            else:
                                messagebox.showerror("Error", "Paid amount cannot be greater than debt")

                        except ValueError:
                            messagebox.showwarning("Paid Amount Error", "Amount paid should be a number only")

                    elif int(poss_debt.get()) == 1 and debt_paid.get().strip() == "":
                        db_co = connect(path_to_database)
                        wri = db_co.cursor()
                        ll = "SELECT * FROM Transactions WHERE TransactionId='{}'".format(items[0])
                        wri.execute(ll)
                        r = wri.fetchall()
                        db_co.close()

                        paid_amount = r[0][4]
                        mode = r[0][8]
                        debt = r[0][7]

                        if mode == "cash":
                            full_settle = float(paid_amount + debt)
                            conn = connect(path_to_database)
                            writes = conn.cursor()
                            lk_comm = "UPDATE Transactions SET AmountPaid='{}' WHERE TransactionId='{}'".format(
                                full_settle, items[0])
                            lk_comm2 = "UPDATE Transactions SET CashAmount='{}' WHERE TransactionId='{}'".format(0.0,
                                                                                                                 items[
                                                                                                                     0])
                            lk_comm3 = "UPDATE Transactions SET debt='{}' WHERE TransactionId='{}'".format(0.0,
                                                                                                           items[0])
                            lk_comm4 = "DELETE FROM debts WHERE TransactionId='{}'".format(items[0])
                            writes.execute(lk_comm)
                            writes.execute(lk_comm2)
                            writes.execute(lk_comm3)
                            writes.execute(lk_comm4)
                            conn.commit()
                            conn.close()

                        elif mode == "mpesa":
                            full_settle = float(paid_amount + debt)
                            conn = connect(path_to_database)
                            writes = conn.cursor()
                            lk_comm = "UPDATE Transactions SET AmountPaid='{}' WHERE TransactionId='{}'".format(
                                full_settle, items[0])
                            lk_comm3 = "UPDATE Transactions SET debt='{}' WHERE TransactionId='{}'".format(0.0,
                                                                                                           items[0])
                            lk_comm4 = "DELETE FROM debts WHERE TransactionId='{}'".format(items[0])
                            writes.execute(lk_comm)
                            writes.execute(lk_comm3)
                            writes.execute(lk_comm4)
                            conn.commit()
                            conn.close()

                        elif mode == "debt":
                            full_settle = float(paid_amount + debt)
                            conn = connect(path_to_database)
                            writes = conn.cursor()
                            lk_comm = "UPDATE Transactions SET AmountPaid='{}' WHERE TransactionId='{}'".format(
                                full_settle, items[0])
                            lk_comm2 = "UPDATE Transactions SET ModeofPayment='{}' WHERE TransactionId='{}'".format(
                                "cash", items[0])
                            lk_comm3 = "UPDATE Transactions SET debt='{}' WHERE TransactionId='{}'".format(0.0,
                                                                                                           items[0])
                            lk_comm4 = "DELETE FROM debts WHERE TransactionId='{}'".format(items[0])
                            writes.execute(lk_comm)
                            writes.execute(lk_comm2)
                            writes.execute(lk_comm3)
                            writes.execute(lk_comm4)
                            conn.commit()
                            conn.close()

                        else:
                            pass

                        debt_center.destroy()
                        db_connection = connect(path_to_database)
                        writer = db_connection.cursor()
                        lookup_command = "SELECT * FROM {}".format("debts")
                        writer.execute(lookup_command)
                        result = writer.fetchall()
                        db_connection.close()

                        for cart_it in cart_table.get_children():
                            cart_table.delete(cart_it)

                        for i in range(0, len(result)):
                            cart_table.insert("", 'end', text="1",
                                              values=(result[i][0], result[i][1] + ", " + result[i][2], result[i][3],
                                                      result[i][4], result[i][5]))

                    else:
                        messagebox.showwarning("Error",
                                               "Paid full checkbox cannot be selected when amount is not empty")
                        debt_center.destroy()

                save_record = Button(debt_center, bg="green", fg="white")
                save_record.configure(relief='solid', text="SAVE RECORD", font=(font, 14), command=save_function)
                save_record.place(x=85, y=220)

            cart_table.bind("<Double-1>", selecting_debt)

        self.window_initializer.bind("<KeyPress-F5>", debt_window)

        def admin_win():
            self.window_initializer.destroy()
            self.window_initializer.after_cancel(self.after_id)
            time.sleep(1)
            load_main_login_page()

        def load_admin_window(event):
            admin_win()

        self.window_initializer.bind("<KeyPress-F11>", load_admin_window)

        self.admin_page = Button(self.banner_frame, fg="white", bg="#0b2971", command=admin_win)
        self.admin_page.configure(text="Admin", font=(font, font_adjust(13)), relief="solid")
        self.admin_page.place(x=widget_width(1400), y=widget_height(5))

        def reports(event):
            self.create_report()

        self.window_initializer.bind("<KeyPress-F6>", reports)

        def remove_st(event):
            self.remove_stock()

        self.window_initializer.bind("<KeyPress-F7>", remove_st)

        def cost_win(event):
            self.costs_window()

        self.window_initializer.bind("<KeyPress-F8>", cost_win)

        def track_orders(event):
            order_tracker = Toplevel(self.window_initializer)
            order_tracker.geometry("900x500")
            order_tracker.title("Sales Tracker")
            center(order_tracker)

            search_value = StringVar()
            year_value = StringVar()

            search_label = Label(order_tracker)
            search_label.configure(font=(font, 13), text="Enter Order No:")
            search_label.place(x=widget_width(600), y=widget_height(35))

            search_entry = Entry(order_tracker, textvariable=search_value)
            search_entry.configure(relief="solid", font=(font, 13), justify=CENTER)
            search_entry.place(x=widget_width(750), y=widget_height(35), width=widget_width(150))
            search_entry.focus_set()
            search_entry.delete(0, END)

            year_label = Label(order_tracker)
            year_label.configure(font=(font, 13), text="Year:")
            year_label.place(x=widget_width(300), y=widget_height(35))

            today = datetime.datetime.today()
            current_year = today.strftime("%Y")

            year_entry = Entry(order_tracker, textvariable=year_value)
            year_entry.configure(relief="solid", font=(font, 13), justify=CENTER)
            year_entry.place(x=widget_width(380), y=widget_height(35), width=widget_width(150))
            year_entry.delete(0, END)
            year_entry.insert(0, current_year)

            sales_column = ('Code', 'Description', 'Price', 'Quantity', 'Subtotal', 'Total')
            style.configure('Treeview.Heading', background="#3e3f3f", foreground='white',
                            font=(font, font_adjust(13), 'bold'), relief='none')

            sales_table = Treeview(order_tracker, columns=sales_column, show='headings')

            sales_table.heading("# 1", text='Transaction No', anchor=CENTER)
            sales_table.column("# 1", stretch=NO, minwidth=widget_width(170), width=widget_width(170), anchor=CENTER)
            sales_table.heading("# 2", text='Date', anchor="w")
            sales_table.column("# 2", stretch=NO, minwidth=widget_width(250), width=widget_width(250), anchor="w")
            sales_table.heading("# 3", text='Description', anchor=CENTER)
            sales_table.column("# 3", stretch=NO, minwidth=widget_width(250), width=widget_width(250), anchor=CENTER)
            sales_table.heading("# 4", text='Unit Price', anchor=CENTER)
            sales_table.column("# 4", stretch=NO, minwidth=widget_width(150), width=widget_width(150), anchor=CENTER)
            sales_table.heading("# 5", text='Bought', anchor=CENTER)
            sales_table.column("# 5", stretch=NO, minwidth=widget_width(100), width=widget_width(100), anchor=CENTER)
            sales_table.heading("# 6", text='Sub Total', anchor=CENTER)
            sales_table.column("# 6", stretch=NO, minwidth=widget_width(100), width=widget_width(100), anchor=CENTER)

            sales_table.place(x=30, y=100, height=350)

            db_connection = connect(path_to_database)
            writer = db_connection.cursor()
            lookup_command = "SELECT * FROM {}".format("Sales")
            writer.execute(lookup_command)
            result = writer.fetchall()
            db_connection.close()

            for i in range(0, len(result)):
                sales_table.insert("", 'end', text="1", values=(result[i][0], result[i][1], result[i][2], result[i][3],
                                                                result[i][4], result[i][5]))

            def search_filter(*args):
                items_on_treeview = sales_table.get_children()
                year = year_value.get().strip()
                search = search_value.get().strip()
                transaction_format = "000000000"
                order_tracker_length = len(str(search))
                transaction_number = str(year) + str(transaction_format[:-order_tracker_length]) + str(search)

                for each_itme in items_on_treeview:
                    if transaction_number in str(sales_table.item(each_itme)['values'][0]):
                        search_var = sales_table.item(each_itme)['values']
                        sales_table.delete(each_itme)
                        sales_table.insert("", 0, values=search_var)

            search_value.trace("w", search_filter)

            def close_tracker(event):
                order_tracker.destroy()

            order_tracker.bind("<KeyPress-Home>", close_tracker)

        self.window_initializer.bind("<KeyPress-F9>", track_orders)

        def cash_receivable(event):
            cash_win = Toplevel(self.window_initializer)
            cash_win.geometry("480x180")
            cash_win.title("Account Receivable")
            cash_win.resizable(False, False)
            center(cash_win)

            account_amount = DoubleVar()

            cash_label = Label(cash_win)
            cash_label.configure(text="Account Receivable:", font=(font, 12, "bold"))
            cash_label.place(x=30, y=20)

            account_entry_ = Entry(cash_win, textvariable=account_amount)
            account_entry_.configure(font=(font, 12), relief="solid", justify=CENTER)
            account_entry_.place(x=230, y=20)
            account_entry_.delete(0, END)

            def save_amount():
                try:
                    cash_amount = account_amount.get()

                    today = datetime.datetime.today()
                    current_time = today.strftime("%d/%B/%Y")

                    if cash_amount > 0:
                        conn = connect(path_to_database)
                        c = conn.cursor()
                        params2 = (current_time, cash_amount)
                        c.execute("INSERT INTO Account_recv VALUES (?, ?)", params2)
                        conn.commit()
                        conn.close()
                        account_entry_.delete(0, END)

                    else:
                        messagebox.showwarning("Amount Error", "Amount should be greater than 0")

                except TclError:
                    messagebox.showwarning("Amount Error", "Amount should be a number")

            _save_btn = Button(cash_win, fg="white", bg="green", command=save_amount)
            _save_btn.configure(text="SAVE", font=(font, 13), relief="solid")
            _save_btn.place(x=180, y=80, width=100)

        self.window_initializer.bind("<KeyPress-F12>", cash_receivable)

    def new_transaction_function(self):
        self.add_to_cart_btn.config(state='normal')
        self.delete_cart_item_btn.config(state='normal')
        self.clear_cart_btn.config(state='normal')
        self.payment_btn.config(state='normal')
        self.new_transaction_btn.config(state='disabled')

        today = datetime.datetime.today()
        current_year = today.strftime("%Y")

        db_connection = connect(path_to_database)
        writer = db_connection.cursor()
        lookup_command = "SELECT TransactionId FROM {}".format(tables[3])
        writer.execute(lookup_command)
        result = writer.fetchall()
        db_connection.close()

        try:
            transaction_number = str(result[-1])
            last_transaction_number = transaction_number.replace('(', '').replace(',', '').replace(')', '')
            new_prefix = str(current_year)
            new_transaction_count = int(last_transaction_number) + 1
            self.new_transaction_number = new_prefix + str(new_transaction_count)[4:]

            self.transaction_count.configure(text=str(self.new_transaction_number))

        except IndexError:
            transaction_number = str(2023000000000)
            last_transaction_number = transaction_number.replace('(', '').replace(',', '').replace(')', '')
            new_prefix = str(current_year)
            new_transaction_count = int(last_transaction_number) + 1
            self.new_transaction_number = new_prefix + str(new_transaction_count)[4:]

            self.transaction_count.configure(text=str(self.new_transaction_number))

        except ValueError:
            transaction_number = str(2023000000000)
            last_transaction_number = transaction_number.replace('(', '').replace(',', '').replace(')', '')
            new_prefix = str(current_year)
            new_transaction_count = int(last_transaction_number) + 1
            self.new_transaction_number = new_prefix + str(new_transaction_count)[4:]

            self.transaction_count.configure(text=str(self.new_transaction_number))

    def add_to_cart_function(self):
        cart_child_process = Toplevel(self.window_initializer)
        cart_child_process.geometry('768x620')
        cart_child_process.resizable(False, False)
        center(cart_child_process)
        cart_child_process.title('SEARCH ITEM TO ADD TO CART')

        product_columns = ('Code', 'Description', 'Price')
        services_columns = ('Code', 'Description', 'Price')

        add_item_table = Treeview(cart_child_process, columns=product_columns, show='headings')
        services_item_table = Treeview(cart_child_process, columns=services_columns, show='headings')

        products_button = Button(cart_child_process)
        services_button = Button(cart_child_process)

        def clear_carts():
            for item in add_item_table.get_children():
                add_item_table.delete(item)

            for item in services_item_table.get_children():
                services_item_table.delete(item)

        def products_section():
            clear_carts()
            # ==================================== Tree view =============================================
            style = Style()
            style.theme_use('clam')
            style.configure('Treeview.Heading', background="#3e3f3f", foreground='white',
                            font=('yu gothic ui', 12, 'bold'))

            add_item_table.heading("# 1", text='Code', anchor="w")
            add_item_table.column("# 1", stretch=NO, minwidth=150, width=150)
            add_item_table.heading("# 2", text='Description', anchor="w")
            add_item_table.column("# 2", stretch=NO, minwidth=300, width=300)
            add_item_table.heading("# 3", text='Price', anchor=CENTER)
            add_item_table.column("# 3", stretch=NO, minwidth=100, width=100, anchor=CENTER)

            add_item_table.place(x=100, y=80, height=500)

            db_connection = connect(path_to_database)
            writer = db_connection.cursor()
            lookup_command = "SELECT * FROM {}".format("Products")
            writer.execute(lookup_command)
            result = writer.fetchall()
            db_connection.close()

            for i in range(0, len(result)):
                add_item_table.insert("", 'end', text="1",
                                      values=(result[i][1], result[i][2], result[i][4]))

            style.configure('Treeview', font=('yu gothic ui', 13))
            products_button.configure(state='disabled')
            services_button.configure(state='normal')
            services_item_table.place(x=0, y=800, height=0)

        def services_section():
            clear_carts()
            # ==================================== Tree view =============================================
            style = Style()
            style.theme_use('clam')
            style.configure('Treeview.Heading', background="#3e3f3f", foreground='white',
                            font=('yu gothic ui', 12, 'bold'))

            services_item_table.heading("# 1", text='Code', anchor="w")
            services_item_table.column("# 1", stretch=NO, minwidth=150, width=150)
            services_item_table.heading("# 2", text='Description', anchor="w")
            services_item_table.column("# 2", stretch=NO, minwidth=300, width=300)
            services_item_table.heading("# 3", text='Price', anchor=CENTER)
            services_item_table.column("# 3", stretch=NO, minwidth=100, width=100, anchor=CENTER)

            services_item_table.place(x=100, y=80, height=500)

            db_connection = connect(path_to_database)
            writer = db_connection.cursor()
            lookup_command = "SELECT * FROM {}".format("services")
            writer.execute(lookup_command)
            result = writer.fetchall()
            db_connection.close()

            for i in range(0, len(result)):
                services_item_table.insert("", 'end', text="1", values=(result[i][1], result[i][2], result[i][3]))

            style.configure('Treeview', font=('yu gothic ui', 13))
            products_button.configure(state='normal')
            services_button.configure(state='disabled')
            add_item_table.place(x=0, y=800, height=0)

        self.cart_table.tag_configure('odd_row', background='#6ac0e6')
        self.cart_table.tag_configure('even_row', background='#DFDFDF')
        products_section()

        products_button.configure(text="PRODUCTS", relief='solid', font=(font, 13), bg='light green')
        products_button.configure(command=products_section)
        products_button.place(x=280, y=25)

        services_button.configure(text="SERVICES", relief='solid', font=(font, 13), bg='light blue')
        services_button.configure(command=services_section)
        services_button.place(x=420, y=25)

        def quick_cart_close(event):
            cart_child_process.destroy()

        cart_child_process.bind('<KeyPress-Home>', quick_cart_close)

        def load_products(event):
            if str(products_button['state']) == "normal":
                products_section()

            else:
                pass

        def load_services(event):
            if str(services_button['state']) == "normal":
                services_section()

            else:
                pass

        cart_child_process.bind('<KeyPress-Left>', load_products)
        cart_child_process.bind('<KeyPress-Right>', load_services)

        def selecting_items(event):
            quantity_variable = IntVar()

            quantity_window = Toplevel(cart_child_process)
            quantity_window.geometry('200x100')
            quantity_window.resizable(False, False)
            center(quantity_window)
            quantity_window.title('Quantity')

            quantity_entry = Entry(quantity_window)
            quantity_entry.focus_set()
            quantity_entry.configure(font=(font, 20), relief='solid', justify=CENTER, textvariable=quantity_variable)
            quantity_entry.delete(0, END)
            quantity_entry.place(x=0, y=0, height=100, width=200)

            def get_quantity(event):
                cart_duplicate = []

                for cart in self.cart_table.get_children():
                    cart_duplicate.append(self.cart_table.item(cart)['values'][0])

                try:
                    quantity = quantity_variable.get()
                    quantity_window.destroy()

                    item = add_item_table.focus()
                    items = add_item_table.item(item)['values']

                    if items[0] in cart_duplicate:
                        cart_child_process.destroy()
                        messagebox.showwarning("Duplicate", "Item already in cart")

                    else:
                        if self.count % 2 == 0:
                            payable = float(items[2]) * quantity
                            self.total_pay = round(payable + self.total_pay, 2)
                            self.payment_label.configure(text=str(self.total_pay))
                            items.append(str(quantity))
                            items.append(str(payable))
                            self.cart_table.insert("", 'end', values=items, tags=('even_row',))
                            self.count += 1

                        else:
                            payable = float(items[2]) * quantity
                            self.total_pay = round(payable + self.total_pay, 2)
                            self.payment_label.configure(text=str(self.total_pay))
                            items.append(str(quantity))
                            items.append(str(payable))
                            self.cart_table.insert("", 'end', values=items, tags=('odd_row',))
                            self.count += 1

                except TclError:
                    quantity_window.destroy()
                    cart_child_process.destroy()
                    messagebox.showerror("Quantity Error", "The quantity must be a number")
                    cart_duplicate.clear()

            quantity_window.bind('<Return>', get_quantity)

        add_item_table.bind("<Double-1>", selecting_items)

        def service_items(event):
            cart_duplicate = []

            quantity_variable = IntVar()

            quantity_window = Toplevel(cart_child_process)
            quantity_window.geometry('200x100')
            quantity_window.resizable(False, False)
            center(quantity_window)
            quantity_window.title('Quantity')

            quantity_entry = Entry(quantity_window)
            quantity_entry.focus_set()
            quantity_entry.configure(font=(font, 20), relief='solid', justify=CENTER, textvariable=quantity_variable)
            quantity_entry.delete(0, END)
            quantity_entry.place(x=0, y=0, height=100, width=200)

            def get_quantity(event):
                cart_duplicat = []

                for cart in self.cart_table.get_children():
                    cart_duplicat.append(self.cart_table.item(cart)['values'][0])

                try:
                    quantity = quantity_variable.get()
                    quantity_window.destroy()

                    item = services_item_table.focus()
                    items = services_item_table.item(item)['values']

                    if items[0] in cart_duplicat:
                        cart_child_process.destroy()
                        messagebox.showwarning("Duplicate", "Item already in cart")

                    else:
                        if self.count % 2 == 0:
                            payable = float(items[2]) * quantity
                            self.total_pay = round(payable + self.total_pay, 2)
                            self.payment_label.configure(text=str(self.total_pay))
                            items.append(str(quantity))
                            items.append(str(payable))
                            self.cart_table.insert("", 'end', values=items, tags=('even_row',))
                            self.count += 1

                        else:
                            payable = float(items[2]) * quantity
                            self.total_pay = round(payable + self.total_pay, 2)
                            self.payment_label.configure(text=str(self.total_pay))
                            items.append(str(quantity))
                            items.append(str(payable))
                            self.cart_table.insert("", 'end', values=items, tags=('odd_row',))
                            self.count += 1

                except TclError:
                    quantity_window.destroy()
                    cart_child_process.destroy()
                    messagebox.showerror("Quantity Error", "The quantity must be a number")
                    cart_duplicate.clear()

            quantity_window.bind('<Return>', get_quantity)

        services_item_table.bind("<Double-1>", service_items)

    def delete_cart_item(self):
        try:
            current_item = self.cart_table.focus()
            item_value = self.cart_table.item(current_item)
            self.total_pay = self.total_pay - float(item_value['values'][4])
            self.payment_label.configure(text=str(self.total_pay))
            self.cart_table.delete(current_item)

        except IndexError:
            pass

    def clear_cart(self):
        for item in self.cart_table.get_children():
            self.cart_table.delete(item)

        self.payment_label.configure(text="0.00")
        self.total_pay = self.total_pay - self.total_pay

    def update_sales(self):
        today = datetime.datetime.today()
        current_time = today.strftime("%d/%B/%Y")

        connection = connect(path_to_database)
        write = connection.cursor()
        lk_command = "SELECT SubTotal FROM Sales WHERE TransactionDate LIKE '{}'".format(current_time + "%")
        write.execute(lk_command)
        values = write.fetchall()
        connection.close()

        totals = []
        for price in values:
            totals.append(price[0])

        tot = (sum(totals))

        self.sales_count.configure(text=len(values))
        self.sales_amount.configure(text=(tot))

    def make_pay(self):
        payment_window = Toplevel(self.window_initializer)
        payment_window.geometry('600x400')
        center(payment_window)
        payment_window.title('PAYMENT PROCESSING')
        payment_window.resizable(False, False)

        discount_value = StringVar()
        separate_value = StringVar()
        debt_value = IntVar()

        def mpesa_sub_frame():
            try:
                poss_debt = IntVar()
                mpesa_frame = Frame(payment_window, width=500, height=300)
                mpesa_frame.configure(highlightthickness=3, highlightbackground='green')
                mpesa_frame.place(x=50, y=80)

                total_bill_label = Label(mpesa_frame)
                total_bill_label.configure(text="Total bill:", font=(font, 15, 'bold'))
                total_bill_label.place(x=95, y=20)

                total_bill_entry = Entry(mpesa_frame, bg='white')
                total_bill_entry.configure(font=(font, 14), justify=CENTER)
                total_bill_entry.insert(0, str(self.total_pay))
                total_bill_entry.configure(state='disabled', relief='solid')
                total_bill_entry.place(x=200, y=23, width=200, height=30)

                discount_label = Label(mpesa_frame)
                discount_label.configure(text="Discount given:", font=(font, 15, 'bold'))
                discount_label.place(x=40, y=60)

                discount_entry = Entry(mpesa_frame, bg='white')
                discount_entry.configure(font=(font, 14), justify=CENTER, relief='solid', textvariable=discount_value)
                discount_entry.place(x=200, y=63, width=200, height=30)
                discount_entry.focus_set()

                separate_label = Label(mpesa_frame)
                separate_label.configure(text="Amount Via Cash:", font=(font, 15, 'bold'))
                separate_label.place(x=20, y=100)

                separate_entry = Entry(mpesa_frame, bg='white')
                separate_entry.configure(font=(font, 14), justify=CENTER, relief='solid', textvariable=separate_value)
                separate_entry.place(x=200, y=103, width=200, height=30)

                amount_label = Label(mpesa_frame)
                amount_label.configure(text="Amount payable:", font=(font, 15, 'bold'))
                amount_label.place(x=30, y=140)

                amount_value = DoubleVar()

                amount_entry = Entry(mpesa_frame, bg='white', textvariable=amount_value)
                amount_entry.delete(0, END)
                amount_entry.insert(0, str(self.total_pay))
                amount_entry.configure(font=(font, 14), justify=CENTER, relief='solid', state='disabled')
                amount_entry.place(x=200, y=143, width=200, height=30)

                def amount_function(*args):
                    try:
                        if discount_value.get().strip() == "" and separate_value.get().strip() == "":
                            amount = self.total_pay
                            amount_entry.configure(state='normal')
                            amount_entry.delete(0, END)
                            amount_entry.insert(0, str(amount))
                            amount_entry.configure(state='disabled')

                        elif discount_value.get().strip() == "" and separate_value.get().strip() != "":
                            amount = self.total_pay - float(separate_value.get().strip())
                            amount_entry.configure(state='normal')
                            amount_entry.delete(0, END)
                            amount_entry.insert(0, str(amount))
                            amount_entry.configure(state='disabled')

                        elif discount_value.get() != "" and separate_value.get() != "":
                            if float(discount_value.get().strip()) < self.total_pay:
                                amount = self.total_pay - float(separate_value.get().strip()) - float(
                                    discount_value.get().strip())
                                amount_entry.configure(state='normal')
                                amount_entry.delete(0, END)
                                amount_entry.insert(0, str(amount))
                                amount_entry.configure(state='disabled')

                            else:
                                pass

                        else:
                            if float(discount_value.get().strip()) < self.total_pay:
                                amount = self.total_pay - float(discount_value.get().strip())
                                amount_entry.configure(state='normal')
                                amount_entry.delete(0, END)
                                amount_entry.insert(0, str(amount))
                                amount_entry.configure(state='disabled')

                            else:
                                pass

                    except ValueError:
                        pass

                discount_value.trace("w", amount_function)
                separate_value.trace("w", amount_function)

                def save_function():
                    if amount_value.get() > 0 and poss_debt.get() == 0:
                        try:
                            number_of_items = len(self.cart_table.get_children())
                            today = datetime.datetime.today()
                            current_time = today.strftime("%d/%B/%Y %H:%M")

                            if separate_value.get().strip() != "":
                                mode = "mpesa&cash"

                            else:
                                mode = "mpesa"

                            if discount_value.get().strip() == "":
                                discount = 0.0

                            else:
                                discount = float(discount_value.get().strip())

                            if separate_value.get().strip() == "":
                                pen_cash = 0.0

                            else:
                                pen_cash = float(separate_value.get().strip())

                            def collect_values(new_quantity, paper):
                                def collect_quantity(field, value):
                                    connection = connect(path_to_database)
                                    write = connection.cursor()
                                    lk_command = "SELECT quantity FROM {} WHERE {}='{}'".format("stock", field,
                                                                                                str(value))
                                    write.execute(lk_command)
                                    values = write.fetchall()
                                    connection.close()

                                    return values

                                old_quantity = collect_quantity("description", paper)
                                update_quantity = int(old_quantity[0][0]) - int(new_quantity)

                                if update_quantity > 0:
                                    conn = connect(path_to_database)
                                    writes = conn.cursor()
                                    lk_comm = "UPDATE {} SET {}='{}' WHERE description='{}'".format("stock", "quantity",
                                                                                                    update_quantity,
                                                                                                    paper)
                                    writes.execute(lk_comm)
                                    conn.commit()
                                    conn.close()

                                else:
                                    payment_window.destroy()
                                    messagebox.showwarning("Low quantity",
                                                           "Cannot update quantity for {} due to low quantity\n"
                                                           "Transaction not complete!".format(paper))
                                    raise StopIteration

                            products_in_cart = []
                            services_in_cart = []

                            for itm in self.cart_table.get_children():
                                cart_values = self.cart_table.item(itm)['values']
                                db_co = connect(path_to_database)
                                wri = db_co.cursor()
                                ll = "SELECT category FROM products WHERE description='{}'".format(cart_values[1])
                                wri.execute(ll)
                                r = wri.fetchall()
                                db_co.close()

                                if not r:
                                    services_in_cart.append(cart_values)

                                else:
                                    products_in_cart.append(cart_values)

                            for product in products_in_cart:
                                db_co = connect(path_to_database)
                                wri = db_co.cursor()
                                ll = "SELECT category FROM products WHERE description='{}'".format(product[1])
                                wri.execute(ll)
                                r = wri.fetchall()
                                db_co.close()

                                if r[0][0] != 'Printing':
                                    def collect_quantity(field, value):
                                        connection = connect(path_to_database)
                                        write = connection.cursor()
                                        lk_command = "SELECT quantity FROM {} WHERE {}='{}'".format("stock", field,
                                                                                                    str(value))
                                        write.execute(lk_command)
                                        values = write.fetchall()
                                        connection.close()

                                        return values

                                    old_quantity = collect_quantity("description", product[1])
                                    update_quantity = int(old_quantity[0][0]) - int(product[3])

                                    if update_quantity > 0:
                                        conn = connect(path_to_database)
                                        writes = conn.cursor()
                                        lk_comm = "UPDATE {} SET {}='{}' WHERE description='{}'".format("stock",
                                                                                                        "quantity",
                                                                                                        update_quantity,
                                                                                                        product[
                                                                                                            1])
                                        writes.execute(lk_comm)
                                        conn.commit()
                                        conn.close()

                                    else:
                                        payment_window.destroy()
                                        messagebox.showwarning("Low quantity",
                                                               "Cannot update quantity for {} due to low quantity\n"
                                                               "Transaction not complete!".format(product[1]))

                                else:
                                    if product[1].startswith("A4 Printing"):
                                        collect_values(product[3], "A4 Rim Papers")

                                    if product[1].startswith("A4 Copy"):
                                        collect_values(product[3], "A4 Rim Papers")

                                    if product[1].startswith("A3 Printing"):
                                        collect_values(product[3], "A3 Paper")

                                    if product[1].startswith("A3 Copy"):
                                        collect_values(product[3], "A3 Paper")

                                    if product[1].startswith("A4 Glossy"):
                                        collect_values(product[3], "Glossy Paper")

                                    if product[1].startswith("A4 Photo"):
                                        collect_values(product[3], "A4 Photo Paper")

                                    if product[1].startswith("A5 Photo"):
                                        collect_values(product[3], "A5 Photo Paper")

                                    if product[1].startswith("Passport"):
                                        collect_values(product[3], "Passport Paper")

                                    if product[1].startswith("A4 150 gsm"):
                                        collect_values(product[3], "A4 Art Paper 150 gsm")

                                    if product[1].startswith("A3 150 gsm"):
                                        collect_values(product[3], "A3 Art Paper 150 gsm")

                                    if product[1].startswith("A4 250/275/300 gsm"):
                                        collect_values(product[3], "A4 Art Paper 250/275/300 gsm")

                                    if product[1].startswith("A3 250/275/300 gsm"):
                                        collect_values(product[3], "A3 Art Paper 250/275/300 gsm")

                                conn = connect(path_to_database)
                                c = conn.cursor()
                                params2 = (self.new_transaction_number, current_time, product[1], product[2],
                                           product[3], product[4])
                                c.execute("INSERT INTO Sales VALUES (?, ?, ?, ?, ?, ?)", params2)
                                conn.commit()

                            for service in services_in_cart:
                                conn = connect(path_to_database)
                                c = conn.cursor()
                                params2 = (
                                    self.new_transaction_number, current_time, service[1], service[2],
                                    service[3], service[4])
                                c.execute("INSERT INTO Sales VALUES (?, ?, ?, ?, ?, ?)", params2)
                                conn.commit()

                            conn = connect(path_to_database)
                            c = conn.cursor()
                            params1 = (self.new_transaction_number, current_time, number_of_items, self.total_pay,
                                       amount_value.get(), discount, pen_cash, 0.0, mode)
                            c.execute("INSERT INTO Transactions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", params1)
                            conn.commit()
                            conn.close()

                            self.payment_label.configure(text="0.00")
                            self.total_pay = 0.0
                            payment_window.destroy()

                            for vals in self.cart_table.get_children():
                                self.cart_table.delete(vals)

                            self.new_transaction_function()

                        except ValueError:
                            pass

                        except StopIteration:
                            pass

                        except IndexError:
                            pass

                    else:
                        if poss_debt.get() == 1:
                            debt_window = Toplevel(payment_window)
                            debt_window.geometry("400x400")
                            debt_window.title("Debt Details")
                            center(debt_window)
                            debt_window.resizable(False, False)

                            first_name_value = StringVar()
                            second_name_value = StringVar()
                            contact_number_value = StringVar()

                            first_name_label = Label(debt_window)
                            first_name_label.configure(text="First Name*:", font=(font, 13, "bold"))
                            first_name_label.place(x=30, y=30)

                            first_name_entry = Entry(debt_window, textvariable=first_name_value)
                            first_name_entry.configure(font=(font, 13), relief="solid", justify=CENTER)
                            first_name_entry.place(x=160, y=30)
                            first_name_entry.focus_set()

                            second_name_label = Label(debt_window)
                            second_name_label.configure(text="Second Name:", font=(font, 13, "bold"))
                            second_name_label.place(x=30, y=80)

                            second_name_entry = Entry(debt_window, textvariable=second_name_value)
                            second_name_entry.configure(font=(font, 13), relief="solid", justify=CENTER)
                            second_name_entry.place(x=160, y=80)

                            contact_label = Label(debt_window)
                            contact_label.configure(text="Contact*:", font=(font, 13, "bold"))
                            contact_label.place(x=30, y=130)

                            contact_entry = Entry(debt_window, textvariable=contact_number_value)
                            contact_entry.configure(font=(font, 13), relief="solid", justify=CENTER)
                            contact_entry.place(x=160, y=130)

                            debt_discount = StringVar()
                            discount_label = Label(debt_window)
                            discount_label.configure(text="Discount:", font=(font, 13, "bold"))
                            discount_label.place(x=30, y=180)

                            discount_entry = Entry(debt_window, textvariable=debt_discount)
                            discount_entry.delete(0, END)
                            discount_entry.insert(0, discount_value.get().strip())
                            discount_entry.configure(font=(font, 13), relief="solid", justify=CENTER, state='disabled')
                            discount_entry.place(x=160, y=180)

                            debt_label = Label(debt_window)
                            debt_label.configure(text="Debt Amount:", font=(font, 13, "bold"))
                            debt_label.place(x=30, y=230)
                            debt_in = StringVar()

                            debt_entry = Entry(debt_window, textvariable=debt_in)
                            debt_entry.delete(0, END)
                            debt_entry.insert(0, str(amount_value.get()))
                            debt_entry.configure(font=(font, 13), relief="solid", justify=CENTER, state='disabled')
                            debt_entry.place(x=160, y=230)
                            mpesa_amount = StringVar()

                            mpesa_label = Label(debt_window)
                            mpesa_label.configure(text="Amount Paid*:", font=(font, 13, "bold"))
                            mpesa_label.place(x=30, y=280)

                            mpesa_entry = Entry(debt_window, textvariable=mpesa_amount)
                            mpesa_entry.configure(font=(font, 13), relief="solid", justify=CENTER)
                            mpesa_entry.place(x=160, y=280)
                            self.update_sales()

                            def calculation(*args):
                                try:
                                    we = amount_value.get()
                                    me = mpesa_amount.get().strip()

                                    if me != "":
                                        if float(me) < float(we):
                                            new_det = float(we) - float(me)
                                            debt_entry.configure(state='normal')
                                            debt_entry.delete(0, END)
                                            debt_entry.insert(0, str(new_det))
                                            debt_entry.configure(state='disabled')

                                        else:
                                            pass

                                    else:
                                        debt_entry.configure(state='normal')
                                        debt_entry.delete(0, END)
                                        debt_entry.insert(0, str(amount_value.get()))
                                        debt_entry.configure(state='disabled')

                                except TclError:
                                    pass

                                except ValueError:
                                    pass

                            mpesa_amount.trace("w", calculation)

                            def save_debt():
                                try:
                                    if first_name_value.get().strip() != "" and contact_number_value.get().strip() != "" \
                                            and len(contact_number_value.get().strip()) > 3 and \
                                            len(first_name_value.get().strip()) >= 3 and mpesa_amount.get().strip() != "" \
                                            and float(mpesa_amount.get().strip()) < amount_value.get():
                                        try:
                                            if separate_value.get().strip() == "":
                                                flo = 0

                                            else:
                                                flo = float(separate_value.get().strip())

                                            pen_cash = float(mpesa_amount.get().strip()) + flo
                                            number_of_items = len(self.cart_table.get_children())
                                            today = datetime.datetime.today()
                                            current_time = today.strftime("%d/%B/%Y %H:%M")

                                            if debt_discount.get().strip() == "":
                                                discount = 0.0

                                            else:
                                                discount = float(debt_discount.get().strip())

                                            if separate_value.get().strip() == "":
                                                cash_amnt = 0.0

                                            else:
                                                cash_amnt = float(separate_value.get().strip())

                                            def collect_values(new_quantity, paper):
                                                def collect_quantity(field, value):
                                                    connection = connect(path_to_database)
                                                    write = connection.cursor()
                                                    lk_command = "SELECT quantity FROM {} WHERE {}='{}'".format("stock",
                                                                                                                field,
                                                                                                                str(value))
                                                    write.execute(lk_command)
                                                    values = write.fetchall()
                                                    connection.close()

                                                    return values

                                                old_quantity = collect_quantity("description", paper)
                                                update_quantity = int(old_quantity[0][0]) - int(new_quantity)

                                                if update_quantity > 0:
                                                    conn = connect(path_to_database)
                                                    writes = conn.cursor()
                                                    lk_comm = "UPDATE {} SET {}='{}' WHERE description='{}'".format(
                                                        "stock",
                                                        "quantity",
                                                        update_quantity,
                                                        paper)
                                                    writes.execute(lk_comm)
                                                    conn.commit()
                                                    conn.close()

                                                else:
                                                    payment_window.destroy()
                                                    messagebox.showwarning("Low quantity",
                                                                           "Cannot update quantity for {} due to low quantity\n"
                                                                           "Transaction not complete!".format(paper))
                                                    raise StopIteration

                                            products_in_cart = []
                                            services_in_cart = []

                                            for itm in self.cart_table.get_children():
                                                cart_values = self.cart_table.item(itm)['values']
                                                db_co = connect(path_to_database)
                                                wri = db_co.cursor()
                                                ll = "SELECT category FROM products WHERE description='{}'".format(
                                                    cart_values[1])
                                                wri.execute(ll)
                                                r = wri.fetchall()
                                                db_co.close()

                                                if not r:
                                                    services_in_cart.append(cart_values)

                                                else:
                                                    products_in_cart.append(cart_values)

                                            for product in products_in_cart:
                                                db_co = connect(path_to_database)
                                                wri = db_co.cursor()
                                                ll = "SELECT category FROM products WHERE description='{}'".format(
                                                    product[1])
                                                wri.execute(ll)
                                                r = wri.fetchall()
                                                db_co.close()

                                                if r[0][0] != 'Printing':
                                                    def collect_quantity(field, value):
                                                        connection = connect(path_to_database)
                                                        write = connection.cursor()
                                                        lk_command = "SELECT quantity FROM {} WHERE {}='{}'".format(
                                                            "stock", field,
                                                            str(value))
                                                        write.execute(lk_command)
                                                        values = write.fetchall()
                                                        connection.close()

                                                        return values

                                                    old_quantity = collect_quantity("description", product[1])
                                                    update_quantity = int(old_quantity[0][0]) - int(product[3])

                                                    if update_quantity > 0:
                                                        conn = connect(path_to_database)
                                                        writes = conn.cursor()
                                                        lk_comm = "UPDATE {} SET {}='{}' WHERE description='{}'".format(
                                                            "stock",
                                                            "quantity",
                                                            update_quantity,
                                                            product[
                                                                1])
                                                        writes.execute(lk_comm)
                                                        conn.commit()
                                                        conn.close()

                                                    else:
                                                        payment_window.destroy()
                                                        messagebox.showwarning("Low quantity",
                                                                               "Cannot update quantity for {} due to low quantity\n"
                                                                               "Transaction not complete!".format(
                                                                                   product[1]))

                                                else:
                                                    if product[1].startswith("A4 Printing"):
                                                        collect_values(product[3], "A4 Rim Papers")

                                                    if product[1].startswith("A4 Copy"):
                                                        collect_values(product[3], "A4 Rim Papers")

                                                    if product[1].startswith("A3 Printing"):
                                                        collect_values(product[3], "A3 Paper")

                                                    if product[1].startswith("A3 Copy"):
                                                        collect_values(product[3], "A3 Paper")

                                                    if product[1].startswith("A4 Glossy"):
                                                        collect_values(product[3], "Glossy Paper")

                                                    if product[1].startswith("A4 Photo"):
                                                        collect_values(product[3], "A4 Photo Paper")

                                                    if product[1].startswith("A5 Photo"):
                                                        collect_values(product[3], "A5 Photo Paper")

                                                    if product[1].startswith("Passport"):
                                                        collect_values(product[3], "Passport Paper")

                                                    if product[1].startswith("A4 150 gsm"):
                                                        collect_values(product[3], "A4 Art Paper 150 gsm")

                                                    if product[1].startswith("A3 150 gsm"):
                                                        collect_values(product[3], "A3 Art Paper 150 gsm")

                                                    if product[1].startswith("A4 250/275/300 gsm"):
                                                        collect_values(product[3], "A4 Art Paper 250/275/300 gsm")

                                                    if product[1].startswith("A3 250/275/300 gsm"):
                                                        collect_values(product[3], "A3 Art Paper 250/275/300 gsm")

                                                conn = connect(path_to_database)
                                                c = conn.cursor()
                                                params2 = (
                                                    self.new_transaction_number, current_time, product[1], product[2],
                                                    product[3], product[4])
                                                c.execute("INSERT INTO Sales VALUES (?, ?, ?, ?, ?, ?)", params2)
                                                conn.commit()

                                            for service in services_in_cart:
                                                conn = connect(path_to_database)
                                                c = conn.cursor()
                                                params2 = (
                                                    self.new_transaction_number, current_time, service[1], service[2],
                                                    service[3], service[4])
                                                c.execute("INSERT INTO Sales VALUES (?, ?, ?, ?, ?, ?)", params2)
                                                conn.commit()

                                            conn = connect(path_to_database)
                                            c = conn.cursor()
                                            params1 = (
                                                self.new_transaction_number, current_time, number_of_items,
                                                self.total_pay,
                                                pen_cash, discount, cash_amnt, float(debt_in.get()), "mpesa")
                                            c.execute("INSERT INTO Transactions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                                      params1)
                                            conn.commit()
                                            params3 = (self.new_transaction_number, first_name_value.get().strip(),
                                                       second_name_value.get().strip(),
                                                       contact_number_value.get().strip(), float(debt_in.get()),
                                                       current_time)
                                            c.execute("INSERT INTO debts VALUES (?, ?, ?, ?, ?, ?)", params3)
                                            conn.commit()
                                            conn.close()

                                            self.payment_label.configure(text="0.00")
                                            self.total_pay = 0.0
                                            payment_window.destroy()

                                            for vals in self.cart_table.get_children():
                                                self.cart_table.delete(vals)

                                            self.new_transaction_function()

                                        except ValueError:
                                            pass

                                        except StopIteration:
                                            pass

                                    else:
                                        debt_window.destroy()
                                        messagebox.showwarning("Form Error", "Fill all fields with *\n"
                                                                             "Debt amount should be greater than 0\n"
                                                                             "Amount paid should be less than payable")
                                except ValueError:
                                    debt_window.destroy()
                                    messagebox.showwarning("Form Error", "Contact number should be numbers only\n"
                                                                         "Amount Paid should be numbers only")

                            save_button = Button(debt_window, bg="red", fg="white")
                            save_button.configure(relief='solid', text="SAVE RECORD", font=(font, 14),
                                                  command=save_debt)
                            save_button.place(x=140, y=340)

                        else:
                            payment_window.destroy()
                            messagebox.showwarning("Amount Warning!", "Please make sure there are items in cart or\n"
                                                                      "Make sure the discount and pending cash should not be greater than Total bill")

                    self.update_sales()

                save_record = Button(mpesa_frame, bg="green", fg="white")
                save_record.configure(relief='solid', text="SAVE RECORD", font=(font, 14), command=save_function)
                save_record.place(x=260, y=200)

                debt_included = Checkbutton(mpesa_frame)
                debt_included.configure(text="Debt included?", variable=poss_debt)
                debt_included.place(x=30, y=200)

            except TclError:
                pass

        def cash_sub_frame():
            cash_frame = Frame(payment_window, width=500, height=300)
            cash_frame.configure(highlightthickness=3, highlightbackground='blue')
            cash_frame.place(x=50, y=80)

            total_bill_label = Label(cash_frame)
            total_bill_label.configure(text="Total bill:", font=(font, 15, 'bold'))
            total_bill_label.place(x=90, y=20)

            total_bill_entry = Entry(cash_frame, bg='white')
            total_bill_entry.configure(font=(font, 14), justify=CENTER)
            total_bill_entry.insert(0, str(self.total_pay))
            total_bill_entry.configure(state='disabled', relief='solid')
            total_bill_entry.place(x=200, y=23, width=200, height=30)

            cash_discount = StringVar()

            discount_label = Label(cash_frame)
            discount_label.configure(text="Discount given:", font=(font, 15, 'bold'))
            discount_label.place(x=30, y=60)

            discount_entry = Entry(cash_frame, bg='white', textvariable=cash_discount)
            discount_entry.configure(font=(font, 14), justify=CENTER, relief='solid')
            discount_entry.place(x=200, y=63, width=200, height=30)

            paid_amount = StringVar()

            separate_label = Label(cash_frame)
            separate_label.configure(text="Amount Paid:", font=(font, 15, 'bold'))
            separate_label.place(x=45, y=100)

            separate_entry = Entry(cash_frame, bg='white', textvariable=paid_amount)
            separate_entry.configure(font=(font, 14), justify=CENTER, relief='solid')
            separate_entry.delete(0, END)
            separate_entry.place(x=200, y=103, width=200, height=30)
            separate_entry.focus_set()

            amount_label = Label(cash_frame)
            amount_label.configure(text="Balance:", font=(font, 15, 'bold'))
            amount_label.place(x=95, y=140)

            cash_amount_value = DoubleVar()

            amount_entry = Entry(cash_frame, bg='white', textvariable=cash_amount_value)
            amount_entry.delete(0, END)
            amount_entry.insert(0, str(self.total_pay))
            amount_entry.configure(font=(font, 14), justify=CENTER, relief='solid', state='disabled')
            amount_entry.place(x=200, y=143, width=200, height=30)

            debt_included = Checkbutton(cash_frame)
            debt_included.configure(text="Debt included?", variable=debt_value)
            debt_included.place(x=30, y=180)

            def amount_function(*args):
                try:
                    if cash_discount.get().strip() == "" and paid_amount.get().strip() == "":
                        amount = self.total_pay
                        amount_entry.configure(state='normal')
                        amount_entry.delete(0, END)
                        amount_entry.insert(0, str(amount))
                        amount_entry.configure(state='disabled')

                    elif cash_discount.get().strip() == "" and paid_amount.get().strip() != "":
                        amount = float(paid_amount.get().strip()) - self.total_pay
                        amount_entry.configure(state='normal')
                        amount_entry.delete(0, END)
                        amount_entry.insert(0, str(amount))
                        amount_entry.configure(state='disabled')

                    elif cash_discount.get().strip() != "" and paid_amount.get().strip() != "":
                        if float(cash_discount.get().strip()) < self.total_pay:
                            amount = float(paid_amount.get().strip()) - (
                                        self.total_pay - float(cash_discount.get().strip()))
                            amount_entry.configure(state='normal')
                            amount_entry.delete(0, END)
                            amount_entry.insert(0, str(amount))
                            amount_entry.configure(state='disabled')

                        else:
                            pass

                    elif cash_discount.get().strip() != "" and paid_amount.get().strip() == "":
                        if float(cash_discount.get().strip()) < self.total_pay:
                            amount = self.total_pay - float(cash_discount.get().strip())
                            amount_entry.configure(state='normal')
                            amount_entry.delete(0, END)
                            amount_entry.insert(0, str(amount))
                            amount_entry.configure(state='disabled')

                        else:
                            pass

                    else:
                        if float(cash_discount.get().strip()) < float(self.total_pay):
                            amount = self.total_pay - float(paid_amount.get().strip())
                            amount_entry.configure(state='normal')
                            amount_entry.delete(0, END)
                            amount_entry.insert(0, str(amount))
                            amount_entry.configure(state='disabled')

                        else:
                            pass

                except ValueError:
                    pass

            cash_discount.trace("w", amount_function)
            paid_amount.trace("w", amount_function)

            def save_function():
                try:
                    if cash_amount_value.get() >= 0 and float(paid_amount.get().strip()) > 0 and debt_value.get() == 0:
                        try:
                            pen_cash = float(paid_amount.get().strip())
                            number_of_items = len(self.cart_table.get_children())
                            today = datetime.datetime.today()
                            current_time = today.strftime("%d/%B/%Y %H:%M")

                            if cash_discount.get().strip() == "":
                                discount = 0.0

                            else:
                                discount = float(cash_discount.get().strip())

                            def collect_values(new_quantity, paper):
                                def collect_quantity(field, value):
                                    connection = connect(path_to_database)
                                    write = connection.cursor()
                                    lk_command = "SELECT quantity FROM {} WHERE {}='{}'".format("stock", field,
                                                                                                str(value))
                                    write.execute(lk_command)
                                    values = write.fetchall()
                                    connection.close()

                                    return values

                                old_quantity = collect_quantity("description", paper)
                                update_quantity = int(old_quantity[0][0]) - int(new_quantity)

                                if update_quantity > 0:
                                    conn = connect(path_to_database)
                                    writes = conn.cursor()
                                    lk_comm = "UPDATE {} SET {}='{}' WHERE description='{}'".format("stock", "quantity",
                                                                                                    update_quantity,
                                                                                                    paper)
                                    writes.execute(lk_comm)
                                    conn.commit()
                                    conn.close()

                                else:
                                    payment_window.destroy()
                                    messagebox.showwarning("Low quantity",
                                                           "Cannot update quantity for {} due to low quantity\n"
                                                           "Transaction not complete!".format(paper))
                                    raise StopIteration

                            products_in_cart = []
                            services_in_cart = []

                            for itm in self.cart_table.get_children():
                                cart_values = self.cart_table.item(itm)['values']
                                db_co = connect(path_to_database)
                                wri = db_co.cursor()
                                ll = "SELECT category FROM products WHERE description='{}'".format(cart_values[1])
                                wri.execute(ll)
                                r = wri.fetchall()
                                db_co.close()

                                if not r:
                                    services_in_cart.append(cart_values)

                                else:
                                    products_in_cart.append(cart_values)

                            for product in products_in_cart:
                                db_co = connect(path_to_database)
                                wri = db_co.cursor()
                                ll = "SELECT category FROM products WHERE description='{}'".format(product[1])
                                wri.execute(ll)
                                r = wri.fetchall()
                                db_co.close()

                                if r[0][0] != 'Printing':
                                    def collect_quantity(field, value):
                                        connection = connect(path_to_database)
                                        write = connection.cursor()
                                        lk_command = "SELECT quantity FROM {} WHERE {}='{}'".format("stock", field,
                                                                                                    str(value))
                                        write.execute(lk_command)
                                        values = write.fetchall()
                                        connection.close()

                                        return values

                                    old_quantity = collect_quantity("description", product[1])
                                    update_quantity = int(old_quantity[0][0]) - int(product[3])

                                    if update_quantity > 0:
                                        conn = connect(path_to_database)
                                        writes = conn.cursor()
                                        lk_comm = "UPDATE {} SET {}='{}' WHERE description='{}'".format("stock",
                                                                                                        "quantity",
                                                                                                        update_quantity,
                                                                                                        product[
                                                                                                            1])
                                        writes.execute(lk_comm)
                                        conn.commit()
                                        conn.close()

                                    else:
                                        payment_window.destroy()
                                        messagebox.showwarning("Low quantity",
                                                               "Cannot update quantity for {} due to low quantity\n"
                                                               "Transaction not complete!".format(product[1]))

                                else:
                                    if product[1].startswith("A4 Printing"):
                                        collect_values(product[3], "A4 Rim Papers")

                                    if product[1].startswith("A4 Copy"):
                                        collect_values(product[3], "A4 Rim Papers")

                                    if product[1].startswith("A3 Printing"):
                                        collect_values(product[3], "A3 Paper")

                                    if product[1].startswith("A3 Copy"):
                                        collect_values(product[3], "A3 Paper")

                                    if product[1].startswith("A4 Glossy"):
                                        collect_values(product[3], "Glossy Paper")

                                    if product[1].startswith("A4 Photo"):
                                        collect_values(product[3], "A4 Photo Paper")

                                    if product[1].startswith("A5 Photo"):
                                        collect_values(product[3], "A5 Photo Paper")

                                    if product[1].startswith("Passport"):
                                        collect_values(product[3], "Passport Paper")

                                    if product[1].startswith("A4 150 gsm"):
                                        collect_values(product[3], "A4 Art Paper 150 gsm")

                                    if product[1].startswith("A3 150 gsm"):
                                        collect_values(product[3], "A3 Art Paper 150 gsm")

                                    if product[1].startswith("A4 250/275/300 gsm"):
                                        collect_values(product[3], "A4 Art Paper 250/275/300 gsm")

                                    if product[1].startswith("A3 250/275/300 gsm"):
                                        collect_values(product[3], "A3 Art Paper 250/275/300 gsm")

                                conn = connect(path_to_database)
                                c = conn.cursor()
                                params2 = (self.new_transaction_number, current_time, product[1], product[2],
                                           product[3], product[4])
                                c.execute("INSERT INTO Sales VALUES (?, ?, ?, ?, ?, ?)", params2)
                                conn.commit()

                            for service in services_in_cart:
                                conn = connect(path_to_database)
                                c = conn.cursor()
                                params2 = (
                                    self.new_transaction_number, current_time, service[1], service[2],
                                    service[3], service[4])
                                c.execute("INSERT INTO Sales VALUES (?, ?, ?, ?, ?, ?)", params2)
                                conn.commit()

                            conn = connect(path_to_database)
                            c = conn.cursor()
                            params1 = (self.new_transaction_number, current_time, number_of_items, self.total_pay,
                                       pen_cash, discount, cash_amount_value.get(), 0.0, "cash")
                            c.execute("INSERT INTO Transactions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", params1)
                            conn.commit()

                            self.payment_label.configure(text="0.00")
                            self.total_pay = 0.0
                            payment_window.destroy()

                            for vals in self.cart_table.get_children():
                                self.cart_table.delete(vals)

                            self.new_transaction_function()

                        except ValueError:
                            pass

                        except StopIteration:
                            pass

                    else:
                        if debt_value.get() == 1:
                            if cash_amount_value.get() < 0:
                                debt_window = Toplevel(payment_window)
                                debt_window.geometry("400x300")
                                debt_window.title("Debt Details")
                                center(debt_window)
                                debt_window.resizable(False, False)

                                first_name_value = StringVar()
                                second_name_value = StringVar()
                                contact_number_value = StringVar()

                                first_name_label = Label(debt_window)
                                first_name_label.configure(text="First Name*:", font=(font, 13, "bold"))
                                first_name_label.place(x=30, y=30)

                                first_name_entry = Entry(debt_window, textvariable=first_name_value)
                                first_name_entry.configure(font=(font, 13), relief="solid", justify=CENTER)
                                first_name_entry.place(x=160, y=30)
                                first_name_entry.focus_set()

                                second_name_label = Label(debt_window)
                                second_name_label.configure(text="Second Name:", font=(font, 13, "bold"))
                                second_name_label.place(x=30, y=80)

                                second_name_entry = Entry(debt_window, textvariable=second_name_value)
                                second_name_entry.configure(font=(font, 13), relief="solid", justify=CENTER)
                                second_name_entry.place(x=160, y=80)

                                contact_label = Label(debt_window)
                                contact_label.configure(text="Contact*:", font=(font, 13, "bold"))
                                contact_label.place(x=30, y=130)

                                contact_entry = Entry(debt_window, textvariable=contact_number_value)
                                contact_entry.configure(font=(font, 13), relief="solid", justify=CENTER)
                                contact_entry.place(x=160, y=130)

                                debt_label = Label(debt_window)
                                debt_label.configure(text="Debt Amount:", font=(font, 13, "bold"))
                                debt_label.place(x=30, y=180)
                                debt_amount = str(cash_amount_value.get()).replace("-", "").strip()

                                debt_entry = Entry(debt_window)
                                debt_entry.delete(0, END)
                                debt_entry.insert(0, debt_amount)
                                debt_entry.configure(font=(font, 13), relief="solid", justify=CENTER, state='disabled')
                                debt_entry.place(x=160, y=180)

                                def save_debt():
                                    if first_name_value.get().strip() != "" and contact_number_value.get().strip() != "" and len(
                                            contact_number_value.get().strip()) > 3 and len(
                                            first_name_value.get().strip()) >= 2:
                                        try:
                                            pen_cash = float(paid_amount.get().strip())
                                            number_of_items = len(self.cart_table.get_children())
                                            today = datetime.datetime.today()
                                            current_time = today.strftime("%d/%B/%Y %H:%M")

                                            if cash_discount.get().strip() == "":
                                                discount = 0.0

                                            else:
                                                discount = float(cash_discount.get().strip())

                                            def collect_values(new_quantity, paper):
                                                def collect_quantity(field, value):
                                                    connection = connect(path_to_database)
                                                    write = connection.cursor()
                                                    lk_command = "SELECT quantity FROM {} WHERE {}='{}'".format("stock",
                                                                                                                field,
                                                                                                                str(value))
                                                    write.execute(lk_command)
                                                    values = write.fetchall()
                                                    connection.close()

                                                    return values

                                                old_quantity = collect_quantity("description", paper)
                                                update_quantity = int(old_quantity[0][0]) - int(new_quantity)

                                                if update_quantity > 0:
                                                    conn = connect(path_to_database)
                                                    writes = conn.cursor()
                                                    lk_comm = "UPDATE {} SET {}='{}' WHERE description='{}'".format(
                                                        "stock",
                                                        "quantity",
                                                        update_quantity,
                                                        paper)
                                                    writes.execute(lk_comm)
                                                    conn.commit()
                                                    conn.close()

                                                else:
                                                    payment_window.destroy()
                                                    messagebox.showwarning("Low quantity",
                                                                           "Cannot update quantity for {} due to low quantity\n"
                                                                           "Transaction not complete!".format(paper))
                                                    raise StopIteration

                                            products_in_cart = []
                                            services_in_cart = []

                                            for itm in self.cart_table.get_children():
                                                cart_values = self.cart_table.item(itm)['values']
                                                db_co = connect(path_to_database)
                                                wri = db_co.cursor()
                                                ll = "SELECT category FROM products WHERE description='{}'".format(
                                                    cart_values[1])
                                                wri.execute(ll)
                                                r = wri.fetchall()
                                                db_co.close()

                                                if not r:
                                                    services_in_cart.append(cart_values)

                                                else:
                                                    products_in_cart.append(cart_values)

                                            for product in products_in_cart:
                                                db_co = connect(path_to_database)
                                                wri = db_co.cursor()
                                                ll = "SELECT category FROM products WHERE description='{}'".format(
                                                    product[1])
                                                wri.execute(ll)
                                                r = wri.fetchall()
                                                db_co.close()

                                                if r[0][0] != 'Printing':
                                                    def collect_quantity(field, value):
                                                        connection = connect(path_to_database)
                                                        write = connection.cursor()
                                                        lk_command = "SELECT quantity FROM {} WHERE {}='{}'".format(
                                                            "stock", field,
                                                            str(value))
                                                        write.execute(lk_command)
                                                        values = write.fetchall()
                                                        connection.close()

                                                        return values

                                                    old_quantity = collect_quantity("description", product[1])
                                                    update_quantity = int(old_quantity[0][0]) - int(product[3])

                                                    if update_quantity > 0:
                                                        conn = connect(path_to_database)
                                                        writes = conn.cursor()
                                                        lk_comm = "UPDATE {} SET {}='{}' WHERE description='{}'".format(
                                                            "stock",
                                                            "quantity",
                                                            update_quantity,
                                                            product[
                                                                1])
                                                        writes.execute(lk_comm)
                                                        conn.commit()
                                                        conn.close()

                                                    else:
                                                        payment_window.destroy()
                                                        messagebox.showwarning("Low quantity",
                                                                               "Cannot update quantity for {} due to low quantity\n"
                                                                               "Transaction not complete!".format(
                                                                                   product[1]))

                                                else:
                                                    if product[1].startswith("A4 Printing"):
                                                        collect_values(product[3], "A4 Rim Papers")

                                                    if product[1].startswith("A4 Copy"):
                                                        collect_values(product[3], "A4 Rim Papers")

                                                    if product[1].startswith("A3 Printing"):
                                                        collect_values(product[3], "A3 Paper")

                                                    if product[1].startswith("A3 Copy"):
                                                        collect_values(product[3], "A3 Paper")

                                                    if product[1].startswith("A4 Glossy"):
                                                        collect_values(product[3], "Glossy Paper")

                                                    if product[1].startswith("A4 Photo"):
                                                        collect_values(product[3], "A4 Photo Paper")

                                                    if product[1].startswith("A5 Photo"):
                                                        collect_values(product[3], "A5 Photo Paper")

                                                    if product[1].startswith("Passport"):
                                                        collect_values(product[3], "Passport Paper")

                                                    if product[1].startswith("A4 150 gsm"):
                                                        collect_values(product[3], "A4 Art Paper 150 gsm")

                                                    if product[1].startswith("A3 150 gsm"):
                                                        collect_values(product[3], "A3 Art Paper 150 gsm")

                                                    if product[1].startswith("A4 250/275/300 gsm"):
                                                        collect_values(product[3], "A4 Art Paper 250/275/300 gsm")

                                                    if product[1].startswith("A3 250/275/300 gsm"):
                                                        collect_values(product[3], "A3 Art Paper 250/275/300 gsm")

                                                conn = connect(path_to_database)
                                                c = conn.cursor()
                                                params2 = (
                                                    self.new_transaction_number, current_time, product[1], product[2],
                                                    product[3], product[4])
                                                c.execute("INSERT INTO Sales VALUES (?, ?, ?, ?, ?, ?)", params2)
                                                conn.commit()

                                            for service in services_in_cart:
                                                conn = connect(path_to_database)
                                                c = conn.cursor()
                                                params2 = (
                                                    self.new_transaction_number, current_time, service[1], service[2],
                                                    service[3], service[4])
                                                c.execute("INSERT INTO Sales VALUES (?, ?, ?, ?, ?, ?)", params2)
                                                conn.commit()

                                            conn = connect(path_to_database)
                                            c = conn.cursor()
                                            params1 = (
                                                self.new_transaction_number, current_time, number_of_items,
                                                self.total_pay,
                                                pen_cash, discount, cash_amount_value.get(), debt_amount, "cash")
                                            c.execute("INSERT INTO Transactions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                                      params1)
                                            conn.commit()
                                            params3 = (self.new_transaction_number, first_name_value.get().strip(),
                                                       second_name_value.get().strip(),
                                                       contact_number_value.get().strip(), debt_amount, current_time)
                                            c.execute("INSERT INTO debts VALUES (?, ?, ?, ?, ?, ?)", params3)
                                            conn.commit()
                                            conn.close()

                                            self.payment_label.configure(text="0.00")
                                            self.total_pay = 0.0
                                            payment_window.destroy()

                                            for vals in self.cart_table.get_children():
                                                self.cart_table.delete(vals)

                                            self.new_transaction_function()

                                        except ValueError:
                                            pass

                                        except StopIteration:
                                            pass

                                    else:
                                        messagebox.showwarning("Form Error", "Fill all fields with *")

                                save_button = Button(debt_window, bg="red", fg="white")
                                save_button.configure(relief='solid', text="SAVE RECORD", font=(font, 14),
                                                      command=save_debt)
                                save_button.place(x=140, y=240)

                            else:
                                messagebox.showwarning("Debt Error", "Un-check the debt included box")

                        else:
                            payment_window.destroy()
                            messagebox.showwarning("Amount Warning!", "Please make sure there are items in cart or\n"
                                                                      "Make sure to enter {Paid Amount} section in the form")

                except ValueError:
                    payment_window.destroy()
                    messagebox.showwarning("Amount Warning!", "Please make sure there are items in cart or\n"
                                                              "Make sure to enter {Paid Amount} section in the form")

                self.update_sales()

            save_record = Button(cash_frame, bg="blue", fg="white")
            save_record.configure(relief='solid', text="SAVE RECORD", font=(font, 14), command=save_function)
            save_record.place(x=260, y=200)
            self.update_sales()

        def debt_sub_frame():
            debt_window = Toplevel(payment_window)
            debt_window.geometry("400x350")
            debt_window.title("Debt Details")
            center(debt_window)
            debt_window.resizable(False, False)

            first_name_value = StringVar()
            second_name_value = StringVar()
            contact_number_value = StringVar()

            first_name_label = Label(debt_window)
            first_name_label.configure(text="First Name*:", font=(font, 13, "bold"))
            first_name_label.place(x=30, y=30)

            first_name_entry = Entry(debt_window, textvariable=first_name_value)
            first_name_entry.configure(font=(font, 13), relief="solid", justify=CENTER)
            first_name_entry.place(x=160, y=30)
            first_name_entry.focus_set()

            second_name_label = Label(debt_window)
            second_name_label.configure(text="Second Name:", font=(font, 13, "bold"))
            second_name_label.place(x=30, y=80)

            second_name_entry = Entry(debt_window, textvariable=second_name_value)
            second_name_entry.configure(font=(font, 13), relief="solid", justify=CENTER)
            second_name_entry.place(x=160, y=80)

            contact_label = Label(debt_window)
            contact_label.configure(text="Contact*:", font=(font, 13, "bold"))
            contact_label.place(x=30, y=130)

            contact_entry = Entry(debt_window, textvariable=contact_number_value)
            contact_entry.configure(font=(font, 13), relief="solid", justify=CENTER)
            contact_entry.place(x=160, y=130)

            debt_discount = StringVar()
            discount_label = Label(debt_window)
            discount_label.configure(text="Discount:", font=(font, 13, "bold"))
            discount_label.place(x=30, y=180)

            discount_entry = Entry(debt_window, textvariable=debt_discount)
            discount_entry.configure(font=(font, 13), relief="solid", justify=CENTER)
            discount_entry.place(x=160, y=180)

            debt_label = Label(debt_window)
            debt_label.configure(text="Debt Amount:", font=(font, 13, "bold"))
            debt_label.place(x=30, y=230)
            debt_amount = str(self.total_pay)
            debt_in = StringVar()

            debt_entry = Entry(debt_window, textvariable=debt_in)
            debt_entry.delete(0, END)
            debt_entry.insert(0, debt_amount)
            debt_entry.configure(font=(font, 13), relief="solid", justify=CENTER, state='disabled')
            debt_entry.place(x=160, y=230)

            def debts(*args):
                debt_on_discount = debt_discount.get().strip()
                try:
                    if float(debt_on_discount) < self.total_pay:
                        new_debt = self.total_pay - float(debt_on_discount)
                        debt_entry.configure(state='normal')
                        debt_entry.delete(0, END)
                        debt_entry.insert(0, str(new_debt))
                        debt_entry.configure(state='disabled')

                    else:
                        pass

                except ValueError:
                    pass

            debt_discount.trace("w", debts)

            def save_function():
                try:
                    if self.total_pay > 0 and first_name_value.get().strip() != "" and \
                            contact_number_value.get().strip() != "" and \
                            len(contact_number_value.get().strip()) > 3 and len(first_name_value.get().strip()) >= 2:
                        try:
                            pen_cash = 0
                            number_of_items = len(self.cart_table.get_children())
                            today = datetime.datetime.today()
                            current_time = today.strftime("%d/%B/%Y %H:%M")

                            if debt_discount.get().strip() == "":
                                discount = 0.0

                            else:
                                discount = float(debt_discount.get().strip())

                            def collect_values(new_quantity, paper):
                                def collect_quantity(field, value):
                                    connection = connect(path_to_database)
                                    write = connection.cursor()
                                    lk_command = "SELECT quantity FROM {} WHERE {}='{}'".format("stock", field,
                                                                                                str(value))
                                    write.execute(lk_command)
                                    values = write.fetchall()
                                    connection.close()

                                    return values

                                old_quantity = collect_quantity("description", paper)
                                update_quantity = int(old_quantity[0][0]) - int(new_quantity)

                                if update_quantity > 0:
                                    conn = connect(path_to_database)
                                    writes = conn.cursor()
                                    lk_comm = "UPDATE {} SET {}='{}' WHERE description='{}'".format("stock", "quantity",
                                                                                                    update_quantity,
                                                                                                    paper)
                                    writes.execute(lk_comm)
                                    conn.commit()
                                    conn.close()

                                else:
                                    payment_window.destroy()
                                    messagebox.showwarning("Low quantity",
                                                           "Cannot update quantity for {} due to low quantity\n"
                                                           "Transaction not complete!".format(paper))
                                    raise StopIteration

                            products_in_cart = []
                            services_in_cart = []

                            for itm in self.cart_table.get_children():
                                cart_values = self.cart_table.item(itm)['values']
                                db_co = connect(path_to_database)
                                wri = db_co.cursor()
                                ll = "SELECT category FROM products WHERE description='{}'".format(cart_values[1])
                                wri.execute(ll)
                                r = wri.fetchall()
                                db_co.close()

                                if not r:
                                    services_in_cart.append(cart_values)

                                else:
                                    products_in_cart.append(cart_values)

                            for product in products_in_cart:
                                db_co = connect(path_to_database)
                                wri = db_co.cursor()
                                ll = "SELECT category FROM products WHERE description='{}'".format(product[1])
                                wri.execute(ll)
                                r = wri.fetchall()
                                db_co.close()

                                if r[0][0] != 'Printing':
                                    def collect_quantity(field, value):
                                        connection = connect(path_to_database)
                                        write = connection.cursor()
                                        lk_command = "SELECT quantity FROM {} WHERE {}='{}'".format("stock", field,
                                                                                                    str(value))
                                        write.execute(lk_command)
                                        values = write.fetchall()
                                        connection.close()

                                        return values

                                    old_quantity = collect_quantity("description", product[1])
                                    update_quantity = int(old_quantity[0][0]) - int(product[3])

                                    if update_quantity > 0:
                                        conn = connect(path_to_database)
                                        writes = conn.cursor()
                                        lk_comm = "UPDATE {} SET {}='{}' WHERE description='{}'".format("stock",
                                                                                                        "quantity",
                                                                                                        update_quantity,
                                                                                                        product[
                                                                                                            1])
                                        writes.execute(lk_comm)
                                        conn.commit()
                                        conn.close()

                                    else:
                                        payment_window.destroy()
                                        messagebox.showwarning("Low quantity",
                                                               "Cannot update quantity for {} due to low quantity\n"
                                                               "Transaction not complete!".format(product[1]))

                                else:
                                    if product[1].startswith("A4 Printing"):
                                        collect_values(product[3], "A4 Rim Papers")

                                    if product[1].startswith("A4 Copy"):
                                        collect_values(product[3], "A4 Rim Papers")

                                    if product[1].startswith("A3 Printing"):
                                        collect_values(product[3], "A3 Paper")

                                    if product[1].startswith("A3 Copy"):
                                        collect_values(product[3], "A3 Paper")

                                    if product[1].startswith("A4 Glossy"):
                                        collect_values(product[3], "Glossy Paper")

                                    if product[1].startswith("A4 Photo"):
                                        collect_values(product[3], "A4 Photo Paper")

                                    if product[1].startswith("A5 Photo"):
                                        collect_values(product[3], "A5 Photo Paper")

                                    if product[1].startswith("Passport"):
                                        collect_values(product[3], "Passport Paper")

                                    if product[1].startswith("A4 150 gsm"):
                                        collect_values(product[3], "A4 Art Paper 150 gsm")

                                    if product[1].startswith("A3 150 gsm"):
                                        collect_values(product[3], "A3 Art Paper 150 gsm")

                                    if product[1].startswith("A4 250/275/300 gsm"):
                                        collect_values(product[3], "A4 Art Paper 250/275/300 gsm")

                                    if product[1].startswith("A3 250/275/300 gsm"):
                                        collect_values(product[3], "A3 Art Paper 250/275/300 gsm")

                                conn = connect(path_to_database)
                                c = conn.cursor()
                                params2 = (self.new_transaction_number, current_time, product[1], product[2],
                                           product[3], product[4])
                                c.execute("INSERT INTO Sales VALUES (?, ?, ?, ?, ?, ?)", params2)
                                conn.commit()

                            for service in services_in_cart:
                                conn = connect(path_to_database)
                                c = conn.cursor()
                                params2 = (
                                    self.new_transaction_number, current_time, service[1], service[2],
                                    service[3], service[4])
                                c.execute("INSERT INTO Sales VALUES (?, ?, ?, ?, ?, ?)", params2)
                                conn.commit()

                            conn = connect(path_to_database)
                            c = conn.cursor()
                            params1 = (self.new_transaction_number, current_time, number_of_items, self.total_pay,
                                       pen_cash, discount, 0.0, float(debt_in.get().strip()), "debt")
                            c.execute("INSERT INTO Transactions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", params1)
                            conn.commit()
                            params4 = (self.new_transaction_number, first_name_value.get().strip(),
                                       second_name_value.get().strip(),
                                       contact_number_value.get().strip(), str(debt_in.get().strip()), current_time)
                            c.execute("INSERT INTO debts VALUES (?, ?, ?, ?, ?, ?)", params4)
                            conn.commit()
                            conn.close()

                            self.payment_label.configure(text="0.00")
                            self.total_pay = 0.0
                            payment_window.destroy()

                            for vals in self.cart_table.get_children():
                                self.cart_table.delete(vals)

                            self.new_transaction_function()
                            self.update_sales()

                        except ValueError:
                            pass

                        except StopIteration:
                            pass

                    else:
                        messagebox.showwarning("Form fill Error", "Make sure to fill filled marked with *\n"
                                                                  "Debt amount must be greater than 0!")

                except ValueError:
                    payment_window.destroy()
                    messagebox.showwarning("Amount Warning!", "Please make sure there are items in cart or\n"
                                                              "Make sure to enter {Paid Amount} section in the form")

            save_button = Button(debt_window, bg="red", fg="white")
            save_button.configure(relief='solid', text="SAVE RECORD", font=(font, 14), command=save_function)
            save_button.place(x=140, y=290)

        cash_sub_frame()

        mpesa_button = Button(payment_window, bg='green', fg='white')
        mpesa_button.configure(text="[F1] MPESA", relief='solid', font=(font, 15), command=mpesa_sub_frame)
        mpesa_button.place(x=50, y=30, width=110, height=40)

        cash_button = Button(payment_window, bg='blue', fg='white')
        cash_button.configure(text="[F2] CASH", relief='solid', font=(font, 15), command=cash_sub_frame)
        cash_button.place(x=180, y=30, width=100, height=40)

        credit_button = Button(payment_window, bg='red', fg='white')
        credit_button.configure(text="[F3] DEBT", relief='solid', font=(font, 15), command=debt_sub_frame)
        credit_button.place(x=300, y=30, width=100, height=40)

        def load_mpesa(event):
            mpesa_sub_frame()

        def load_cash(event):
            cash_sub_frame()

        def load_credit(event):
            debt_sub_frame()

        def close_payment(event):
            payment_window.destroy()

        payment_window.bind('<KeyPress-F1>', load_mpesa)
        payment_window.bind('<KeyPress-F2>', load_cash)
        payment_window.bind('<KeyPress-F3>', load_credit)
        payment_window.bind('<KeyPress-Home>', close_payment)

    def create_report(self):
        receipt_window = Toplevel(self.window_initializer)
        receipt_window.geometry("400x180")
        receipt_window.title("Choose Report Timeframe")
        receipt_window.resizable(False, False)
        center(receipt_window)
        time_frame_value = StringVar()

        report_time_label = Label(receipt_window)
        report_time_label.configure(text="Select Time Period:", font=(font, 12))
        report_time_label.place(x=30, y=30)

        report_time_list = Combobox(receipt_window, textvariable=time_frame_value)
        report_time_list['values'] = ['Yesterday', "Today", "Last 7 days", "This Month", "Last Month", "This Year",
                                      "Last Year"]
        report_time_list.configure(font=(font, 11), state='readonly')
        report_time_list.place(x=180, y=30)

        def report_generator(sales, mpesa_am, cash, discount, debts, expenses, floats, account_recv):
            pdf_creator = FPDF()
            pdf_creator.add_page()

            pdf_creator.set_font("Arial", "B", 20)
            pdf_creator.set_fill_color(r=90, g=199, b=99)
            pdf_creator.set_text_color(r=255, g=255, b=255)
            pdf_creator.cell(w=80, h=20, txt="SALES REPORT", ln=1, fill=True, align='C')
            pdf_creator.ln(5)

            pdf_creator.set_font("Arial", "BU", 15)
            pdf_creator.set_fill_color(r=255, g=255, b=255)
            pdf_creator.set_text_color(r=0, g=0, b=0)
            pdf_creator.cell(w=0, h=8, txt="HUDUMIA CYBER", ln=1)

            pdf_creator.set_font("Arial", "B", 11)
            pdf_creator.cell(w=15, h=7, txt="Phone: ", ln=0)
            pdf_creator.set_font("Arial", "", 11)
            pdf_creator.cell(w=0, h=7, txt="+254 7969 52820", ln=1)

            pdf_creator.set_font("Arial", "B", 11)
            pdf_creator.cell(w=13, h=7, txt="Email: ", ln=0)
            pdf_creator.set_font("Arial", "", 11)
            pdf_creator.cell(w=0, h=7, txt="hudumiacyber@gmail.com", ln=1)

            pdf_creator.set_font("Arial", "B", 11)
            pdf_creator.cell(w=19, h=7, txt="P.O. BOX: ", ln=0)
            pdf_creator.set_font("Arial", "", 11)
            pdf_creator.cell(w=0, h=7, txt="120-00100", ln=1)

            pdf_creator.set_font("Arial", "B", 11)
            pdf_creator.cell(w=18, h=7, txt="Address: ", ln=0)
            pdf_creator.set_font("Arial", "", 11)
            pdf_creator.cell(w=0, h=7, txt="Nairobi, Kenya", ln=1)

            pdf_creator.set_font("Arial", "B", 11)
            pdf_creator.cell(w=18, h=7, txt="Location: ", ln=0)
            pdf_creator.set_font("Arial", "", 11)
            pdf_creator.cell(w=0, h=7, txt="Northern Bypass, Marurui Thome", ln=1)

            display_time = time.strftime('%d %B %Y')
            pdf_creator.ln(5)
            pdf_creator.set_font("Arial", "B", 11)
            pdf_creator.cell(w=13, h=7, txt="DATE: ", ln=0)
            pdf_creator.set_font("Arial", "", 11)
            pdf_creator.cell(w=0, h=7, txt=display_time, ln=1)
            pdf_creator.ln(3)

            pdf_creator.set_fill_color(r=90, g=199, b=99)
            pdf_creator.set_text_color(r=255, g=255, b=255)
            pdf_creator.cell(w=50, h=8, txt="Category", ln=0, fill=True)
            pdf_creator.cell(w=20, h=8, txt="Sub Total", ln=1, fill=True)
            pdf_creator.ln(2)

            pdf_creator.set_fill_color(r=255, g=255, b=255)
            pdf_creator.set_font("Arial", "B", 11)
            pdf_creator.set_text_color(r=0, g=0, b=0)
            pdf_creator.cell(w=50, h=6, txt="Total Sales", ln=0, fill=True)
            pdf_creator.cell(w=20, h=6, txt="{}".format(sales), ln=1, fill=True)
            pdf_creator.set_font("Arial", "", 11)

            pdf_creator.set_fill_color(r=150, g=212, b=212)
            pdf_creator.cell(w=50, h=6, txt="Mpesa Amount", ln=0, fill=True)
            pdf_creator.cell(w=20, h=6, txt="{}".format(mpesa_am), ln=1, fill=True)

            pdf_creator.set_fill_color(r=255, g=255, b=255)
            pdf_creator.cell(w=50, h=6, txt="Cash Amount", ln=0, fill=True)
            pdf_creator.cell(w=20, h=6, txt="{}".format(cash), ln=1, fill=True)

            pdf_creator.set_fill_color(r=150, g=212, b=212)
            pdf_creator.cell(w=50, h=6, txt="Discount", ln=0, fill=True)
            pdf_creator.cell(w=20, h=6, txt="{}".format(discount), ln=1, fill=True)

            pdf_creator.set_fill_color(r=255, g=255, b=255)
            pdf_creator.cell(w=50, h=6, txt="Debts", ln=0, fill=True)
            pdf_creator.cell(w=20, h=6, txt="{}".format(debts), ln=1, fill=True)

            pdf_creator.set_fill_color(r=150, g=212, b=212)
            pdf_creator.cell(w=50, h=6, txt="Expenses", ln=0, fill=True)
            pdf_creator.cell(w=20, h=6, txt="{}".format(expenses), ln=1, fill=True)

            pdf_creator.set_fill_color(r=255, g=255, b=255)
            pdf_creator.cell(w=50, h=6, txt="Float Balance", ln=0, fill=True)
            pdf_creator.cell(w=20, h=6, txt="{}".format(floats), ln=1, fill=True)

            pdf_creator.set_fill_color(r=150, g=212, b=212)
            pdf_creator.cell(w=50, h=6, txt="Account Recv.", ln=0, fill=True)
            pdf_creator.cell(w=20, h=6, txt="{}".format(account_recv), ln=1, fill=True)
            pdf_creator.ln(1)

            pdf_creator.set_font("Arial", "", 11)
            pdf_creator.set_fill_color(r=0, g=0, b=0)
            pdf_creator.cell(w=70, h=1, txt="", ln=1, fill=True)
            pdf_creator.ln(1)

            profit = sales - discount - debts - expenses
            pdf_creator.set_fill_color(r=255, g=255, b=255)
            pdf_creator.set_text_color(r=0, g=0, b=0)
            pdf_creator.set_font("Arial", "BU", 13)
            pdf_creator.cell(w=50, h=10, txt="TOTAL", ln=0, fill=True)
            pdf_creator.set_font("Arial", "B", 13)
            pdf_creator.cell(w=20, h=10, txt="{}".format(profit), ln=1, fill=True)

            try:
                desktop_location = path.join(path.join(path.expanduser('~')), 'Desktop')
                filepath = filedialog.askdirectory(initialdir=r"{}".format(desktop_location),
                                                   title="Select File Path")
                if len(filepath) > 2:
                    full_path = filepath + "/" + "Sales Report(" + time.strftime('%d-%B-%Y %H_%M %p') + ")" + ".pdf"
                    messagebox.showinfo("Report Generated", "Report was saved successfully to:\n"
                                                            "{}".format(full_path))

                    pdf_creator.output(full_path)

                else:
                    pass

            except PermissionError:
                pass

        def debt_calculator(debt_list):
            debt_debt = 0
            debt_discount = 0
            debt_total_sales = 0
            for debts_ in debt_list:
                debt_debt = debt_debt + debts_[7]
                debt_total_sales = debt_total_sales + debts_[3]
                debt_discount = debt_discount + debts_[5]

            return debt_total_sales, 0, 0, debt_discount, debt_debt

        def cash_calculator(cash_list):
            cash_debt = 0
            cash_discount = 0
            cash = 0
            cash_sales = 0

            for cash_ in cash_list:
                cash_debt = cash_debt + cash_[7]
                cash_discount = cash_discount + cash_[5]
                cash_sales = cash_sales + cash_[3]
                cash = cash + (cash_[4] - cash_[6] - cash_[7])

            return cash_sales, 0, cash, cash_discount, cash_debt

        def mpesa_calculator(mpesa_list):
            mpesa_debt = 0
            mpesa_discount = 0
            mpesa_sales = 0
            mpesa_amount = 0
            mpesa_cash = 0

            for mpesa_ in mpesa_list:
                mpesa_debt = mpesa_debt + mpesa_[7]
                mpesa_discount = mpesa_discount + mpesa_[5]
                mpesa_sales = mpesa_sales + mpesa_[3]
                mpesa_amount = mpesa_amount + abs((mpesa_[4] - mpesa_[6]))
                mpesa_cash = mpesa_cash + mpesa_[6]

            return mpesa_sales, mpesa_amount, mpesa_cash, mpesa_discount, mpesa_debt

        def mpesa_cash_calculator(mpesa_list):
            mpesa_debt = 0
            mpesa_discount = 0
            mpesa_sales = 0
            mpesa_amount = 0
            mpesa_cash = 0

            for mpesa_ in mpesa_list:
                mpesa_debt = mpesa_debt + mpesa_[7]
                mpesa_discount = mpesa_discount + mpesa_[5]
                mpesa_sales = mpesa_sales + mpesa_[3]
                mpesa_amount = mpesa_amount + mpesa_[4]
                mpesa_cash = mpesa_cash + mpesa_[6]

            return mpesa_sales, mpesa_amount, mpesa_cash, mpesa_discount, mpesa_debt

        def data_collection(string_):
            connection = connect(path_to_database)
            write = connection.cursor()
            lk_command = "SELECT * FROM Transactions WHERE TransactionDate LIKE '{}'".format(string_)
            write.execute(lk_command)
            values = write.fetchall()
            connection.close()

            return values

        def get_data():
            if time_frame_value.get() == "Today":
                today = datetime.datetime.today()
                current_time = today.strftime("%d/%B/%Y")
                current_time = current_time + "%"
                values = data_collection(current_time)

                try:
                    connection = connect(path_to_database)
                    write = connection.cursor()
                    lk_command = "SELECT Amount FROM Expenses WHERE Date LIKE '{}'".format(str(current_time) + "%")
                    write.execute(lk_command)
                    amounts = write.fetchall()
                    connection.close()

                    today_expense = 0
                    for sums in amounts:
                        today_expense = today_expense + sums[0]

                except IndexError:
                    today_expense = 0

                try:
                    connection = connect(path_to_database)
                    write = connection.cursor()
                    lk_command = "SELECT Float FROM Costs WHERE Date LIKE '{}'".format(str(current_time) + "%")
                    write.execute(lk_command)
                    floats = write.fetchall()
                    connection.close()
                    today_float = sum(floats[0])

                except IndexError:
                    today_float = 0

                try:
                    connection = connect(path_to_database)
                    write = connection.cursor()
                    lk_command = "SELECT Amount FROM Account_recv WHERE Date LIKE '{}'".format(str(current_time) + "%")
                    write.execute(lk_command)
                    cash_recv = write.fetchall()
                    connection.close()

                    cash_received = 0
                    for cash_rv in cash_recv:
                        cash_received = cash_received + cash_rv[0]

                except IndexError:
                    cash_received = 0

                mpesa_data = []
                cash_data = []
                debt_data = []
                mpesa_cash_data = []

                for vals in values:
                    if vals[8] == "debt":
                        debt_data.append(vals)

                    if vals[8] == "cash":
                        cash_data.append(vals)

                    if vals[8] == "mpesa":
                        mpesa_data.append(vals)

                    if vals[8] == "mpesa&cash":
                        mpesa_cash_data.append(vals)

                debt_sale, debt_mpesa, debt_cash, debt_discount, debt_debt = debt_calculator(debt_data)
                cash_sale, cash_mpesa, cash_cash, cash_discount, cash_debt = cash_calculator(cash_data)
                mpesa_sale, mpesa_mpesa, mpesa_cash, mpesa_discount, mpesa_debt = mpesa_calculator(mpesa_data)
                mpesa_cash_sale, mpesa_cash_mpesa, mpesa_cash_cash, mpesa_cash_discount, mpesa_cash_debt = mpesa_cash_calculator(
                    mpesa_cash_data)

                total_sales = debt_sale + cash_sale + mpesa_sale + mpesa_cash_sale
                mpesa_bal = debt_mpesa + cash_mpesa + mpesa_mpesa + mpesa_cash_mpesa
                cash_bal = debt_cash + cash_cash + mpesa_cash + mpesa_cash_cash
                total_discount = debt_discount + cash_discount + mpesa_discount + mpesa_cash_discount
                total_debt = debt_debt + cash_debt + mpesa_cash_debt + mpesa_debt

                report_generator(total_sales, mpesa_bal, cash_bal, total_discount, total_debt, today_expense,
                                 today_float, cash_received)

            if time_frame_value.get() == "Yesterday":
                today = datetime.datetime.today()
                current_time = today.strftime("%d/%B/%Y")
                yesterday_time = int((current_time[0] + current_time[1])) - 1
                values = data_collection(str(yesterday_time) + "%")

                try:
                    connection = connect(path_to_database)
                    write = connection.cursor()
                    lk_command = "SELECT Amount FROM Expenses WHERE Date LIKE '{}'".format(str(yesterday_time) + "%")
                    write.execute(lk_command)
                    amounts = write.fetchall()
                    connection.close()
                    today_expense = 0
                    for sums in amounts:
                        today_expense = today_expense + sums[0]

                except IndexError:
                    today_expense = 0

                try:
                    connection = connect(path_to_database)
                    write = connection.cursor()
                    lk_command = "SELECT Float FROM Costs WHERE Date LIKE '{}'".format(str(yesterday_time) + "%")
                    write.execute(lk_command)
                    floats = write.fetchall()
                    connection.close()
                    today_float = sum(floats[0])

                except IndexError:
                    today_float = 0

                try:
                    connection = connect(path_to_database)
                    write = connection.cursor()
                    lk_command = "SELECT Amount FROM Account_recv WHERE Date LIKE '{}'".format(str(yesterday_time) + "%")
                    write.execute(lk_command)
                    cash_recv = write.fetchall()
                    connection.close()

                    cash_received = 0
                    for cash_rv in cash_recv:
                        cash_received = cash_received + cash_rv[0]

                except IndexError:
                    cash_received = 0

                mpesa_data = []
                cash_data = []
                debt_data = []
                mpesa_cash_data = []

                for vals in values:
                    if vals[8] == "debt":
                        debt_data.append(vals)

                    if vals[8] == "cash":
                        cash_data.append(vals)

                    if vals[8] == "mpesa":
                        mpesa_data.append(vals)

                    if vals[8] == "mpesa&cash":
                        mpesa_cash_data.append(vals)

                debt_sale, debt_mpesa, debt_cash, debt_discount, debt_debt = debt_calculator(debt_data)
                cash_sale, cash_mpesa, cash_cash, cash_discount, cash_debt = cash_calculator(cash_data)
                mpesa_sale, mpesa_mpesa, mpesa_cash, mpesa_discount, mpesa_debt = mpesa_calculator(mpesa_data)
                mpesa_cash_sale, mpesa_cash_mpesa, mpesa_cash_cash, mpesa_cash_discount, mpesa_cash_debt = mpesa_cash_calculator(
                    mpesa_cash_data)

                total_sales = debt_sale + cash_sale + mpesa_sale + mpesa_cash_sale
                mpesa_bal = debt_mpesa + cash_mpesa + mpesa_mpesa + mpesa_cash_mpesa
                cash_bal = debt_cash + cash_cash + mpesa_cash + mpesa_cash_cash
                total_discount = debt_discount + cash_discount + mpesa_discount + mpesa_cash_discount
                total_debt = debt_debt + cash_debt + mpesa_cash_debt + mpesa_debt

                report_generator(total_sales, mpesa_bal, cash_bal, total_discount, total_debt, today_expense,
                                 today_float, cash_received)

            if time_frame_value.get() == "Last 7 days":
                def calculate_time(day_of_week):
                    connection = connect(path_to_database)
                    write = connection.cursor()
                    lk_command = "SELECT * FROM Expenses WHERE Date LIKE '{}'".format(day_of_week + "%")
                    write.execute(lk_command)
                    values = write.fetchall()
                    connection.close()

                    return values

                def collect_expenses(day_of_week):
                    connection = connect(path_to_database)
                    write = connection.cursor()
                    lk_command = "SELECT Amount FROM Expenses WHERE Date LIKE '{}'".format(day_of_week)
                    write.execute(lk_command)
                    amounts = write.fetchall()
                    connection.close()

                    return amounts

                def collect_floats(day_of_week):
                    connection = connect(path_to_database)
                    write = connection.cursor()
                    lk_command = "SELECT Float FROM Costs WHERE Date LIKE '{}'".format(day_of_week)
                    write.execute(lk_command)
                    floats = write.fetchall()
                    connection.close()

                    return floats

                week_data = []
                expense_data = []
                float_data = []

                for i in range(1, 7):
                    previous_date = datetime.datetime.today() - datetime.timedelta(days=i)
                    current_tim = previous_date.strftime("%d/%B/%Y")
                    week_values = calculate_time(current_tim)
                    week_data.append(week_values)
                    expense_data.append(collect_expenses(current_tim))
                    float_data.append(collect_floats(current_tim))

                mpesa_data = []
                cash_data = []
                debt_data = []
                mpesa_cash_data = []
                expense_list = []
                float_list = []

                for list_ in expense_data:
                    expense_list.append(sum(list_))

                for f_list in float_data:
                    float_list.append(sum(f_list))

                try:
                    total_expense = 0
                    for sums in expense_list:
                        total_expense = total_expense + sums

                except IndexError:
                    total_expense = 0

                try:
                    total_float = sum(float_list)

                except IndexError:
                    total_float = 0

                for i in range(0, len(week_data)):
                    try:
                        if week_data[i][8] == "debt":
                            debt_data.append(week_data[i])

                        if week_data[i][8] == "cash":
                            cash_data.append(week_data[i])

                        if week_data[i][8] == "mpesa":
                            mpesa_data.append(week_data[i])

                        if week_data[i][8] == "mpesa&cash":
                            mpesa_cash_data.append(week_data[i])

                    except IndexError:
                        pass

                debt_sale, debt_mpesa, debt_cash, debt_discount, debt_debt = debt_calculator(debt_data)
                cash_sale, cash_mpesa, cash_cash, cash_discount, cash_debt = cash_calculator(cash_data)
                mpesa_sale, mpesa_mpesa, mpesa_cash, mpesa_discount, mpesa_debt = mpesa_calculator(mpesa_data)
                mpesa_cash_sale, mpesa_cash_mpesa, mpesa_cash_cash, mpesa_cash_discount, mpesa_cash_debt = mpesa_cash_calculator(
                    mpesa_cash_data)

                total_sales = debt_sale + cash_sale + mpesa_sale + mpesa_cash_sale
                mpesa_bal = debt_mpesa + cash_mpesa + mpesa_mpesa + mpesa_cash_mpesa
                cash_bal = debt_cash + cash_cash + mpesa_cash + mpesa_cash_cash
                total_discount = debt_discount + cash_discount + mpesa_discount + mpesa_cash_discount
                total_debt = debt_debt + cash_debt + mpesa_cash_debt + mpesa_debt

                report_generator(total_sales, mpesa_bal, cash_bal, total_discount, total_debt, total_expense,
                                 total_float, 0)

            if time_frame_value.get() == "This Month":
                today = datetime.datetime.today()
                current_time = today.strftime("%B/%Y")
                values = data_collection("%" + str(current_time) + "%")

                try:
                    connection = connect(path_to_database)
                    write = connection.cursor()
                    lk_command = "SELECT Amount FROM Expenses WHERE Date LIKE '{}'".format(
                        "%" + str(current_time) + "%")
                    write.execute(lk_command)
                    amounts = write.fetchall()
                    connection.close()
                    today_expense = 0

                    for sums in amounts:
                        today_expense = today_expense + sums[0]

                except IndexError:
                    today_expense = 0

                try:
                    connection = connect(path_to_database)
                    write = connection.cursor()
                    lk_command = "SELECT Amount FROM Account_recv WHERE Date LIKE '{}'".format(
                        "%" + str(current_time) + "%")
                    write.execute(lk_command)
                    cash_recv = write.fetchall()
                    connection.close()

                    cash_received = 0
                    for cash_rv in cash_recv:
                        cash_received = cash_received + cash_rv[0]

                except IndexError:
                    cash_received = 0

                try:
                    connection = connect(path_to_database)
                    write = connection.cursor()
                    lk_command = "SELECT Float FROM Costs WHERE Date LIKE '{}'".format("%" + str(current_time) + "%")
                    write.execute(lk_command)
                    floats = write.fetchall()
                    connection.close()
                    today_float = sum(floats[0])

                except IndexError:
                    today_float = 0

                mpesa_data = []
                cash_data = []
                debt_data = []
                mpesa_cash_data = []

                for vals in values:
                    if vals[8] == "debt":
                        debt_data.append(vals)

                    if vals[8] == "cash":
                        cash_data.append(vals)

                    if vals[8] == "mpesa":
                        mpesa_data.append(vals)

                    if vals[8] == "mpesa&cash":
                        mpesa_cash_data.append(vals)

                debt_sale, debt_mpesa, debt_cash, debt_discount, debt_debt = debt_calculator(debt_data)
                cash_sale, cash_mpesa, cash_cash, cash_discount, cash_debt = cash_calculator(cash_data)
                mpesa_sale, mpesa_mpesa, mpesa_cash, mpesa_discount, mpesa_debt = mpesa_calculator(mpesa_data)
                mpesa_cash_sale, mpesa_cash_mpesa, mpesa_cash_cash, mpesa_cash_discount, mpesa_cash_debt = mpesa_cash_calculator(
                    mpesa_cash_data)

                total_sales = debt_sale + cash_sale + mpesa_sale + mpesa_cash_sale
                mpesa_bal = debt_mpesa + cash_mpesa + mpesa_mpesa + mpesa_cash_mpesa
                cash_bal = debt_cash + cash_cash + mpesa_cash + mpesa_cash_cash
                total_discount = debt_discount + cash_discount + mpesa_discount + mpesa_cash_discount
                total_debt = debt_debt + cash_debt + mpesa_cash_debt + mpesa_debt

                report_generator(total_sales, mpesa_bal, cash_bal, total_discount, total_debt, today_expense,
                                 today_float, cash_received)

            if time_frame_value.get() == "Last Month":
                last_month = datetime.datetime.now() - relativedelta(months=1)
                last_month_day = format(last_month, '%B/%Y')
                values = data_collection("%" + last_month_day + "%")

                try:
                    connection = connect(path_to_database)
                    write = connection.cursor()
                    lk_command = "SELECT Amount FROM Expenses WHERE Date LIKE '{}'".format("%" + last_month_day + "%")
                    write.execute(lk_command)
                    amounts = write.fetchall()
                    connection.close()
                    today_expense = 0
                    for sums in amounts:
                        today_expense = today_expense + sums[0]

                except IndexError:
                    today_expense = 0

                try:
                    connection = connect(path_to_database)
                    write = connection.cursor()
                    lk_command = "SELECT Amount FROM Account_recv WHERE Date LIKE '{}'".format("%" + last_month_day + "%")
                    write.execute(lk_command)
                    cash_recv = write.fetchall()
                    connection.close()

                    cash_received = 0
                    for cash_rv in cash_recv:
                        cash_received = cash_received + cash_rv[0]

                except IndexError:
                    cash_received = 0

                try:
                    connection = connect(path_to_database)
                    write = connection.cursor()
                    lk_command = "SELECT Float FROM Costs WHERE Date LIKE '{}'".format("%" + last_month_day + "%")
                    write.execute(lk_command)
                    floats = write.fetchall()
                    connection.close()
                    today_float = sum(floats[0])

                except IndexError:
                    today_float = 0

                mpesa_data = []
                cash_data = []
                debt_data = []
                mpesa_cash_data = []

                for vals in values:
                    if vals[8] == "debt":
                        debt_data.append(vals)

                    if vals[8] == "cash":
                        cash_data.append(vals)

                    if vals[8] == "mpesa":
                        mpesa_data.append(vals)

                    if vals[8] == "mpesa&cash":
                        mpesa_cash_data.append(vals)

                debt_sale, debt_mpesa, debt_cash, debt_discount, debt_debt = debt_calculator(debt_data)
                cash_sale, cash_mpesa, cash_cash, cash_discount, cash_debt = cash_calculator(cash_data)
                mpesa_sale, mpesa_mpesa, mpesa_cash, mpesa_discount, mpesa_debt = mpesa_calculator(mpesa_data)
                mpesa_cash_sale, mpesa_cash_mpesa, mpesa_cash_cash, mpesa_cash_discount, mpesa_cash_debt = mpesa_cash_calculator(
                    mpesa_cash_data)

                total_sales = debt_sale + cash_sale + mpesa_sale + mpesa_cash_sale
                mpesa_bal = debt_mpesa + cash_mpesa + mpesa_mpesa + mpesa_cash_mpesa
                cash_bal = debt_cash + cash_cash + mpesa_cash + mpesa_cash_cash
                total_discount = debt_discount + cash_discount + mpesa_discount + mpesa_cash_discount
                total_debt = debt_debt + cash_debt + mpesa_cash_debt + mpesa_debt

                report_generator(total_sales, mpesa_bal, cash_bal, total_discount, total_debt, today_expense,
                                 today_float, cash_received)

            if time_frame_value.get() == "This Year":
                today = datetime.datetime.today()
                current_time = today.strftime("%Y")
                values = data_collection("%" + str(current_time) + "%")

                try:
                    connection = connect(path_to_database)
                    write = connection.cursor()
                    lk_command = "SELECT Amount FROM Expenses WHERE Date LIKE '{}'".format(
                        "%" + str(current_time) + "%")
                    write.execute(lk_command)
                    amounts = write.fetchall()
                    connection.close()
                    today_expense = 0
                    for sums in amounts:
                        today_expense = today_expense + sums[0]

                except IndexError:
                    today_expense = 0

                try:
                    connection = connect(path_to_database)
                    write = connection.cursor()
                    lk_command = "SELECT Amount FROM Account_recv WHERE Date LIKE '{}'".format(
                        "%" + str(current_time) + "%")
                    write.execute(lk_command)
                    cash_recv = write.fetchall()
                    connection.close()

                    cash_received = 0
                    for cash_rv in cash_recv:
                        cash_received = cash_received + cash_rv[0]

                except IndexError:
                    cash_received = 0

                try:
                    connection = connect(path_to_database)
                    write = connection.cursor()
                    lk_command = "SELECT Float FROM Costs WHERE Date LIKE '{}'".format("%" + str(current_time) + "%")
                    write.execute(lk_command)
                    floats = write.fetchall()
                    connection.close()
                    today_float = sum(floats[0])

                except IndexError:
                    today_float = 0

                mpesa_data = []
                cash_data = []
                debt_data = []
                mpesa_cash_data = []

                for vals in values:
                    if vals[8] == "debt":
                        debt_data.append(vals)

                    if vals[8] == "cash":
                        cash_data.append(vals)

                    if vals[8] == "mpesa":
                        mpesa_data.append(vals)

                    if vals[8] == "mpesa&cash":
                        mpesa_cash_data.append(vals)

                debt_sale, debt_mpesa, debt_cash, debt_discount, debt_debt = debt_calculator(debt_data)
                cash_sale, cash_mpesa, cash_cash, cash_discount, cash_debt = cash_calculator(cash_data)
                mpesa_sale, mpesa_mpesa, mpesa_cash, mpesa_discount, mpesa_debt = mpesa_calculator(mpesa_data)
                mpesa_cash_sale, mpesa_cash_mpesa, mpesa_cash_cash, mpesa_cash_discount, mpesa_cash_debt = mpesa_cash_calculator(
                    mpesa_cash_data)

                total_sales = debt_sale + cash_sale + mpesa_sale + mpesa_cash_sale
                mpesa_bal = debt_mpesa + cash_mpesa + mpesa_mpesa + mpesa_cash_mpesa
                cash_bal = debt_cash + cash_cash + mpesa_cash + mpesa_cash_cash
                total_discount = debt_discount + cash_discount + mpesa_discount + mpesa_cash_discount
                total_debt = debt_debt + cash_debt + mpesa_cash_debt + mpesa_debt

                report_generator(total_sales, mpesa_bal, cash_bal, total_discount, total_debt, today_expense,
                                 today_float, cash_received)

            if time_frame_value.get() == "Last Year":
                last_month = datetime.datetime.now() - relativedelta(years=1)
                last_month_day = format(last_month, '%Y')
                values = data_collection("%" + last_month_day + "%")

                try:
                    connection = connect(path_to_database)
                    write = connection.cursor()
                    lk_command = "SELECT Amount FROM Expenses WHERE Date LIKE '{}'".format("%" + last_month_day + "%")
                    write.execute(lk_command)
                    amounts = write.fetchall()
                    connection.close()
                    today_expense = 0
                    for sums in amounts:
                        today_expense = today_expense + sums[0]

                except IndexError:
                    today_expense = 0

                try:
                    connection = connect(path_to_database)
                    write = connection.cursor()
                    lk_command = "SELECT Amount FROM Account_recv WHERE Date LIKE '{}'".format("%" + last_month_day + "%")
                    write.execute(lk_command)
                    cash_recv = write.fetchall()
                    connection.close()

                    cash_received = 0
                    for cash_rv in cash_recv:
                        cash_received = cash_received + cash_rv[0]

                except IndexError:
                    cash_received = 0

                try:
                    connection = connect(path_to_database)
                    write = connection.cursor()
                    lk_command = "SELECT Float FROM Costs WHERE Date LIKE '{}'".format("%" + last_month_day + "%")
                    write.execute(lk_command)
                    floats = write.fetchall()
                    connection.close()
                    today_float = sum(floats[0])

                except IndexError:
                    today_float = 0

                mpesa_data = []
                cash_data = []
                debt_data = []
                mpesa_cash_data = []

                for vals in values:
                    if vals[8] == "debt":
                        debt_data.append(vals)

                    if vals[8] == "cash":
                        cash_data.append(vals)

                    if vals[8] == "mpesa":
                        mpesa_data.append(vals)

                    if vals[8] == "mpesa&cash":
                        mpesa_cash_data.append(vals)

                debt_sale, debt_mpesa, debt_cash, debt_discount, debt_debt = debt_calculator(debt_data)
                cash_sale, cash_mpesa, cash_cash, cash_discount, cash_debt = cash_calculator(cash_data)
                mpesa_sale, mpesa_mpesa, mpesa_cash, mpesa_discount, mpesa_debt = mpesa_calculator(mpesa_data)
                mpesa_cash_sale, mpesa_cash_mpesa, mpesa_cash_cash, mpesa_cash_discount, mpesa_cash_debt = mpesa_cash_calculator(
                    mpesa_cash_data)

                total_sales = debt_sale + cash_sale + mpesa_sale + mpesa_cash_sale
                mpesa_bal = debt_mpesa + cash_mpesa + mpesa_mpesa + mpesa_cash_mpesa
                cash_bal = debt_cash + cash_cash + mpesa_cash + mpesa_cash_cash
                total_discount = debt_discount + cash_discount + mpesa_discount + mpesa_cash_discount
                total_debt = debt_debt + cash_debt + mpesa_cash_debt + mpesa_debt

                report_generator(total_sales, mpesa_bal, cash_bal, total_discount, total_debt, today_expense,
                                 today_float, cash_received)

            receipt_window.destroy()

        report_generate_btn = Button(receipt_window, command=get_data)
        report_generate_btn.configure(relief='solid', text="GENERATE REPORT", font=(font, 12), bg='green', fg='white')
        report_generate_btn.place(x=130, y=100)

        def close_receipt(event):
            receipt_window.destroy()

        receipt_window.bind("<KeyPress-Home>", close_receipt)

    def remove_stock(self):
        cashier_waste_frame = Toplevel(self.window_initializer)
        cashier_waste_frame.geometry("450x250")
        cashier_waste_frame.title("Remove Stock")
        cashier_waste_frame.resizable(False, False)
        center(cashier_waste_frame)

        cashier_waste_label = Label(cashier_waste_frame)
        cashier_waste_label.configure(font=(font, 14, "bold"), text="Select Stock:")
        cashier_waste_label.place(x=35, y=20)
        stock_waste_var = StringVar()

        def get_stock_information():
            db_connection = connect(path_to_database)
            writer = db_connection.cursor()
            lookup_command = "SELECT * FROM {}".format("stock")
            writer.execute(lookup_command)
            result = writer.fetchall()
            db_connection.close()

            stock_info = []

            for stocks in result:
                stock_info.append(str(stocks[2]))

            return stock_info

        cashier_waste_entry = Combobox(cashier_waste_frame)
        cashier_waste_entry['values'] = get_stock_information()
        cashier_waste_entry.configure(font=(font, 12), state='readonly', textvariable=stock_waste_var)
        cashier_waste_entry.place(x=180, y=23)

        cashier_waste_quan_label = Label(cashier_waste_frame)
        cashier_waste_quan_label.configure(font=(font, 14, "bold"), text="Stock Quantity:")
        cashier_waste_quan_label.place(x=35, y=60)

        cashier_waste_quan_entry = Entry(cashier_waste_frame)
        cashier_waste_quan_entry.configure(font=(font, 13), justify=CENTER, state='disabled')
        cashier_waste_quan_entry.place(x=180, y=60)

        cashier_waste_amnt_label = Label(cashier_waste_frame)
        cashier_waste_amnt_label.configure(font=(font, (14), "bold"), text="Remove Amount:")
        cashier_waste_amnt_label.place(x=35, y=100)

        waste_amnt = IntVar()
        cashier_waste_amnt_entry = Entry(cashier_waste_frame, textvariable=waste_amnt)
        cashier_waste_amnt_entry.configure(font=(font, 13), justify=CENTER)
        cashier_waste_amnt_entry.place(x=180, y=100)
        cashier_waste_amnt_entry.delete(0, END)

        def load_stock_waste(*args):
            stock_waste_name = stock_waste_var.get()

            db_connection = connect(path_to_database)
            writer = db_connection.cursor()
            lookup_command = "SELECT * FROM {} WHERE description='{}'".format("stock", stock_waste_name)
            writer.execute(lookup_command)
            result = writer.fetchall()
            db_connection.close()

            current_stock_amount = result[0][3]
            cashier_waste_quan_entry.configure(state='normal')
            cashier_waste_quan_entry.delete(0, END)
            cashier_waste_quan_entry.insert(0, str(current_stock_amount))
            cashier_waste_quan_entry.configure(state='disabled')

        stock_waste_var.trace("w", load_stock_waste)

        def waste_cancel():
            cashier_waste_quan_entry.configure(state='normal')
            cashier_waste_quan_entry.delete(0, END)
            cashier_waste_quan_entry.configure(state='disabled')

            cashier_waste_amnt_entry.delete(0, END)

        def update_waste():
            try:
                stock_name = stock_waste_var.get()
                db_connection = connect(path_to_database)
                writer = db_connection.cursor()
                lookup_command = "SELECT quantity FROM {} WHERE description='{}'".format("stock", stock_name)
                writer.execute(lookup_command)
                result = writer.fetchall()
                db_connection.close()

                wasted_amount = waste_amnt.get()
                current_stock = result[0][0]
                print(wasted_amount, current_stock)

                if int(current_stock) > wasted_amount:
                    today = datetime.datetime.today()
                    current_time = today.strftime("%d/%B/%Y %H:%M")
                    new_amount = int(current_stock) - int(wasted_amount)

                    conn = connect(path_to_database)
                    writes = conn.cursor()
                    lk_comm = "UPDATE stock SET quantity='{}' WHERE description='{}'".format(new_amount, stock_name)
                    lk_comm2 = "UPDATE stock SET stockindate='{}' WHERE description='{}'".format(current_time,
                                                                                                 stock_name)
                    writes.execute(lk_comm)
                    writes.execute(lk_comm2)
                    conn.commit()
                    conn.close()
                    waste_cancel()

                else:
                    messagebox.showwarning("Waste Error", "Waste quantity should less than stock quantity!")
                    waste_cancel()

            except TclError:
                messagebox.showwarning("Waste Error", "Waste quantity should be a number")
                waste_cancel()

        cashier_update_waste = Button(cashier_waste_frame, bg='light green')
        cashier_update_waste.configure(text="UPDATE", font=(font, 14), relief='solid')
        cashier_update_waste.configure(command=update_waste)
        cashier_update_waste.place(x=180, y=160)

        cashier_cancel_waste = Button(cashier_waste_frame, bg='light yellow')
        cashier_cancel_waste.configure(text="CANCEL", font=(font, 14), relief='solid')
        cashier_cancel_waste.configure(command=waste_cancel)
        cashier_cancel_waste.place(x=280, y=160)

    def costs_window(self):
        cost_win = Toplevel(self.window_initializer)
        cost_win.geometry("400x300")
        cost_win.title("Expenses and Float")
        cost_win.resizable(False, False)
        center(cost_win)

        today = datetime.datetime.today()
        current_time = today.strftime("%d/%B/%Y")

        def float_section():
            float_frame = Frame(cost_win)
            float_frame.configure(width=360, height=200)
            float_frame.place(x=20, y=70)
            today_float = DoubleVar()

            float_label = Label(float_frame)
            float_label.configure(text="Today's Float:", font=(font, 12, "bold"))
            float_label.place(x=30, y=20)

            db_connection = connect(path_to_database)
            writer = db_connection.cursor()
            lookup_command = "SELECT Float FROM Costs WHERE Date LIKE '{}'".format(current_time)
            writer.execute(lookup_command)
            result = writer.fetchall()
            db_connection.close()

            try:
                float_t_entry = Entry(float_frame)
                float_t_entry.configure(font=(font, 12), relief="solid", justify=CENTER, state='disabled')
                float_t_entry.place(x=140, y=22)
                float_t_entry.configure(state='normal')
                float_t_entry.insert(0, result[0][0])
                float_t_entry.configure(state='disabled')

                float_label_ = Label(float_frame)
                float_label_.configure(text="Enter float:", font=(font, 12, "bold"))
                float_label_.place(x=30, y=60)

                float_t_entry_ = Entry(float_frame, textvariable=today_float)
                float_t_entry_.configure(font=(font, 12), relief="solid", justify=CENTER, state='disabled')
                float_t_entry_.place(x=140, y=62)
                float_t_entry_.delete(0, END)

                float_save_btn = Label(float_frame)
                float_save_btn.configure(text="Float already entered!", font=(font, 13), fg="green")
                float_save_btn.place(x=90, y=120)

            except IndexError:
                float_t_entry = Entry(float_frame)
                float_t_entry.configure(font=(font, 12), relief="solid", justify=CENTER, state='disabled')
                float_t_entry.place(x=140, y=22)
                float_t_entry.configure(state='normal')
                float_t_entry.insert(0, "0.0")
                float_t_entry.configure(state='disabled')

                float_label_ = Label(float_frame)
                float_label_.configure(text="Enter float:", font=(font, 12, "bold"))
                float_label_.place(x=30, y=60)

                float_t_entry_ = Entry(float_frame, textvariable=today_float)
                float_t_entry_.configure(font=(font, 12), relief="solid", justify=CENTER)
                float_t_entry_.place(x=140, y=62)
                float_t_entry_.delete(0, END)

                def save_function():
                    try:
                        float_value = today_float.get()

                        conn = connect(path_to_database)
                        c = conn.cursor()
                        params2 = (float_value, current_time)
                        c.execute("INSERT INTO Costs VALUES (?, ?)", params2)
                        conn.commit()
                        conn.close()
                        cost_win.destroy()

                    except TclError:
                        messagebox.showwarning("Float Error", "Float should not be empty and must be a number")

                float_save_btn = Button(float_frame, command=save_function)
                float_save_btn.configure(text="SAVE", font=(font, 13), fg="white", bg="green", relief="solid")
                float_save_btn.place(x=250, y=120, width=70)

        def expense_section():
            expense_frame = Frame(cost_win)
            expense_frame.configure(width=360, height=200)
            expense_frame.place(x=20, y=70)
            expense_amount = DoubleVar()

            expense_label = Label(expense_frame)
            expense_label.configure(text="Description:", font=(font, 12, "bold"))
            expense_label.place(x=30, y=20)

            expense_t_entry = Entry(expense_frame)
            expense_t_entry.configure(font=(font, 12), relief="solid", justify=CENTER)
            expense_t_entry.place(x=140, y=22, width=189, height=60)

            expense_label_ = Label(expense_frame)
            expense_label_.configure(text="Amount:", font=(font, 12, "bold"))
            expense_label_.place(x=30, y=100)

            expense_t_entry_ = Entry(expense_frame, textvariable=expense_amount)
            expense_t_entry_.configure(font=(font, 12), relief="solid", justify=CENTER)
            expense_t_entry_.place(x=140, y=102)
            expense_t_entry_.delete(0, END)

            def save_function():
                try:
                    expense_description = expense_t_entry.get().strip()
                    expense_value = expense_amount.get()

                    conn = connect(path_to_database)
                    c = conn.cursor()
                    params2 = (expense_description, expense_value, current_time)
                    c.execute("INSERT INTO Expenses VALUES (?, ?, ?)", params2)
                    conn.commit()
                    conn.close()

                    expense_t_entry.delete(0, END)
                    expense_t_entry_.delete(0, END)

                except TclError:
                    messagebox.showwarning("Amount Error", "Expense amount should not be empty and must be a number")

            expense_save_btn = Button(expense_frame, command=save_function)
            expense_save_btn.configure(text="SAVE", font=(font, 13), fg="white", bg="green", relief="solid")
            expense_save_btn.place(x=170, y=150, width=70)

            def view_expenses():
                expense_window = Toplevel(cost_win)
                expense_window.geometry("700x600")
                expense_window.title("Expenses")
                expense_window.resizable(False, False)
                center(expense_window)

                db_connection = connect(path_to_database)
                writer = db_connection.cursor()
                lookup_command = "SELECT * FROM Expenses"
                writer.execute(lookup_command)
                result = writer.fetchall()
                db_connection.close()

                columns = ('Description', 'Amount', 'Date')
                style = Style()
                style.configure('Treeview.Heading', background="#3e3f3f", foreground='white', font=(font, 11, 'bold'),
                                relief='none')

                cart_table = Treeview(expense_window, columns=columns, show='headings')

                cart_table.heading("# 1", text='Description', anchor="w")
                cart_table.column("# 1", stretch=NO, minwidth=250, width=250, anchor="w")
                cart_table.heading("# 2", text='Amount', anchor="w")
                cart_table.column("# 2", stretch=NO, minwidth=150, width=150, anchor="w")
                cart_table.heading("# 3", text='Date', anchor="w")
                cart_table.column("# 3", stretch=NO, minwidth=200, width=200, anchor="w")

                cart_table.place(x=50, y=80, height=400)

                for i in range(0, len(result)):
                    cart_table.insert("", END, text="1", values=(result[i][0], result[i][1], "`" + result[i][2]))

                def export_to_csv():
                    desktop_location = path.join(path.join(path.expanduser('~')), 'Desktop')
                    filepath = filedialog.askdirectory(initialdir=r"{}".format(desktop_location),
                                                       title="Select File Path")

                    sales = []
                    for items in cart_table.get_children():
                        sales_displayed = cart_table.item(items)
                        sales.append(sales_displayed['values'])

                    display_time = strftime('%d-%B-%Y %H-%M-%S %p')

                    full_path = filepath + "/" + "Export data(" + display_time + ")" + ".csv"

                    headers = ['Description', 'Amount', 'Date']
                    sale_dataframe = pd.DataFrame(sales, columns=headers)
                    sale_dataframe.to_csv(full_path, index=False)
                    messagebox.showinfo("File Saved", "File was saved successfully to:\n"
                                                      "{}".format(full_path))

                export_btn = Button(expense_window, command=export_to_csv)
                export_btn.configure(text="Export", font=(font, 15, "bold"), fg="white", bg="blue", relief="solid")
                export_btn.place(x=490, y=520)

                def yesterday_sales():
                    today = datetime.datetime.today()
                    current_time = today.strftime("%d/%B/%Y")
                    yesterday_time = int((current_time[0] + current_time[1])) - 1
                    yesterday_dat = str(yesterday_time) + "/" + current_time[3:]

                    connection = connect(path_to_database)
                    write = connection.cursor()
                    lk_command = "SELECT * FROM Expenses WHERE Date LIKE '{}'".format(str(yesterday_dat) + "%")
                    write.execute(lk_command)
                    values = write.fetchall()
                    connection.close()

                    for it in cart_table.get_children():
                        cart_table.delete(it)

                    for i in range(0, len(values)):
                        cart_table.insert("", END, text="1", values=(values[i][0], values[i][1], values[i][2]))

                def today_sales():
                    today = datetime.datetime.today()
                    current_time = today.strftime("%d/%B/%Y")

                    connection = connect(path_to_database)
                    write = connection.cursor()
                    lk_command = "SELECT * FROM Expenses WHERE Date LIKE '{}'".format(str(current_time) + "%")
                    write.execute(lk_command)
                    values = write.fetchall()
                    connection.close()

                    for it in cart_table.get_children():
                        cart_table.delete(it)

                    for i in range(0, len(values)):
                        cart_table.insert("", END, text="1", values=(values[i][0], values[i][1], values[i][2]))

                def last7_days():
                    try:
                        for it in cart_table.get_children():
                            cart_table.delete(it)

                        def calculate_time(day_of_week):
                            connection = connect(path_to_database)
                            write = connection.cursor()
                            lk_command = "SELECT * FROM Expenses WHERE Date LIKE '{}'".format(day_of_week + "%")
                            write.execute(lk_command)
                            values = write.fetchall()
                            connection.close()

                            return values

                        week_data = []

                        for i in range(1, 7):
                            previous_date = datetime.datetime.today() - datetime.timedelta(days=i)
                            current_tim = previous_date.strftime("%d/%B/%Y")
                            week_values = calculate_time(current_tim)
                            week_data.append(week_values)

                        for i in range(0, len(week_data)):
                            for sub in week_data:
                                if sub:
                                    cart_table.insert("", END, text="1", values=(sub[i][0], sub[i][1], sub[i][2]))
                                else:
                                    pass

                    except IndexError:
                        pass

                def last_months():
                    last_month = datetime.datetime.now() - relativedelta(months=1)
                    last_month_day = format(last_month, '%B/%Y')

                    connection = connect(path_to_database)
                    write = connection.cursor()
                    lk_command = "SELECT * FROM Expenses WHERE Date LIKE '{}'".format(
                        "%" + last_month_day + "%")
                    write.execute(lk_command)
                    values = write.fetchall()
                    connection.close()

                    for it in cart_table.get_children():
                        cart_table.delete(it)

                    for i in range(0, len(values)):
                        cart_table.insert("", END, text="1", values=(values[i][0], values[i][1], values[i][2]))

                def this_months():
                    last_month = datetime.datetime.now() - relativedelta(months=0)
                    last_month_day = format(last_month, '%B/%Y')

                    connection = connect(path_to_database)
                    write = connection.cursor()
                    lk_command = "SELECT * FROM Expenses WHERE Date LIKE '{}'".format(
                        "%" + last_month_day + "%")
                    write.execute(lk_command)
                    values = write.fetchall()
                    connection.close()

                    for it in cart_table.get_children():
                        cart_table.delete(it)

                    for i in range(0, len(values)):
                        cart_table.insert("", END, text="1", values=(values[i][0], values[i][1], values[i][2]))

                def last_year():
                    last_month = datetime.datetime.now() - relativedelta(years=1)
                    last_month_day = format(last_month, '%Y')

                    connection = connect(path_to_database)
                    write = connection.cursor()
                    lk_command = "SELECT * FROM Expenses WHERE Date LIKE '{}'".format(
                        "%" + last_month_day + "%")
                    write.execute(lk_command)
                    values = write.fetchall()
                    connection.close()

                    for it in cart_table.get_children():
                        cart_table.delete(it)

                    for i in range(0, len(values)):
                        cart_table.insert("", END, text="1", values=(values[i][0], values[i][1], values[i][2]))

                def this_year():
                    today = datetime.datetime.today()
                    current_tim = today.strftime("%Y")

                    connection = connect(path_to_database)
                    write = connection.cursor()
                    lk_command = "SELECT * FROM Expenses WHERE Date LIKE '{}'".format("%" + current_tim + "%")
                    write.execute(lk_command)
                    values = write.fetchall()
                    connection.close()

                    for it in cart_table.get_children():
                        cart_table.delete(it)

                    for i in range(0, len(values)):
                        cart_table.insert("", END, text="1", values=(values[i][0], values[i][1], values[i][2]))

                chart_timeframe_value = StringVar()

                chart_timeframe = Combobox(expense_window, textvariable=chart_timeframe_value)
                chart_times = ["Yesterday", "Today", "Last 7 Days", "This Month", "Last Month", "This Year",
                               "Last Year"]
                chart_timeframe['values'] = chart_times
                chart_timeframe.configure(state="readonly", font=(font, 12))
                chart_timeframe.place(x=400, y=20)

                def load_respective_chart(*args):
                    if chart_timeframe_value.get() == chart_times[0]:
                        yesterday_sales()

                    elif chart_timeframe_value.get() == chart_times[1]:
                        today_sales()

                    elif chart_timeframe_value.get() == chart_times[2]:
                        last7_days()

                    elif chart_timeframe_value.get() == chart_times[3]:
                        this_months()

                    elif chart_timeframe_value.get() == chart_times[4]:
                        last_months()

                    elif chart_timeframe_value.get() == chart_times[5]:
                        this_year()

                    elif chart_timeframe_value.get() == chart_times[6]:
                        last_year()

                    else:
                        pass

                chart_timeframe_value.trace("w", load_respective_chart)

                def close_expense(event):
                    expense_window.destroy()

                expense_window.bind("KeyPress-Home>", close_expense)

            expense_view_btn = Button(expense_frame, command=view_expenses)
            expense_view_btn.configure(text="VIEW", font=(font, 13), fg="white", bg="blue", relief="solid")
            expense_view_btn.place(x=260, y=150, width=70)

        float_section()

        load_float = Button(cost_win, command=float_section)
        load_float.configure(text="FLOAT", font=(font, 12), relief="solid")
        load_float.place(x=50, y=10)

        load_expense = Button(cost_win, command=expense_section)
        load_expense.configure(text="EXPENSES", font=(font, 12), relief="solid")
        load_expense.place(x=130, y=10)

        def close_costs(event):
            cost_win.destroy()

        cost_win.bind("<KeyPress-Home>", close_costs)


def load_cashier_page():
    cashier_page = Tk()
    CashierPage(cashier_page)
    cashier_page.mainloop()


def load_admin_page():
    admin_page = Tk()
    AdminPage(admin_page)
    admin_page.mainloop()


def load_main_login_page():
    main_window = Tk()
    LoginMainPage(main_window)
    main_window.mainloop()


if __name__ == '__main__':
    load_main_login_page()

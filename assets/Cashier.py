import datetime
import time
from tkinter import TclError, NO, Checkbutton, END, DoubleVar
from tkinter import Tk, Label, Frame, Entry, Button, StringVar, CENTER, Toplevel, messagebox, IntVar
from tkinter.ttk import Combobox, Treeview, Style
from os import getcwd
from sqlite3 import connect
from ctypes import windll as window_dpi
from screeninfo import get_monitors
from Admin import load_admin

window_dpi.shcore.SetProcessDpiAwareness(True)

# ====================== Locating files and folders ============================
db_name = 'Qwe390snnskeyy46snckalkjdn872209102.db'
current_directory = getcwd()
path_to_icons = current_directory + '\\' + 'assets' + '\\' + 'icons' + '\\'
path_to_images = current_directory + '\\' + 'assets' + '\\' + 'images' + '\\'
path_to_database = current_directory + '\\' + 'assets' + '\\' + 'informational' + '\\' + db_name
account_types = ['Admin', 'Cashier']
tables = ['Users', 'Products', 'Sales', 'Transactions']
font = "yu gothic ui"


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


class CashierPage:
    def __init__(self, cashier_init):
        self.count = 0
        self.new_transaction_number = None
        self.total_pay = 0
        self.window_initializer = cashier_init
        new_quantity = IntVar()
        monitor = get_monitors()

        def widget_width(expected_value):
            monitor_width = monitor[0].width_mm
            window_width = self.window_initializer.winfo_screenwidth()
            resolution = window_width + (monitor_width/25.4)
            optimal_resolution = 1600 + (309/25.4)
            new_value = (resolution * expected_value)/optimal_resolution

            return int(round(new_value, 0))

        def widget_height(expected_value):
            monitor_height = monitor[0].height_mm
            window_height = self.window_initializer.winfo_screenheight()
            resolution = window_height + (monitor_height/25.4)
            optimal_resolution = 900 + (174/25.4)
            new_value = (resolution * expected_value)/optimal_resolution

            return int(round(new_value, 0))

        def font_adjust(expected_value):
            text_width = widget_width(expected_value=expected_value)
            text_height = widget_height(expected_value=expected_value)

            optimal_font = (text_width + text_height)/2

            return int(round(optimal_font))

        x = self.window_initializer.winfo_screenwidth()
        y = self.window_initializer.winfo_screenheight()
        self.window_initializer.geometry('{}x{}'.format(x, y))
        self.window_initializer.title("CASHIER ACCOUNT")
        self.window_initializer.state('zoomed')
        self.window_initializer.resizable(0, 1)

        self.cashier_waste_frame = Frame(self.window_initializer)
        self.cashier_waste_frame.configure(width=widget_width(380), height=widget_height(230), highlightbackground="black", highlightthickness=3)
        self.cashier_waste_frame.place(x=widget_width(50), y=widget_height(80))

        self.cashier_waste_label = Label(self.cashier_waste_frame)
        self.cashier_waste_label.configure(font=(font, font_adjust(14), "bold"), text="Select Stock:")
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
        self.cashier_waste_entry.configure(font=(font, font_adjust(12)), state='readonly', textvariable=stock_waste_var)
        self.cashier_waste_entry.place(x=widget_width(150), y=widget_height(23))

        self.cashier_waste_quan_label = Label(self.cashier_waste_frame)
        self.cashier_waste_quan_label.configure(font=(font, font_adjust(14), "bold"), text="Stock Quantity:")
        self.cashier_waste_quan_label.place(x=widget_width(5), y=widget_height(60))

        self.cashier_waste_quan_entry = Entry(self.cashier_waste_frame)
        self.cashier_waste_quan_entry.configure(font=(font, font_adjust(13)), justify=CENTER, state='disabled')
        self.cashier_waste_quan_entry.place(x=widget_width(150), y=widget_height(60))

        self.cashier_waste_amnt_label = Label(self.cashier_waste_frame)
        self.cashier_waste_amnt_label.configure(font=(font, font_adjust(14), "bold"), text="Waste Amount:")
        self.cashier_waste_amnt_label.place(x=widget_width(5), y=widget_height(100))

        waste_amnt = IntVar()
        self.cashier_waste_amnt_entry = Entry(self.cashier_waste_frame, textvariable=waste_amnt)
        self.cashier_waste_amnt_entry.configure(font=(font, font_adjust(13)), justify=CENTER)
        self.cashier_waste_amnt_entry.place(x=widget_width(150), y=widget_height(100))
        self.cashier_waste_amnt_entry.delete(0, END)

        self.waste_label = Label(self.window_initializer)
        self.waste_label.configure(text="Waste", font=(font, font_adjust(14), "bold"))
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
        self.cashier_update_waste.configure(text="UPDATE", font=(font, font_adjust(14)), relief='solid')
        self.cashier_update_waste.configure(command=update_waste)
        self.cashier_update_waste.place(x=widget_width(150), y=widget_height(160))

        self.cashier_cancel_waste = Button(self.cashier_waste_frame, bg='light yellow')
        self.cashier_cancel_waste.configure(text="CANCEL", font=(font, font_adjust(14)), relief='solid')
        self.cashier_cancel_waste.configure(command=waste_cancel)
        self.cashier_cancel_waste.place(x=widget_width(250), y=widget_height(160))

        self.cashier_update_frame = Frame(self.window_initializer)
        self.cashier_update_frame.configure(width=widget_width(369), height=widget_height(230), highlightbackground="black", highlightthickness=3)
        self.cashier_update_frame.place(x=widget_width(880), y=widget_height(80))

        self.cashier_update_product_code_label = Label(self.cashier_update_frame)
        self.cashier_update_product_code_label.configure(font=(font, font_adjust(14), "bold"), text="Product Code:")
        self.cashier_update_product_code_label.place(x=widget_width(5), y=widget_height(20))

        self.cashier_update_product_code = Entry(self.cashier_update_frame)
        self.cashier_update_product_code.configure(state='disabled', font=(font, font_adjust(14), "bold"), relief="solid")
        self.cashier_update_product_code.place(x=widget_width(133), y=widget_height(20))

        self.cashier_update_product_desc_label = Label(self.cashier_update_frame)
        self.cashier_update_product_desc_label.configure(font=(font, font_adjust(14), "bold"), text="Product Desc:")
        self.cashier_update_product_desc_label.place(x=widget_width(5), y=widget_height(60))

        self.cashier_update_product_desc = Entry(self.cashier_update_frame)
        self.cashier_update_product_desc.configure(state='disabled', font=(font, font_adjust(14), "bold"), relief="solid")
        self.cashier_update_product_desc.place(x=widget_width(133), y=widget_height(60))

        self.cashier_update_product_quan_label = Label(self.cashier_update_frame)
        self.cashier_update_product_quan_label.configure(font=(font, font_adjust(14), "bold"), text="Quantity:")
        self.cashier_update_product_quan_label.place(x=widget_width(40), y=widget_height(100))

        self.cashier_update_product_quan = Entry(self.cashier_update_frame, textvariable=new_quantity)
        self.cashier_update_product_quan.configure(font=(font, font_adjust(14), "bold"), relief="solid", justify=CENTER, state="disabled")
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
        self.cashier_update_button.configure(state='disabled', text="UPDATE", font=(font, font_adjust(14)), relief='solid')
        self.cashier_update_button.configure(command=update_quantity)
        self.cashier_update_button.place(x=widget_width(240), y=widget_height(160))

        self.cashier_cancel_button = Button(self.cashier_update_frame, bg='light yellow')
        self.cashier_cancel_button.configure(state='disabled', text="CANCEL", font=(font, font_adjust(14)), relief='solid')
        self.cashier_cancel_button.configure(command=change_quantity_cancel)
        self.cashier_cancel_button.place(x=widget_width(140), y=widget_height(160))

        self.change_quantity_label = Label(self.window_initializer)
        self.change_quantity_label.configure(text="Change Quantity", font=(font, font_adjust(14), "bold"))
        self.change_quantity_label.place(x=widget_width(930), y=widget_height(65))
        
        self.cashier_stock_frame = Frame(self.window_initializer)
        self.cashier_stock_frame.configure(width=widget_width(369), height=widget_height(230), highlightbackground="black", highlightthickness=3)
        self.cashier_stock_frame.place(x=widget_width(480), y=widget_height(80))

        self.cashier_stock_product_code_label = Label(self.cashier_stock_frame)
        self.cashier_stock_product_code_label.configure(font=(font, font_adjust(14), "bold"), text="Product Code:")
        self.cashier_stock_product_code_label.place(x=widget_width(5), y=widget_height(20))

        self.cashier_stock_product_code = Entry(self.cashier_stock_frame)
        self.cashier_stock_product_code.configure(state='disabled', font=(font, font_adjust(14), "bold"), relief="solid")
        self.cashier_stock_product_code.place(x=widget_width(133), y=widget_height(20))

        self.cashier_stock_product_desc_label = Label(self.cashier_stock_frame)
        self.cashier_stock_product_desc_label.configure(font=(font, font_adjust(14), "bold"), text="Product Desc:")
        self.cashier_stock_product_desc_label.place(x=widget_width(5), y=widget_height(60))

        self.cashier_stock_product_desc = Entry(self.cashier_stock_frame)
        self.cashier_stock_product_desc.configure(state='disabled', font=(font, font_adjust(14), "bold"), relief="solid")
        self.cashier_stock_product_desc.place(x=widget_width(133), y=widget_height(60))

        self.cashier_stock_product_quan_label = Label(self.cashier_stock_frame)
        self.cashier_stock_product_quan_label.configure(font=(font, font_adjust(14), "bold"), text="Current Stock:")
        self.cashier_stock_product_quan_label.place(x=widget_width(5), y=widget_height(100))

        self.cashier_stock_product_quan = Entry(self.cashier_stock_frame)
        self.cashier_stock_product_quan.configure(font=(font, font_adjust(14), "bold"), relief="solid", justify=CENTER, state="disabled")
        self.cashier_stock_product_quan.place(x=widget_width(133), y=widget_height(100))

        self.cashier_stock_product_new_label = Label(self.cashier_stock_frame)
        self.cashier_stock_product_new_label.configure(font=(font, font_adjust(14), "bold"), text="New Stock:")
        self.cashier_stock_product_new_label.place(x=widget_width(28), y=widget_height(140))

        cashier_new_stock = IntVar()

        self.cashier_stock_product_new = Entry(self.cashier_stock_frame, textvariable=cashier_new_stock)
        self.cashier_stock_product_new.configure(font=(font, font_adjust(14), "bold"), relief="solid", justify=CENTER, state="disabled")
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
                    lk_comm2 = "UPDATE stock SET stockindate='{}' WHERE description='{}'".format(current_time, stock_name)
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
        self.cashier_stock_button.configure(state='disabled', text="UPDATE", font=(font, font_adjust(11)), relief='solid')
        self.cashier_stock_button.configure(command=update_stock)
        self.cashier_stock_button.place(x=widget_width(260), y=widget_height(180))

        self.cashier_cancel_stock = Button(self.cashier_stock_frame, bg='light yellow')
        self.cashier_cancel_stock.configure(state='disabled', text="CANCEL", font=(font, font_adjust(11)), relief='solid')
        self.cashier_cancel_stock.configure(command=change_stock_cancel)
        self.cashier_cancel_stock.place(x=widget_width(180), y=widget_height(180))

        self.change_stock_label = Label(self.window_initializer)
        self.change_stock_label.configure(text="Add Stock", font=(font, font_adjust(14), "bold"))
        self.change_stock_label.place(x=widget_width(530), y=widget_height(65))

        self.banner_frame = Frame(self.window_initializer)
        self.banner_frame.configure(background="#0b2971", height=widget_height(50), width=x)
        self.banner_frame.place(x=0, y=0)

        self.banner_frame_text = Label(self.banner_frame, bg='#0b2971')
        self.banner_frame_text.configure(text="HUDUMIA CYBER POS TERMINAL", font=(font, font_adjust(18), 'bold'), fg='white')
        self.banner_frame_text.place(x=x/2-200, y=widget_height(7))

        # =================================== Bottom Panel =========================================
        self.bottom_frame = Frame(self.window_initializer)
        self.bottom_frame.configure(bg='#30475c', height=widget_height(50), width=x)
        self.bottom_frame.place(x=0, y=widget_height(788))
        self.after_id = None

        def present_time():
            display_time = time.strftime('%d-%B-%Y %H:%M:%S %p')
            self.clock_label.config(text=display_time)
            self.after_id = self.clock_label.after(1000, present_time)

        self.clock_label = Label(self.bottom_frame, fg="white", bg="#30475c")
        self.clock_label.configure(font=(font, font_adjust(14)))
        self.clock_label.place(x=widget_width(1270), y=widget_height(7))

        present_time()

        self.sales_count_label = Label(self.bottom_frame, fg="white", bg="#30475c")
        self.sales_count_label.configure(text="Today's Sales:", font=(font, font_adjust(13)))
        self.sales_count_label.place(x=widget_width(950), y=widget_height(8))

        self.sales_count = Label(self.bottom_frame, fg="white", bg="#30475c")
        self.sales_count.configure(text=0, font=(font, font_adjust(13)))
        self.sales_count.place(x=widget_width(1060), y=widget_height(8))

        self.sales_label = Label(self.bottom_frame, fg="white", bg="#30475c")
        self.sales_label.configure(text="Sales: ", font=(font, font_adjust(13)))
        self.sales_label.place(x=widget_width(1125), y=widget_height(8))

        self.sales_amount = Label(self.bottom_frame, fg="white", bg="#30475c")
        self.sales_amount.configure(text=0, font=(font, font_adjust(13)))
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
        self.transaction.configure(text='TRANSACTION NO:', font=(font, font_adjust(11), 'bold'), fg='white', bg='#058de2')
        self.transaction.place(x=widget_width(10), y=widget_height(10))

        self.transaction_count = Label(self.transaction_count_frame)
        self.transaction_count.configure(text='000000000000', font=(font, font_adjust(18), 'bold'), fg='white',
                                         bg='#058de2')
        self.transaction_count.place(x=widget_width(65), y=widget_height(40))

        self.new_transaction_btn = Button(self.right_frame, font=(font, font_adjust(14), 'bold'),
                                          command=self.new_transaction_function)
        self.new_transaction_btn.configure(text='[F1] NEW TRANSACTION', fg='white', bg='#00ab78', relief='ridge', height=widget_height(2))
        self.new_transaction_btn.place(x=widget_width(22), y=widget_height(280), width=widget_width(290))

        self.add_to_cart_btn = Button(self.right_frame, font=(font, font_adjust(14), 'bold'))
        self.add_to_cart_btn.configure(text='[F2] ADD TO CART', fg='white', bg='#058de2', relief='ridge', height=widget_height(2))
        self.add_to_cart_btn.config(state='disabled', command=self.add_to_cart_function)
        self.add_to_cart_btn.place(x=widget_width(22), y=widget_height(360), width=widget_width(290))

        self.delete_cart_item_btn = Button(self.right_frame, font=(font, font_adjust(14), 'bold'))
        self.delete_cart_item_btn.configure(text='[DEL] DELETE ITEM', fg='white', bg='#058de2', relief='ridge', height=widget_height(2))
        self.delete_cart_item_btn.config(state='disabled', command=self.delete_cart_item)
        self.delete_cart_item_btn.place(x=widget_width(22), y=widget_height(440), width=widget_width(290))

        self.clear_cart_btn = Button(self.right_frame, font=(font, font_adjust(14), 'bold'))
        self.clear_cart_btn.configure(text='[END] CLEAR CART', fg='white', bg='#058de2', relief='ridge', height=widget_height(2))
        self.clear_cart_btn.config(state='disabled', command=self.clear_cart)
        self.clear_cart_btn.place(x=widget_width(22), y=widget_height(520), width=widget_width(290))

        self.payment_btn = Button(self.right_frame, font=(font, font_adjust(14), 'bold'))
        self.payment_btn.configure(text='[F12] MAKE PAYMENT', fg='white', bg='#058de2', relief='ridge', height=widget_height(2))
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
        style.configure('Treeview.Heading', background="#3e3f3f", foreground='white', font=(font, font_adjust(16), 'bold'),
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

        self.cart_table.place(x=0, y=widget_width(330), height=widget_height(405))

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
            window_debt.geometry("900x550")
            center(window_debt)
            search_value = StringVar()

            search_label = Label(window_debt)
            search_label.configure(font=(font, 13), text="Search Name:")
            search_label.place(x=widget_width(430), y=widget_height(35))

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
            cart_table.column("# 1", stretch=NO, minwidth=widget_width(150), width=widget_width(150),
                                   anchor=CENTER)
            cart_table.heading("# 2", text='Name', anchor="w")
            cart_table.column("# 2", stretch=NO, minwidth=widget_width(150), width=widget_width(150), anchor="w")
            cart_table.heading("# 3", text='Contact', anchor=CENTER)
            cart_table.column("# 3", stretch=NO, minwidth=widget_width(150), width=widget_width(150),
                                   anchor=CENTER)
            cart_table.heading("# 4", text='Debt Amount', anchor=CENTER)
            cart_table.column("# 4", stretch=NO, minwidth=widget_width(150), width=widget_width(150),
                                   anchor=CENTER)
            cart_table.heading("# 5", text='Date', anchor=CENTER)
            cart_table.column("# 5", stretch=NO, minwidth=widget_width(200), width=widget_width(200),
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
                                      values=(result[i][0], result[i][1] + ", " + result[i][2], result[i][3], result[i][4], result[i][5]))

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
                                lk_comm = "UPDATE debts SET debtamount='{}' WHERE TransactionId='{}'".format(new_debt, items[0])
                                lk_comm2 = "UPDATE debts SET date='{}' WHERE TransactionId='{}'".format(current_time, items[0])
                                lk_comm3 = "UPDATE Transactions SET debt='{}' WHERE TransactionId='{}'".format(new_debt, items[0])
                                lk_comm4 = "UPDATE Transactions SET AmountPaid='{}' WHERE TransactionId='{}'".format(new_paid_amount, items[0])
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
                            lk_comm = "UPDATE Transactions SET AmountPaid='{}' WHERE TransactionId='{}'".format(full_settle, items[0])
                            lk_comm2 = "UPDATE Transactions SET CashAmount='{}' WHERE TransactionId='{}'".format(0.0, items[0])
                            lk_comm3 = "UPDATE Transactions SET debt='{}' WHERE TransactionId='{}'".format(0.0, items[0])
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
                            lk_comm = "UPDATE Transactions SET AmountPaid='{}' WHERE TransactionId='{}'".format(full_settle, items[0])
                            lk_comm3 = "UPDATE Transactions SET debt='{}' WHERE TransactionId='{}'".format(0.0, items[0])
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
                            lk_comm = "UPDATE Transactions SET AmountPaid='{}' WHERE TransactionId='{}'".format(full_settle, items[0])
                            lk_comm2 = "UPDATE Transactions SET ModeofPayment='{}' WHERE TransactionId='{}'".format("cash", items[0])
                            lk_comm3 = "UPDATE Transactions SET debt='{}' WHERE TransactionId='{}'".format(0.0, items[0])
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
                        messagebox.showwarning("Error", "Paid full checkbox cannot be selected when amount is not empty")
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
            load_admin()

        def load_admin_window(event):
            admin_win()

        self.window_initializer.bind("<KeyPress-F11>", load_admin_window)

        self.admin_page = Button(self.banner_frame, fg="white", bg="#0b2971", command=admin_win)
        self.admin_page.configure(text="Admin", font=(font, font_adjust(13)), relief="solid")
        self.admin_page.place(x=widget_width(1400), y=widget_height(5))

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
                                    lk_command = "SELECT quantity FROM {} WHERE {}='{}'".format("stock", field, str(value))
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
                                    messagebox.showwarning("Low quantity", "Cannot update quantity for {} due to low quantity\n"
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
                                            len(first_name_value.get().strip()) >= 3 and mpesa_amount.get().strip() != ""\
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
                                                       contact_number_value.get().strip(), float(debt_in.get()), current_time)
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
                            amount = float(paid_amount.get().strip()) - (self.total_pay - float(cash_discount.get().strip()))
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
                                    if first_name_value.get().strip() != "" and contact_number_value.get().strip() != "" and len(contact_number_value.get().strip()) > 3 and len(first_name_value.get().strip()) >= 2:
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
                                            self.new_transaction_number, current_time, number_of_items, self.total_pay,
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
                                        pen_cash, discount, 0.0,float(debt_in.get().strip()), "debt")
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


def load_cashier_window():
    cashier_page = Tk()
    CashierPage(cashier_page)
    cashier_page.mainloop()


if __name__ == '__main__':
    load_cashier_window()

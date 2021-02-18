from tkinter import *
from tkinter import ttk

from config.config import user, password
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

class workOrder:
    def __init__(self, wo):
        
        self.root = Tk()
        self.root.title('WorkOrder --- TreeView')
        self.root.geometry("700x550")
        self.PATH = '/Users/juansantos/Documents/GitHub/FIIX-data-scanner/driver/chromedriver'
        self.count = 0

        # Encabezado
        self.label = Label(self.root, text=wo.name)
        self.label.config(
            fg="white",
            bg="darkgray",
            font=("Sans serif", 25),
            padx=10,
            pady=10
        )

        self.label.place(x=350, y=25, anchor='center')
        
        # Label static 
        self.status = Label(self.root, text='Status:')
        self.status.config(
            fg="black",
            font=("Sans serif", 13)
        )
        self.status.place(x=35, y=75, anchor='center')

        self.type = Label(self.root, text='Type:')
        self.type.config(
            fg="black",
            font=("Sans serif", 13)
        )
        self.type.place(x=250, y=75, anchor='center')

        self.priority = Label(self.root, text='Priority:')
        self.priority.config(
            fg="black",
            font=("Sans serif", 13)
        )
        self.priority.place(x=430, y=75, anchor='center')

        # Label dinamic
        self.statusTxt = Label(self.root, text=wo.woStatus)
        self.statusTxt.config(
            fg="black",
            font=("Sans serif", 15)
        )
        self.statusTxt.place(x=150, y=75, anchor='center')

        self.typeTxt = Label(self.root, text=wo.woType)
        self.typeTxt.config(
            fg="black",
            font=("Sans serif", 15)
        )
        self.typeTxt.place(x=340, y=75, anchor='center')

        self.priorityTxt = Label(self.root, text=wo.woPriority)
        self.priorityTxt.config(
            fg="black",
            font=("Sans serif", 15)
        )
        self.priorityTxt.place(x=510, y=75, anchor='center')

        self.my_tree = ttk.Treeview(self.root)

        # Define Our Columns
        self.my_tree['columns'] = ("Part Name", "Part#", "Qty")

        # Formate Our Columns
        self.my_tree.column("#0", width=0, stretch=NO)
        self.my_tree.column("Part Name", anchor=W, width=300)
        self.my_tree.column("Part#", anchor=CENTER, width=80)
        self.my_tree.column("Qty", anchor=W, width=50)

        # Make Headings
        self.my_tree.heading("#0", text="", anchor=W)
        self.my_tree.heading("Part Name", text="Part Name", anchor=W)
        self.my_tree.heading("Part#", text="Part#", anchor=CENTER)
        self.my_tree.heading("Qty", text="Qty", anchor=W)

        # Insert Data
        # my_tree.insert(parent='', index='end', iid=0, text='', values=('Bearing FL207', 'A4876', 2))

        self.my_tree.bind('<Button-1>', self.seletionData)
        # Pack to screen
        self.my_tree.pack(pady=100)

        self.Name = Label(self.root, text='Name')
        self.Name.config(
            fg="black",
            font=("Sans serif", 13)
        )
        self.Name.place(x=200, y=340, anchor='center')

        self.partNo = Label(self.root, text='Part#')
        self.partNo.config(
            fg="black",
            font=("Sans serif", 13)
        )
        self.partNo.place(x=430, y=340, anchor='center')

        self.qty = Label(self.root, text='Quantity')
        self.qty.config(
            fg="black",
            font=("Sans serif", 13)
        )
        self.qty.place(x=550, y=340, anchor='center')

        # Update Data
        self.txtName = Entry(self.root, width=30)
        self.txtName.config(
            state=DISABLED,
            fg="black",
            font=("Sans serif", 13)
        )
        self.txtName.place(x=200, y=370, anchor='center')

        self.txtpartNo = Entry(self.root, width=10)
        self.txtpartNo.config(
            state=DISABLED,
            fg="black",
            font=("Sans serif", 13)
        )
        self.txtpartNo.place(x=430, y=370, anchor='center')

        self.txtqty = Entry(self.root, width=5)
        self.txtqty.config(
            fg="black",
            font=("Sans serif", 13)
        )
        self.txtqty.place(x=550, y=370, anchor='center')

        # buttons
        self.btnUpdate = Button(self.root, text='Update', command= self.update, width=10, height=2)
        self.btnUpdate.place(x=240, y=430, anchor='center')

        self.btnDelete = Button(self.root, text='Delete', command= self.delete, width=10, height=2)
        self.btnDelete.place(x=360, y=430, anchor='center')

        self.btnSave = Button(self.root, text='Close and Save', command= self.closeAndSave, width=15, height=2)
        self.btnSave.place(x=550, y=430, anchor='center')

        # Scan parts
        self.txtPartUrl = Entry(self.root, width=30)
        self.txtPartUrl.config(
            fg="black",
            font=("Sans serif", 13)
        )
        self.txtPartUrl.place(x=200, y=500, anchor='center')
        self.txtPartUrl.bind('<Return>', self.scan)

        self.btnScan = Button(self.root, text='Scan Part', command= self.scan, width=10, height=2)
        self.btnScan.place(x=440, y=500, anchor='center')

        self.root.mainloop()

    def seletionData(self, event=''):
        self.txtName.config(
                state=NORMAL
            )
        self.txtName.delete(0, END)
        self.txtName.config(
                state=DISABLED
            )
        self.txtpartNo.config(
                state=NORMAL
            )
        self.txtpartNo.delete(0, END)
        self.txtpartNo.config(
                state=DISABLED
            )
        self.txtqty.delete(0, END)

        selected = self.my_tree.focus()

        if selected:
            values = self.my_tree.item(selected, 'values')

            self.txtName.config(
                state=NORMAL
            )
            self.txtName.insert(0, values[0])
            self.txtName.config(
                state=DISABLED
            )
            self.txtpartNo.config(
                state=NORMAL
            )
            self.txtpartNo.insert(0, values[1])
            self.txtpartNo.config(
                state=DISABLED
            )
            self.txtqty.insert(0, values[2])

    def obtDriver(self, url=''):

        opt =  Options()
        opt.add_argument('--headless')

        driver = webdriver.Chrome(self.PATH, chrome_options=opt)
        driver.get(url)
        j_username = driver.find_element_by_name('j_username')
        j_username.send_keys(user)
        j_password = driver.find_element_by_name('j_password')
        j_password.send_keys(password)
        j_password.submit()

        return driver

    def scan(self, event=''):
        timeWait = 5

        try:
            if 'https://windset.macmms.com/?a=' in self.txtPartUrl.get():
                driver = self.obtDriver(self.txtPartUrl.get())

                element_present = ec.presence_of_element_located((By.CSS_SELECTOR, ".maFormNew"))
                WebDriverWait(driver, timeWait).until(element_present)

                idMain = driver.find_element_by_css_selector('.maFormNew').get_attribute('id')

                element_present = ec.presence_of_element_located((By.CSS_SELECTOR, ".graingerNameFld"))
                WebDriverWait(driver, timeWait).until(element_present)

                name = driver.find_element_by_css_selector('.graingerNameFld').get_attribute('value')

                element_present = ec.presence_of_element_located((By.CSS_SELECTOR, f"#{idMain}_column_strCode_cell .formCellInside35 input"))
                WebDriverWait(driver, timeWait).until(element_present)

                partNo = driver.find_element_by_css_selector(f'#{idMain}_column_strCode_cell .formCellInside35 input').get_attribute('value')

                self.my_tree.insert(parent='', index='end', iid=self.count, text='', values=(name, partNo, 1))
                self.count += 1

                driver.close()
        except TimeoutException:
            print(f"Exception: {TimeoutException}")
        finally:
            self.txtPartUrl.delete(0, END)

    def update(self):
        selected = self.my_tree.focus()

        self.my_tree.item(selected, text='', values=(self.txtName.get(), self.txtpartNo.get(), self.txtqty.get()))

        self.txtName.config(
                state=NORMAL
            )
        self.txtName.delete(0, END)
        self.txtName.config(
                state=DISABLED
            )
        self.txtpartNo.config(
                state=NORMAL
            )
        self.txtpartNo.delete(0, END)
        self.txtpartNo.config(
                state=DISABLED
            )
        self.txtqty.delete(0, END)

    def delete(self):
        x = self.my_tree.selection()

        for record in x:
            self.my_tree.delete(record)
        

    def closeAndSave(self):

        pass
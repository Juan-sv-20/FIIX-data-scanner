from tkinter import Tk, Label, Button, Entry, END
from tkinter.messagebox import showinfo
import time
from config.config import user, password
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class Program:
    def __init__(self):
        self.title = 'Fiix-Scanner'
        self.size = '400x200'
        self.resizable = False
        self.PATH = '/Users/juansantos/Desktop/Python/interfaz-Fiix-scaner/driver/chromedriver'
    
    def obtDriver(self, url=''):

        self.driver = webdriver.Chrome(self.PATH)
        self.driver.get(self.txtScanner.get())
        j_username = self.driver.find_element_by_name('j_username')
        j_username.send_keys(user)
        j_password = self.driver.find_element_by_name('j_password')
        j_password.send_keys(password)
        j_password.submit()

        time.sleep(1)

    def obtPrice(self):
        # e10twf T4OwTb
        # e10twf T4OwTb
    
        url = f'https://www.google.com/'

        driver = webdriver.Chrome(self.PATH)
        driver.get(url)
        
        buscador = driver.find_element_by_name('q')
        buscador.send_keys(self.nameSupplie)
        buscador.submit()

        prices = driver.find_elements_by_css_selector('.e10twf')
        if len(prices) > 0:
            self.price = prices[0].text
        
        driver.close()


    def openTabWO(self):

        self.obtDriver()

        table = self.driver.find_element_by_css_selector('.formTabs35 ul').get_attribute('id')

        id = table.find('_')
        table = table[:id]

        part_seccion = self.driver.find_element_by_css_selector(f'.formTabs35 ul #{table}_tabPage_Parts')

        part_seccion.click()
    
    def openTabSupplie(self):

        self.obtDriver()

        id = self.driver.find_element_by_class_name('maFormNew').get_attribute('id')

        self.idSupplie = self.driver.find_element_by_css_selector(f'#{id}_column_strCode_cell .formCellInside35 input').get_attribute('value')
        
        self.nameSupplie = self.driver.find_element_by_css_selector(f'#{id}_column_strName_cell .formExtraLarge div .graingerNameFld').get_attribute('value')
        
        self.qtyOnHand = self.driver.find_element_by_id(f'{id}_isl').text

        self.driver.close()

        self.obtPrice()

        showinfo(title='Informacion sobre el Supplie', message=f"""
        Supplie name: {self.nameSupplie}\n
        Code: {self.idSupplie}\n
        Qty on hand: {self.qtyOnHand}\n
        Price: {self.price}\n
        """)

    def verificar(self, event=''):
        if 'https://windset.macmms.com/?wo=' in self.txtScanner.get():
            self.openTabWO()

        elif 'https://windset.macmms.com/?a=' in self.txtScanner.get():
            self.openTabSupplie()
        else:
            showinfo(title='Error al escanear', message='No se reconoce el codigo ingresado')
        self.txtScanner.delete(0, END)
        self.txtScanner.focus()

    def load(self):
        # Crear ventana raiz
        self.ventana = Tk()

        # Titulo de la ventana
        self.ventana.title(self.title)

        # Cambio en el tamaño de la ventana
        self.ventana.geometry(self.size)

        # Bloquear el tamaño de la ventana
        if self.resizable:
            self.ventana.resizable(1, 1)
        else:
            self.ventana.resizable(0, 0)

        self.ventana.config(
            bg="darkgray"
        )

        # Encabezado
        self.label = Label(self.ventana, text='API TO FIIX-SCANNER')
        self.label.config(
            fg="white",
            bg="darkgray",
            font=("Sans serif", 25),
            padx=10,
            pady=10
        )

        self.label.place(x=200, y=25, anchor='center')

        # Label del escaner
        self.lblScanner = Label(self.ventana, text='Escanee la pieza o orden a verificar:')
        self.lblScanner.config(
            fg="white",
            bg="darkgray",
            font=("Sans serif", 15)
        )
        self.lblScanner.place(x=200, y=90, anchor='center')

        # Campo de texto
        self.txtScanner = Entry(self.ventana)
        self.txtScanner.place(x=200, y=120, anchor='center')
        self.txtScanner.bind('<Return>', self.verificar)
        self.txtScanner.focus()

        # Button submit()
        self.btnEnter = Button(self.ventana, text='Verificar', command= self.verificar)
        self.btnEnter.place(x=200, y=150, anchor='center')

        # Arrancar y mostrar la ventana hasta que se cierre
        self.ventana.mainloop()

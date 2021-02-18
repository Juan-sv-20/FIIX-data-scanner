from tkinter import Tk, Label, Button, Entry, END
from tkinter.messagebox import showinfo
import time
from config.config import user, password
from selenium import webdriver
from msedge.selenium_tools import EdgeOptions
from msedge.selenium_tools import Edge
from selenium.webdriver import ActionChains

class Program:
    # Constructor
    def __init__(self):
        self.title = 'Fiix-Scanner'
        self.size = '400x200'
        self.resizable = False
        self.PATH = 'driver\msedgedriver.exe'
        self.woOpen = False
        self.addComponentBefore = False
        self.edge_options = EdgeOptions()
        self.edge_options.use_chromium = True  # if we miss this line, we can't make Edge headless
        # A little different from Chrome cause we don't need two lines before 'headless' and 'disable-gpu'
        self.edge_options.add_argument('headless')
        self.edge_options.add_argument('disable-gpu')
    
    # Method to obtain the driver to navigate inside it
    def obtDriver(self, url=''):
        
        # Open driver with Chromedriver
        driver = Edge(executable_path=self.PATH, options=self.edge_options)
        # driver = Edge(executable_path=self.PATH)
        # Open Url on driver
        driver.get(self.txtScanner.get())

        # Initialize session with the TOKEN's 
        j_username = driver.find_element_by_name('j_username')
        j_username.send_keys(user)
        j_password = driver.find_element_by_name('j_password')
        j_password.send_keys(password)
        j_password.submit()

        # Return the driver initialized
        return driver
    
    # Method to obtain a price depend only for its name
    def obtPrice(self):
        
        # URL
        url = f'https://www.google.com/'

        # Open driver with Chromedriver
        driver = Edge(executable_path=self.PATH, options=self.edge_options)
        # Open URL on driver
        driver.get(url)
        
        # Find the search text input and send the componento find
        buscador = driver.find_element_by_name('q')
        buscador.send_keys(self.nameSupplie)
        buscador.submit()

        # Obtaining the price from the ADS
        prices = driver.find_elements_by_css_selector('.e10twf')
        if len(prices) > 0:
            self.price = prices[0].text
        
        driver.close()

    def openTabWO(self):

        # Get the driver primary
        self.driverWo = self.obtDriver()

        # Flags
        self.addComponentBefore = False
        self.woOpen = True

        time.sleep(2)

        # Find the ID 
        id = self.driverWo.find_element_by_class_name('maFormNew').get_attribute('id')

        part_seccion = self.driverWo.find_element_by_id(f'{id}_tabPage_Parts')

        part_seccion.click()
    
    def addComponentToOrder(self):
        idWindowAddContainer = self.driverWo.find_element_by_class_name('modalWindowFrame').get_attribute('id')

        idAdd = self.driverWo.find_element_by_css_selector(f'#{idWindowAddContainer}_innerDiv .listLargeMain').get_attribute('id')

        inputSearch = self.driverWo.find_element_by_id(f'{idAdd}_search____searchtermparameter')
        inputSearch.clear()
        inputSearch.send_keys(self.idSupplie)
            
        btnSearch = self.driverWo.find_element_by_css_selector('.listSearchLarge div')
        btnSearch.click()

        self.addComponentBefore = True

    def openTabSupplie(self):

        driver = self.obtDriver()

        time.sleep(3)
        
        id = driver.find_element_by_class_name('maFormNew').get_attribute('id')

        self.idSupplie = driver.find_element_by_css_selector(f'#{id}_column_strCode_cell .formCellInside35 input').get_attribute('value')
        
        if self.woOpen:
            driver.close()

            if self.addComponentBefore == False:
                idContainer = self.driverWo.find_elements_by_class_name('listLargeMain')
                id = idContainer[1].get_attribute('id')

                buttonAdd = self.driverWo.find_element_by_css_selector(f'#{id}_ft .listPagingContainer35 span')
                buttonAdd.click()

                time.sleep(1)

            self.addComponentToOrder()

            return 0

        self.nameSupplie = driver.find_element_by_css_selector(f'#{id}_column_strName_cell .formExtraLarge div .graingerNameFld').get_attribute('value')
        
        self.qtyOnHand = driver.find_element_by_id(f'{id}_isl').text

        self.price = driver.find_element_by_css_selector(f'#{id}_column_dblLastPrice_cell .formCellInside35 input').get_attribute('value')

        print(f'Precio del FIIX: {self.price}')
        if self.price == '':
            self.obtPrice()

        priceOnFiixUpdate = driver.find_element_by_css_selector(f'#{id}_column_dblLastPrice_cell .formCellInside35 input')

        self.price = self.price.replace('USD', '')
        self.price = self.price.replace('$', '')
        
        priceOnFiixUpdate.send_keys(self.price.strip())
        buttonSave = driver.find_element_by_class_name('saveButtonAct').click()

        ActionChains(driver).click(buttonSave).perform()
        # buttonSave.click()

        time.sleep(2)

        driver.close()

        print(f'\n\n\n\n\n\n\n\nEl precio se actualizo... del producto: {self.nameSupplie}\n\n\n\n\n\n\n\n\n')
        # showinfo(title='Informacion sobre el Supplie', message=f"""
        # Supplie name: {self.nameSupplie}\n
        # Code: {self.idSupplie}\n
        # Qty on hand: {self.qtyOnHand}\n
        # Price: USD {self.price}\n
        # """)

    def verificar(self, event=''):
        # self.ventana.iconify()
        if 'https://windset.macmms.com/?wo=' in self.txtScanner.get():
            self.openTabWO()

        elif 'https://windset.macmms.com/?a=' in self.txtScanner.get():
            self.openTabSupplie()
        else:
            showinfo(title='Error al escanear', message='No se reconoce el codigo ingresado')

        # self.ventana.deiconify()
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

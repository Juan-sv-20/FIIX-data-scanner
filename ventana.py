from tkinter import Tk, Label, Button, Entry, END
from tkinter.constants import X
from tkinter.messagebox import showinfo
import time

from config.config import user, password
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

import wo
import workOrderDisplay

class Program:
    def __init__(self):
        self.title = 'Fiix-Scanner'
        self.size = '400x200'
        self.resizable = False
        self.PATH = '/Users/juansantos/Documents/GitHub/FIIX-data-scanner/driver/chromedriver'
        self.woOpen = False
        self.addComponentBefore = False
    
    def obtDriver(self, url=''):

        opt =  Options()
        opt.add_argument('--headless')

        driver = webdriver.Chrome(self.PATH, chrome_options=opt)
        driver.get(self.txtScanner.get())
        j_username = driver.find_element_by_name('j_username')
        j_username.send_keys(user)
        j_password = driver.find_element_by_name('j_password')
        j_password.send_keys(password)
        j_password.submit()

        return driver

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

        self.driverWo = self.obtDriver()

        # Flags
        self.addComponentBefore = False
        self.woOpen = True

        timeWait = 5

        try:
            element_present = ec.presence_of_element_located((By.CSS_SELECTOR, ".contentPaneFrameStacked .maFormNew"))
            WebDriverWait(self.driverWo, timeWait).until(element_present)

            idMain = self.driverWo.find_element_by_css_selector('.contentPaneFrameStacked .maFormNew').get_attribute('id')

            print(idMain)
            try:

                element_present = ec.presence_of_element_located((By.ID, f"{idMain}_label"))
                WebDriverWait(self.driverWo, timeWait).until(element_present)

                self.woName = self.driverWo.find_element_by_id(f'{idMain}_label').text
                self.woName = self.woName.replace('Work Order Administration: ', '')

            except TimeoutException:
                print("woName Not Loaded")
            finally:
                print("woName Loaded")

            try:
                element_present = ec.presence_of_element_located((By.CSS_SELECTOR, f"#{idMain}_column_intWorkOrderStatusID_cell .formCellInside35 .autoSuggestDropdownContainer35"))
                WebDriverWait(self.driverWo, timeWait).until(element_present)

                idSelector = self.driverWo.find_element_by_css_selector(f"#{idMain}_column_intWorkOrderStatusID_cell .formCellInside35 .autoSuggestDropdownContainer35").get_attribute('id')
                idSelector = idSelector.replace('_oe', '')

                try:
                    element_present = ec.presence_of_element_located((By.ID, f"{idSelector}_oit"))
                    WebDriverWait(self.driverWo, timeWait).until(element_present)

                    self.woStatus = self.driverWo.find_element_by_id(f'{idSelector}_oit').get_attribute('value')

                except TimeoutException:
                    print("woStatus Not Loaded")
                finally:
                    print("woStatus Loaded")
            except TimeoutException:
                print("idSelector Not Loaded")
            finally:
                print("idSelector Loaded")

            try:
                element_present = ec.presence_of_element_located((By.CSS_SELECTOR, f"#{idMain}_column_intMaintenanceTypeID_cell .formCellInside35 .autoSuggestDropdownContainer35"))
                WebDriverWait(self.driverWo, timeWait).until(element_present)

                idSelector = self.driverWo.find_element_by_css_selector(f"#{idMain}_column_intMaintenanceTypeID_cell .formCellInside35 .autoSuggestDropdownContainer35").get_attribute('id')
                idSelector = idSelector.replace('_oe', '')

                try:
                    element_present = ec.presence_of_element_located((By.ID, f"{idSelector}_oit"))
                    WebDriverWait(self.driverWo, timeWait).until(element_present)

                    self.woType = self.driverWo.find_element_by_id(f'{idSelector}_oit').get_attribute('value')

                except TimeoutException:
                    print("woType Not Loaded")
                finally:
                    print("woType Loaded")
            except TimeoutException:
                print("idSelector Not Loaded")
            finally:
                print("idSelector Loaded")

            try:
                element_present = ec.presence_of_element_located((By.CSS_SELECTOR, f"#{idMain}_column_intPriorityID_cell .formCellInside35 .autoSuggestDropdownContainer35"))
                WebDriverWait(self.driverWo, timeWait).until(element_present)

                idSelector = self.driverWo.find_element_by_css_selector(f"#{idMain}_column_intPriorityID_cell .formCellInside35 .autoSuggestDropdownContainer35").get_attribute('id')
                idSelector = idSelector.replace('_oe', '')

                try:
                    element_present = ec.presence_of_element_located((By.ID, f"{idSelector}_oit"))
                    WebDriverWait(self.driverWo, timeWait).until(element_present)

                    self.woPriority = self.driverWo.find_element_by_id(f'{idSelector}_oit').get_attribute('value')

                except TimeoutException:
                    print("woPriority Not Loaded")
                finally:
                    print("woPriority Loaded")
            except TimeoutException:
                print("idSelector Not Loaded")
            finally:
                print("idSelector Loaded")
            
            try:
                element_present = ec.presence_of_element_located((By.CSS_SELECTOR, f"#{idMain}_column_strDescription_cell div textarea"))
                WebDriverWait(self.driverWo, timeWait).until(element_present)

                self.woSummary = self.driverWo.find_element_by_css_selector(f"#{idMain}_column_strDescription_cell div textarea").text

            except TimeoutException:
                print("woSummary Not Loaded")
            finally:
                print("woSummary Loaded")

        except TimeoutException:
            print("Timed out waiting for page to load")
        finally:
            print("All loaded")

        try:
            element_present = ec.presence_of_element_located((By.CSS_SELECTOR, f"#{idMain}_tabPage_Parts"))
            WebDriverWait(self.driverWo, timeWait).until(element_present)

            btnPart = self.driverWo.find_element_by_css_selector(f"#{idMain}_tabPage_Parts")
            btnPart.click()

        except TimeoutException:
            print("")
        finally:
            print("")

        wOrder = wo.wo(self.woName, self.woStatus, self.woType, self.woPriority, self.woSummary, self.driverWo)

        woDisplay = workOrderDisplay.workOrder(wOrder)

        # idMain = WebDriverWait(self.driverWo, 10).until(ec.presence_of_element_located((By.CSS_SELECTOR, '.contentPaneFrameStacked .maFormNew')))
        # idMain = self.driverWo.find_element_by_css_selector('.contentPaneFrameStacked .maFormNew').get_attribute('id')
        # woName = self.driverWo.find_element_by_id(f'{idMain}_label').text
        # # woName = WebDriverWait(self.driverWo, 10).until(ec.visibility_of_element_located((By.ID, f'{idMain}_label'))).text
        # woName = woName.replace('Work Order Administration:', '')

        # print(idMain.get_attribute('id'))
        # print(woName) 


        # id = self.driverWo.find_element_by_class_name('maFormNew').get_attribute('id')

        # part_seccion = self.driverWo.find_element_by_id(f'{id}_tabPage_Parts')

        # part_seccion.click()
    
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

        print(driver.title)

        driver.close()

        return 0

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
        
        priceOnFiixUpdate.send_keys(self.price.strip())
        buttonSave = driver.find_element_by_class_name('saveButtonAct')
        buttonSave.click()

        driver.close()

        showinfo(title='Informacion sobre el Supplie', message=f"""
        Supplie name: {self.nameSupplie}\n
        Code: {self.idSupplie}\n
        Qty on hand: {self.qtyOnHand}\n
        Price: USD {self.price}\n
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

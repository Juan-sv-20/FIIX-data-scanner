from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class wo:
    def __init__(self, name, woStatus, woType, woPriority, woSummary, driver):
        self.name = name,
        self.woStatus = woStatus
        self.woType = woType
        self.woPriority = woPriority
        self.woSummary = woSummary
        self.driver = driver
    
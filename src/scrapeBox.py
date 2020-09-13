from selenium import webdriver
import time
#webdriverwait related imports
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class scrapeBox:
    def __init__(self):
        chromedriver = "/Users/rgoodman/Desktop/ROUTE/Route-Scrape-Bxs/src/chromedriver"
        self.driver = webdriver.Chrome(chromedriver)
        url = "https://www.ncaa.com/game/3959666#boxscore"
        self.driver.get(url)
        self.moveToBox()

    def moveToBox(self):
        newUrl = (self.driver.current_url).replace('#', '/')
        self.driver.get(newUrl)



m = scrapeBox()

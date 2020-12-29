from selenium.webdriver.common.keys import Keys
from chromeSync import driver
#webdriverwait related imports
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class scrapeBox:
    def __init__(self, url, driver):
        self.driver = driver
        self.url = url
        self.moveToBox()

    def moveToBox(self):
        if 'boxscore' in self.url:
            self.url = self.url.replace('#', '/')
        elif self.url[-1] == '/':
            self.url += 'boxscore'
        else:
            self.url += '/boxscore'
        self.driver.get(self.url)
        source = self.driver.page_source
    
    
    def switchTeam(self):
        pass


url = 'https://www.ncaa.com/game/3959666/boxscore'
#GET TEAM
#GET OPPONENT
#GET DATE
#GET LOCATION
scrapeBox(url, driver)

        

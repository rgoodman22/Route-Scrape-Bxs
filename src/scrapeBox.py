from selenium.webdriver.common.keys import Keys
from chromeSync import driver
import time
#webdriverwait related imports
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

monthDict = {
    "JANUARY" : "1",
    "FEBRUARY" : "2",
    "MARCH" : "3",
    "APRIL" : "4",
    "MAY" : "5",
    "JUNE" : "6",
    "JULY" : "7",
    "AUGUST" : "8",
    "SEPTEMBER" : "9",
    "OCTOBER" : "10",
    "NOVEMBER" : "11",
    "DECEMBER" : "12"
}

def parseDate(date):
    date = date.split(' ')[:3]
    month = monthDict[date[0]]
    day = date[1][:2]
    year = date[2]

    return month + "/" + day + "/" + year

class scrapeBox:
    def __init__(self, url, driver, ID):
        self.ID = ID+1
        self.data = {}
        self.driver = driver
        self.url = url
        self.moveToBox()
        self.getTeams()
        # self.getDetails()
        self.parseBox(0)
        self.switchTeam()
        self.parseBox(1)
        

    def moveToBox(self):
        if 'boxscore' in self.url:
            self.url = self.url.replace('#', '/')
        elif self.url[-1] == '/':
            self.url += 'boxscore'
        else:
            self.url += '/boxscore'
        self.driver.get(self.url)    
    
    def switchTeam(self):
        time.sleep(.5)
        myXpath = "//div[@class='boxscore-team-selector-team homeTeam-bg-primary_color awayTeam-border-primary_color home']"
        homeTeam = self.driver.find_element_by_xpath(myXpath)
        driver.execute_script("arguments[0].click();", homeTeam)
    
    
    def parseBox(self, team):
        if team == 0:
            cur, opp = self.teams
        else:
            opp, cur = self.teams
        myXpath = "//div[@class='boxscore-table-collection']"
        tables = self.driver.find_element_by_xpath(myXpath)
        tables = tables.find_elements_by_xpath("//div[@class='boxscore-table-collection']")[0]
        tables = tables.find_elements_by_xpath(".//table")
        for table in tables:
            self.parseTable(table)

    def parseTable(self, webElement):
        category = webElement.find_element_by_xpath(".//th[@class='tableHeadCollegeName']").text
        attributeElements = webElement.find_elements_by_xpath(".//thead/tr/*")[1:]
        attributes = []
        for a in attributeElements:
            attributes.append(a.text)
        print(category)
        print(attributes)
        
            
    def getTeams(self):
        self.teams = []
        myXpath = "//div[@class='boxscore-team-selector-team awayTeam-bg-primary_color homeTeam-border-primary_color away active']"
        away = self.driver.find_element_by_xpath(myXpath)
        self.teams.append(away.text)

        myXpath = "//div[@class='boxscore-team-selector-team homeTeam-bg-primary_color awayTeam-border-primary_color home']"
        home = self.driver.find_element_by_xpath(myXpath)
        self.teams.append(home.text)

    def getDetails(self):
        myXpath = "//span[@class='venue']"
        self.date = self.driver.find_element_by_xpath(myXpath).text
        self.date = parseDate(self.date)
    

url = 'https://www.ncaa.com/game/3959666/boxscore'
#url = 'https://www.ncaa.com/game/football/d3/2013/09/07/alma-heidelberg/'

scrapeBox(url, driver, 0)

        

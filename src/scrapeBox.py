import time
import csv
# from selenium import webdriver
# from selenium.common.exceptions import NoSuchElementException 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException


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
    day = date[1][:-2]
    year = date[2]

    return month + "/" + day + "/" + year

class scrapeBox:
    def __init__(self, url, driver, div, ID):
        self.driver = driver
        self.url = url
        self.div = div
        self.moveToBox()
        
        #if not self.check404():
        if self.getTeams():
            self.fields = ['ID','date','division','team','opponent','statCategory','firstName','lastName','statistic','value']
            self.data = []
            self.ID = ID+1
            self.getDetails()
            self.parseBox(0)
            self.switchTeam()
            self.parseBox(1)
            self.write()
                    
    def check404(self):
        errors = self.driver.find_elements_by_class_name("error-page error-404")
        print(errors)
        if len(errors) == 0:
            return False
        else:
            print(self.url)
            return True

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
        self.driver.execute_script("arguments[0].click();", homeTeam)
    
    
    def parseBox(self, team):

        if team == 0:
            cur, opp = self.teams
        else:
            opp, cur = self.teams

        def parseTable(webElement):
            category = webElement.find_element_by_xpath(".//th[@class='tableHeadCollegeName']").text
            attributeElements = webElement.find_elements_by_xpath(".//thead/tr/*")[1:]
            attributes = []
            for a in attributeElements:
                attributes.append(a.text)
            dataRows = webElement.find_elements_by_xpath(".//tr")[1:]
            
            for row in dataRows:
                dataPoints = row.find_elements_by_xpath(".//*")
                player = dataPoints[0].text.split(' ')
                if 'Total' in player or category in player:
                    continue
                elif len(player) == 1:
                    player = ['', 'Team']
                for i in range(1, len(dataPoints)):
                    line = [self.ID, self.date, self.div, cur, opp, category, player[0], ''.join(player[1:]), attributes[i-1], dataPoints[i].text]
                    self.data.append(line)
                    self.ID += 1
        
        myXpath = "//div[@class='boxscore-table-collection']"
        tables = self.driver.find_element_by_xpath(myXpath)
        tables = tables.find_elements_by_xpath("//div[@class='boxscore-table-collection']")[0]
        tables = tables.find_elements_by_xpath(".//table")
        for table in tables:
            parseTable(table)

    


    def getTeams(self):
        try:
            self.teams = []
            myXpath = "//div[@class='boxscore-team-selector-team awayTeam-bg-primary_color homeTeam-border-primary_color away active']"
            away = WebDriverWait(self.driver, 4).until(EC.presence_of_element_located((By.XPATH, myXpath)))
            self.teams.append(away.text)
            myXpath = "//div[@class='boxscore-team-selector-team homeTeam-bg-primary_color awayTeam-border-primary_color home']"
            home = self.driver.find_element_by_xpath(myXpath)
            self.teams.append(home.text)
            return True
        except TimeoutException:
            print(self.url)
            pathName = "../data/errorLinks.txt"
            file = open(pathName, "a+")
            file.write(self.url + "\r\n")
            file.close()
            return False

    def getDetails(self):
        myXpath = "//span[@class='venue']"
        self.date = self.driver.find_element_by_xpath(myXpath).text
        self.date = parseDate(self.date)

    def write(self):
        pathName = "../data/%s/%s/%s-%s-%s.csv" %(self.div, self.date.split('/')[-1],self.date.replace('/', '-'), self.teams[0],self.teams[1])
        file = open(pathName, 'w')
        csvwriter = csv.writer(file)
        csvwriter.writerow(self.fields)
        csvwriter.writerows(self.data)

    

#url = 'https://www.ncaa.com/game/3959666/boxscore'
# url = 'https://www.ncaa.com/game/football/d3/2013/09/07/alma-heidelberg/'
# url = "https://www.ncaa.com/game/football/fbs/2013/08/29/southern-utah-south-alabama/boxscore"

# scrapeBox(url, driver, 'FBS', 0)

        

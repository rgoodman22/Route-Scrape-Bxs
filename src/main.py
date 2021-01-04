from selenium import webdriver
from menuSelect import menuSelect
from constants import constants
import time
from scrapeBox import scrapeBox
from chromeSync import driverInstall

dates = constants.dates
divs = constants.divDict
menuDriver = webdriver.Chrome(driverInstall)
gameDriver = webdriver.Chrome(driverInstall)
class main:
    def __init__(self):
        ID = 28138000#1000
        gameLinks = []
        m = menuSelect(menuDriver) #open boxscore database site
        for div in divs: #loop over divisions
            m.selectDivision(div) #select division combobox on site
            last = None

            ##
            #code used to customize dates used for current division
            curDates = dates #
            if div == "FBS":
                continue
            if div == "FCS":
                continue
                # curDates = dates[dates.index('10/12/2019'):]
                # m.yearSelect('2019')
            if div == "D-II":
                # curDates = dates[dates.index('11/1/2015'):]
                # m.yearSelect('2015')
                continue
            if div == "D-III":
                curDates = dates[dates.index('11/17/2019'):]
                m.yearSelect('2019')

            for date in curDates:
                time.sleep(.2)
                print(date)
                if '08/1/' in date:
                    year = date[-4:]
                    print('change year:', date, year)
                    m.yearSelect(year) # move to next year since the first date of a new season is always august first
                m.changeDate(date)
                cur = m.getBoxes() # get box score links from page
                if last == cur: # if the links are new
                    continue
                else:
                    last = cur
                    for link in cur:
                        scrapeBox(link, gameDriver, div, ID)
                        ID += 1000
                    #gameLinks.append(cur)


main()

                


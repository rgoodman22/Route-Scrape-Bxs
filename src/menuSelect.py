# -*- coding: utf-8 -*-
from constants import constants
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


#Constants
yearDict = constants.yearDict
divDict = constants.divDict

class menuSelect:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://stats.ncaa.org/season_divisions/11420/scoreboards?utf8=%E2%9C%93&season_division_id=&game_date=08%2F01%2F2013&conference_id=0&tournament_id=&commit=Submit"
        self.driver.get(self.url)


    #year menu logix
    def yearSelect(self, year):
        try:
            yearDropDown = self.driver.find_element_by_id("game_sport_year_ctl_id_select_chosen")
            yearDropDown.click()
            selectNextYear = yearDropDown.find_element_by_tag_name("ul")

            index = yearDict[year]
            myXpath = "//li[@data-option-array-index='%i']" % index
            selectNextYear = selectNextYear.find_element_by_xpath(myXpath)
            selectNextYear.click()
        except NoSuchElementException:
            print('help year select')
            self.yearSelect(year)

    def changeDate(self, date):
        openDate = self.driver.find_element_by_id("game_date")
        for i in range(0,10):
            openDate.send_keys(Keys.BACK_SPACE)
        openDate.send_keys(date, Keys.ENTER)

    def selectDivision(self, division):
        divDropDown = self.driver.find_element_by_id("season_division_id_select_chosen")
        divDropDown.click()
        selectNextDivision = divDropDown.find_element_by_tag_name("ul")

        index = divDict[division]
        myXpath = "//li[@data-option-array-index='%i']" % index
        selectNextDivision = selectNextDivision.find_element_by_xpath(myXpath)
        selectNextDivision.click()

    def getBoxes(self):
        myBoxes = []
        myElements = self.driver.find_elements_by_xpath('//*[@target="TURNER_BOX"]')
        for element in myElements:
            myBoxes.append(element.get_attribute('href'))
        return myBoxes
    def toHome(self, year):
        self.driver.get(self.url.replace('2013',year))
        
        






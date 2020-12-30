from menuSelect import menuSelect
from constants import constants
import time
from scrapeBox import scrapeBox
from chromeSync import driver

dates = constants.dates
divs = constants.divDict
class main:
    def __init__(self, driver):
        ID = 1000
        gameLinks = []
        m = menuSelect(driver)
        for div in divs:
            m.selectDivision(div)
            last = None
            for date in dates:
                time.sleep(.2)
                if '08/1/' in date:
                    year = date[5:]
                    m.yearSelect(year)
                m.changeDate(date)
                cur = m.getBoxes()
                if last == cur:
                    continue
                else:
                    last = cur
                    for link in cur:
                        scrapeBox(link, driver, div, ID)
                        ID += 1000
                    #gameLinks.append(cur)


main(driver)

                


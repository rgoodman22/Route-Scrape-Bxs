from menuSelect import menuSelect
from constants import constants
import time

dates = constants.dates
divs = constants.divDict
class main:
    def __init__(self):
        gameLinks = []
        m = menuSelect()
        for div in divs:
            m.selectDivision(div)
            last = None
            for date in dates:
                time.sleep(.2)
                if '08/1/' in date:
                    year = date[5::]
                    m.yearSelect(year)
                m.changeDate(date)
                cur = m.getBoxes()
                if last == cur:
                    continue
                else:
                    last = cur
                    print(cur)
                    gameLinks.append(cur)


main()

                


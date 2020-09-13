class constants:
    yearDict = {
        "2020" : 0,
        "2019" : 1,
        "2018" : 2,
        "2017" : 3,
        "2016" : 4,
        "2015" : 5,
        "2014" : 6,
        "2013" : 7,
        "2012" : 8,
        "2011" : 9,
        "2009" : 10,
        "2008" : 11,
        "2007" : 12      
    }

    divDict = {
        "FBS" : 1,
        "FCS" : 2,
        "D-II" : 3,
        "D-III" : 4
    }
    ##LOGIC FOR ALL DATES
    years = ['2013','2014','2015','2016','2017','2018','2019','2020','2021']
    months = ['01','08','09','10','11','12']
    days1 = [str(i) for i in range(1,32)]
    days2 = [str(i) for i in range(1,31)]
    dates = []
    y = ''
    m = ''
    d = ''
    days = ''
    for y in years:
        for m in months:
            if y == '2013' and m == '01':
                continue
            elif y == '2021' and m != '01':
                continue
            elif m in ['08','10','12','01']:
                days = days1
            else:
                days = days2
            for d in days:
                dates.append(m+'/'+d+'/'+y)
    


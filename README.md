# Web Scraping Project

Code to scrape all divisions of NCAA football box scores from www.ncaa.com, beginning in the 2013-2014 season.

## To Do

1. Edit errorLinks
2. commit scrapeBox.py
3. clean data to ROUTE SQL standards

## Functionality

### main

uses dates in the constants file to loop over all applicable dates and divisions.

### menuSelect

Implements the traversal of the ncaa homepage, found [here](`https://stats.ncaa.org/season_divisions/11420/scoreboards?utf8=%E2%9C%93&season_division_id=&game_date=08%2F01%2F2013&conference_id=0&tournament_id=&commit=Submit`), for all dates and divisions.

### scrapeBox

Scrapes all tables in the box score, getting date, team, and stats information.  Must click on team name tame to switch from away team to home team data.  Uses webDriverWait to check for missing data (error 404 or broken page).

### data

Naming convention is date-away team-home team.  errorLinks currently stores all links where data is missing.  Have yet to follow up on whether missing data is consistently due to broken pages or broken code.

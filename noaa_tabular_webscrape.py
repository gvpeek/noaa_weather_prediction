from bs4 import BeautifulSoup
import urllib2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlite3 import dbapi2 as sqlite
import sqlite3
import time

from weather_scrape_noaa_table_definitions import NOAAPrediction

def removeNonAscii(s):
    '''
    See http://stackoverflow.com/questions/1342000/how-to-replace-non-ascii-characters-in-string
    '''
    return "".join(i for i in s if ord(i)<128) 

def process_unicode_data(data):
    try:
        data = removeNonAscii(data.get_text())
    except:
        pass
    return str(data.replace(u'\xb0','')).strip()

## create db if it doesn't exist
conn = sqlite3.connect('database/weather_scrape.db')
conn.close()

engine = create_engine('sqlite:///database/weather_scrape.db') ##, echo=True)
Session = sessionmaker(bind=engine)

NOAAPrediction.metadata.create_all(engine)
session = Session()

pages = []

for h in range(3):
    ahead_hour = h * 48
    pages.append(urllib2.urlopen('http://forecast.weather.gov/MapClick.php?lat=30.32000&lon=-97.77&unit=0&lg=english&FcstType=digital&AheadHour=' + str(ahead_hour)).read())

##file = open('test_weather.html', 'w+')
##file.write(html)
##file.close()

##pages.append(open('test_weather.html','r'))

sample_time = time.strftime('%Y%m%d%H%M',time.localtime())

for html in pages:

    soup = BeautifulSoup(html)

    ctr=0
    expand_rows=False

    for i in soup.find_all('table'):
        ctr+=1
        if ctr == 8:
            rows=[]
            for row in i.find_all('tr'):
                if len(row) > 1: ## skip buffer rows with no data
                    if expand_rows:
                        total_rows=len(rows)
                        expand=[[] for i in range(len(row))]
                        rows=rows+expand
                        expand_rows=False
                    column_ctr=total_rows
                    for column in row.find_all('td'):
                        rows[column_ctr].append(process_unicode_data(column.get_text()))
                        if rows[column_ctr][0] == '':
                            if rows[(column_ctr-1)][0] == 'Date':
                                rows[column_ctr][0] = rows[(column_ctr-2)][0]
                            else:
                                rows[column_ctr][0] = rows[(column_ctr-1)][0]
                        column_ctr+=1
                else:
                    expand_rows=True

    for row in rows:
        if row[0]=='Date':
            pass
        else:
            row.append(sample_time)
            row[0] = time.strftime('%Y',time.localtime()) + row[0][0:2] + row[0][3:5]
            session.add(NOAAPrediction(row))
            session.commit()

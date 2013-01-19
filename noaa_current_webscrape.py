from bs4 import BeautifulSoup
import urllib2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlite3 import dbapi2 as sqlite
import sqlite3
import time
from math import ceil

from weather_scrape_noaa_table_definitions import NOAACurrent

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

NOAACurrent.metadata.create_all(engine)
session = Session()

##html = urllib2.urlopen('http://w1.weather.gov/obhistory/KATT.html').read()

##file = open('test_weather.html', 'w+')
##file.write(html)
##file.close()

html = (open('KATT.html','r'))

sample_time = time.strftime('%Y%m%d%H%M',time.localtime())

soup = BeautifulSoup(html)

ctr=0
row_ctr=0
expand_rows=False

for i in soup.find_all('table'):
    ctr+=1
    if ctr == 4:
        rows=[]
        for row in i.find_all('tr'):
            row_ctr+=1
            if row_ctr==61: ## 4
                date, hour, wind, visibility, weather, sky, temp, dewpoint, six_hour_max, six_hour_min, humidity, wind_chill, heat_index, altimeter, sea_level, precip_one_hour, precip_three_hour, precip_six_hour = row.find_all('td')

                date = time.strftime('%Y%m',time.localtime()) + process_unicode_data(date)

                hour = process_unicode_data(hour)[0:2]

                wind = process_unicode_data(wind).split()
                gust=''
                wind_dir=''
                if len(wind) == 4:
                    gust = wind.pop()
                    wind.pop() ## pop 3rd and 4th words so next if is hit
                if len(wind) == 2:
                    wind_dir = wind.pop(0)
                    wind = wind[0]
                elif wind[0] == 'Calm':
                    wind='0'
                else:
                    wind_dir = wind.pop()
                    wind=''

                sky = process_unicode_data(sky).split()
                sky_cover=0
                if not sky[0] == 'CLR':
                    for measure in sky:
                        sky_cover = sky_cover + int(measure[-3:])
                    sky_cover = int(ceil(sky_cover/len(sky)))

                precipitation_amnt = process_unicode_data(precip_one_hour)

                temp = process_unicode_data(temp)

                dewpoint = process_unicode_data(dewpoint)

                wind_chill = process_unicode_data(wind_chill)
                wind_chill=wind_chill.replace('NA','0')

                relative_humidity = process_unicode_data(humidity)[:-1]

                freezing_rain = False
                rain = False
                snow = False
                sleet = False
                thunder = False
                weather = process_unicode_data(weather)
                if weather.find('Freezing Rain') > 0:
                    freezing_rain = True
                elif weather.find('Rain') > 0:
                    rain = True
                elif weather.find('Snow') > 0:
                    snow = True
                elif weather.find('Sleet') > 0:
                    sleet = True
                elif weather.find('Thunder') > 0:
                    thunder = True

                
                        

##                        temp = Column(String)
##                        dewpoint = Column(String)
##                        wind_chill = Column(String)
##                        wind = Column(String)
##                        wind_direction = Column(String)
##                        gust = Column(String)
##                        sky_cover = Column(String)
##                        precipitation_pct = Column(String)
##                        relative_humidity = Column(String)
##                        thunder = Column(String)
##                        rain = Column(String)
##                        snow = Column(String)
##                        freezing_rain = Column(String)
##                        sleet = Column(String)

##                for column in row.find_all('td'):
##                    print column.get_text()

##            if len(row) > 1: ## skip buffer rows with no data
##                if expand_rows:
##                    total_rows=len(rows)
##                    expand=[[] for i in range(len(row))]
##                    rows=rows+expand
##                    expand_rows=False
##                column_ctr=total_rows
##                for column in row.find_all('td'):
##                    rows[column_ctr].append(process_unicode_data(column.get_text()))
##                    if rows[column_ctr][0] == '':
##                        if rows[(column_ctr-1)][0] == 'Date':
##                            rows[column_ctr][0] = rows[(column_ctr-2)][0]
##                        else:
##                            rows[column_ctr][0] = rows[(column_ctr-1)][0]
##                    column_ctr+=1
##            else:
##                expand_rows=True
##
##for row in rows:
##    if row[0]=='Date':
##        pass
##    else:
##        row.append(sample_time)
##        session.add(NOAAPrediction(row))
##        session.commit()

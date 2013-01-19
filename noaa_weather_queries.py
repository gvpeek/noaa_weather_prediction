from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from weather_scrape_noaa_table_definitions import NOAAPrediction

engine = create_engine('sqlite:///database/weather_scrape.db') ##, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

for prediction in session.query(NOAAPrediction.id, NOAAPrediction.date, NOAAPrediction.hour, NOAAPrediction.temp, NOAAPrediction.sample_time).all():
    print 'pred', prediction.id, prediction.date, prediction.hour, prediction.temp, prediction.sample_time
    

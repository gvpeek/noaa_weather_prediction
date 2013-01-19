from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class NOAAPrediction(Base):
    __tablename__ = 'noaa_prediction'

    id = Column(Integer, primary_key=True)
    date = Column(String)
    hour = Column(String)
    temp = Column(String)
    dewpoint = Column(String)
    wind_chill = Column(String)
    wind = Column(String)
    wind_direction = Column(String)
    gust = Column(String)
    sky_cover = Column(String)
    precipitation_pct = Column(String)
    relative_humidity = Column(String)
    thunder = Column(String)
    rain = Column(String)
    snow = Column(String)
    freezing_rain = Column(String)
    sleet = Column(String)
    sample_time = Column(String)

    def __init__(self,list_of_values):
        self.date, self.hour, self.temp, self.dewpoint, self.wind_chill, self.wind, self.wind_direction, self.gust, self.sky_cover, self.precipitation_pct, self.relative_humidity, self.thunder, self.rain, self.snow, self.freezing_rain, self.sleet, self.sample_time = list_of_values


class NOAACurrent(Base):
    __tablename__ = 'noaa_current'

    id = Column(Integer, primary_key=True)
    date = Column(String) #
    hour = Column(String) #
    temp = Column(String) #
    dewpoint = Column(String) #
    wind_chill = Column(String) #
    wind = Column(String) #
    wind_direction = Column(String) #
    gust = Column(String) #
    sky_cover = Column(String) #
    precipitation_amnt = Column(String) #
    relative_humidity = Column(String) #
    weather = Column(String)
    thunder = Column(Boolean)
    rain = Column(Boolean)
    snow = Column(Boolean)
    freezing_rain = Column(Boolean)
    sleet = Column(Boolean)
    sample_time = Column(String)

    def __init__(self,list_of_values):
            self.date, self.hour, self.temp, self.dewpoint, self.wind_chill, self.wind, self.wind_direction, self.gust, self.sky_cover, self.precipitation_pct, self.relative_humidity, self.thunder, self.rain, self.snow, self.freezing_rain, self.sleet, self.sample_time = list_of_values

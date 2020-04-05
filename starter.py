#%matplotlib inline
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt


import numpy as np
import pandas as pd

import datetime as dt


# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


'''

Use SQLAlchemy create_engine to connect to your sqlite database.
'''

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

'''
Choose a start date and end date for your trip. Make sure that your vacation range is approximately 3-15 days total.

2015 jan 10 to jan 24 
'''


# reflect an existing database into a new model

Base = automap_base()

Base.prepare(engine, reflect=True)

#print(Base.classes.keys())


# reflect the tables


# We can view all of the classes that automap found

'''
Use SQLAlchemy automap_base() to reflect your tables into classes and save a reference to those classes called Station and Measurement.

'''


# Save references to each table

Measurement = Base.classes.measurement
Station = Base.classes.station




# Create our session (link) from Python to the DB

session = Session(engine)




# Design a query to retrieve the last 12 months of precipitation data and plot the results

#first_row = session.query(Measurement).first()
#print(first_row.__dict__)

#for row in session.query(Measurement.date, Measurement.prcp).limit(15).all():
#    print(row)

dates = []
rainfalls = []
for a,b in session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > '2014-01-15').filter(Measurement.date < '2015-01-15').\
    order_by(Measurement.date).all():
        dates.append(a)
        rainfalls.append(b)

for i in range(len(rainfalls)):
    if rainfalls[i] == rainfalls[29]:
        rainfalls[i] = 0.0


print(rainfalls)
print(dates)

data = pd.DataFrame(rainfalls, dates)
data.columns = ['rainfall']
data.index.name = 'date'
data.fillna(0.0, inplace=True)
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(data)

# Calculate the date 1 year ago from the last data point in the database

# Perform a query to retrieve the data and precipitation scores

# Save the query results as a Pandas DataFrame and set the index to the date column

# Sort the dataframe by date

# Use Pandas Plotting with Matplotlib to plot the data

plt.figure()
data.plot()
plt.ylim((0, 13))
plt.xlabel('Dates')
plt.ylabel('Rainfall in Inches')
plt.title('Rainfall for jan 14 2014 to jan 14 2015 ')
plt.show()

# Use Pandas to calculate the summary statistics for the precipitation data

print(data.describe())


# Design a query to show how many stations are available in this dataset?

# What are the most active stations? (i.e. what stations have the most rows)?
# List the stations and the counts in descending order.

# Using the station id from the previous query, calculate the lowest temperature recorded,
# highest temperature recorded, and average temperature of the most active station?


# Choose the station with the highest number of temperature observations.
# Query the last 12 months of temperature observation data for this station and plot the results as a histogram

# This function called `calc_temps` will accept start date and end date in the format '%Y-%m-%d'
# and return the minimum, average, and maximum temperatures for that range of dates

'''
def calc_temps(start_date, end_date):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    
    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

# function usage example
print(calc_temps('2012-02-28', '2012-03-05'))

'''




# Use your previous function `calc_temps` to calculate the tmin, tavg, and tmax
# for your trip using the previous year's data for those same dates.


# Plot the results from your previous query as a bar chart.
# Use "Trip Avg Temp" as your Title
# Use the average temperature for the y value
# Use the peak-to-peak (tmax-tmin) value as the y error bar (yerr)

# Calculate the total amount of rainfall per weather station for your trip dates using the previous year's matching dates.
# Sort this in descending order by precipitation amount and list the station, name, latitude, longitude, and elevation


# Create a query that will calculate the daily normals
# (i.e. the averages for tmin, tmax, and tavg for all historic data matching a specific month and day)

'''
def daily_normals(date):
    """Daily Normals.
    
    Args:
        date (str): A date string in the format '%m-%d'
        
    Returns:
        A list of tuples containing the daily normals, tmin, tavg, and tmax
    
    """
    
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    return session.query(*sel).filter(func.strftime("%m-%d", Measurement.date) == date).all()
    
daily_normals("01-01")

'''

# calculate the daily normals for your trip
# push each tuple of calculations into a list called `normals`

# Set the start and end date of the trip

# Use the start and end date to create a range of dates

# Stip off the year and save a list of %m-%d strings

# Loop through the list of %m-%d strings and calculate the normals for each date


# Load the previous query results into a Pandas DataFrame and add the `trip_dates` range as the `date` index

# Plot the daily normals as an area plot with `stacked=False`




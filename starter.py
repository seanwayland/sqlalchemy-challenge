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

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")
session = Session(engine)
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table

Measurement = Base.classes.measurement
Station = Base.classes.station

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


plt.figure()
data.plot()
plt.ylim((0, 13))
plt.xlabel('Dates')
plt.ylabel('Rainfall in Inches')
plt.title('Rainfall for jan 14 2014 to jan 14 2015 ')
plt.show()

# Use Pandas to calculate the summary statistics for the precipitation data

print(data.describe())


#Design a query to calculate the total number of stations.

session = Session(engine)
Base = automap_base()
Base.prepare(engine, reflect=True)
# query the data
stations = []
rainfalls = []
results = []
# get results for year 2017
for a,b,c in session.query(Measurement.station, Measurement.tobs, Measurement.date).\
filter(Measurement.date > '2017-01-01').\
order_by(Measurement.station) .\
order_by(Measurement.date).all():
        resultsdict = {}
        resultsdict["station"] = a
        resultsdict["tobs"] = b
        resultsdict["date"] = c
        results.append(resultsdict)
session.close()
 # convert to dataframe
data = pd.DataFrame(results)
# ditch rows with null values
data = data.dropna()
# sort to find station with most results
counts = data.groupby('station').count()
counts = counts.sort_values('date', ascending = False)
mostActiveStation = counts.index[0]
# filter data based on station with most values
data2 = data.loc[data['station'] == mostActiveStation]
#print(data2)
print('most active station is: ')
print(mostActiveStation)



#Design a query to find the most active stations.

#List the stations and observation counts in descending order.

#Which station has the highest number of observations?

#Hint: You may need to use functions such as func.min, func.max, func.avg, and func.count in your queries.

#Design a query to retrieve the last 12 months of temperature observation data (TOBS).

#Filter by the station with the highest number of observations.

#Plot the results as a histogram with bins=12.




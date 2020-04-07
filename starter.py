#%matplotlib inline
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

import datetime
import calendar

import numpy as np
import pandas as pd

import datetime as dt

from scipy.stats import ttest_ind

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import extract

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

# plot counts
d3 = data2['tobs'].tolist()
plt.hist(d3, bins = 12)
plt.xlabel('Temp')
plt.ylabel('Frequency')
plt.title('Number of temp observations for station with most values ')
plt.show()




#Hawaii is reputed to enjoy mild weather all year.
#Is there a meaningful difference between the temperature in, for example, June and December?
#You may either use SQLAlchemy or pandas's read_csv() to perform this portion.
#Identify the average temperature in June at all stations across all available years in the dataset.


#Identify the average temperature in June at all stations across all available years in the dataset
session = Session(engine)
Base = automap_base()
Base.prepare(engine, reflect=True)

res = session.query(Measurement.tobs, Measurement.date).filter(extract('month', Measurement.date)==6).all()
session.close()
 # convert to dataframe
junedata = pd.DataFrame(res)

#print(junedata)
print(junedata.mean(skipna = True))

# Do the same for December temperature.

session = Session(engine)
Base = automap_base()
Base.prepare(engine, reflect=True)

res = session.query(Measurement.tobs, Measurement.date).filter(extract('month', Measurement.date)==12).all()
session.close()
 # convert to dataframe
decData = pd.DataFrame(res)

#print(decData)
print(decData.mean(skipna = True))
#Use the t-test to determine whether the difference in the means, if any, is statistically significant.
#Will you use a paired t-test, or an unpaired t-test? Why?

'''
You cant use a paired t-test because the sample sizes are not the same 

tobs    74.944118
dtype: float64
tobs    71.041529
dtype: float64
Ttest_indResult(statistic=31.60372399000329, pvalue=3.9025129038616655e-191)
'''


cat1 = junedata['tobs']
cat2 = decData['tobs']

print(ttest_ind(cat1, cat2))


# This function called `calc_temps` will accept start date and end date in the format '%Y-%m-%d'
# and return the minimum, average, and maximum temperatures for that range of dates

'''
Use the calc_temps function to calculate the min, avg, and max temperatures for your trip
 using the matching dates from the previous year
 (i.e., use "2017-01-01" if your trip start date was "2018-01-01").
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
values = calc_temps('2014-01-15', '2015-01-15')
print(values)

df5 = pd.DataFrame(values, columns=['Min Temp', 'Average Temp', 'Max Temp'])
avg_temp = df5['Average Temp']
tmin_tmax_temp = df5.iloc[0]['Max Temp'] - df5.iloc[0]['Min Temp']
avg_temp.plot(kind='bar', yerr=tmin_tmax_temp, figsize=(5,8), alpha=0.6, color='coral')
plt.title("Average temperature for trip", fontsize=20)
plt.ylabel("Temp in farenheight")
plt.xticks([])
plt.grid()
plt.show()







import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from collections import Counter

from flask import Flask, jsonify

import pandas as pd

import datetime as dt
import json


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table

Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


def queryDB(query):
    session = Session(engine)
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    # query the data
    results = session.query(query)
    session.close()
    return results

def trim_word(word, from_start=0, from_end=0):
    return word[from_start:len(word) - from_end]


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    top = "Welcome to the weather API for hawaii query possibilites are: <br/> "
    a = "/api/v1.0/precipitation <br/> Convert the query results to a dictionary using date as the key and prcp as the value. <br/>"

    b = "Return the JSON representation of your dictionary. <br/> "

    c ="/api/v1.0/stations <br/> "

    d = "Return a JSON list of stations from the dataset. <br/>"

    e = "/api/v1.0/tobs <br/> "

    f = "Query the dates and temperature observations of the most active station for the last year of data. <br/>"

    g = "Return a JSON list of temperature observations (TOBS) for the previous year. <br/> "

    h = "/api/v1.0/&lt;start&gt; and /api/v1.0/&lt;start&gt;/&lt;end&gt; <br/>"

    i = "Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range. <br/>"

    j = "When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.<br/> "

    k ="When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.<br/> "

    return(  top + a + b  + c + d   + e +f + g  + h + i + j + k + 'Query should be structured YYYY-MM-DD'  )

'''
/api/v1.0/precipitation

Convert the query results to a dictionary using date as the key and prcp as the value.

Return the JSON representation of your dictionary.

'''

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB

    session = Session(engine)
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    # query the data
    results = session.query(Measurement.prcp, Measurement.date)
    session.close()

    # Convert list of tuples into normal list
    dates = []
    rainfalls = []

    for a,b in results:

        rainfalls.append(a)
        dates.append(b)

    # use pandas to strip nulls from precipitation
    data = pd.DataFrame(rainfalls, dates)
    data.columns = ['rainfall']
    data.index.name = 'date'
    data.fillna(0.0, inplace=True)

    rainfalls = data['rainfall'].tolist()
    # create dictionary from results
    result = {dates[i]: rainfalls[i] for i in range(len(dates))}

    return jsonify(result)
'''
/api/v1.0/stations

Return a JSON list of stations from the dataset.
'''
@app.route("/api/v1.0/stations")
def stations():

    results = queryDB(Station.name)

    result = []
    for row in results:
        result.append(row)

    print(result)

    return(jsonify(result))


'''

/api/v1.0/tobs

Query the dates and temperature observations of the most active station for the last year of data.

Return a JSON list of temperature observations (TOBS) for the previous year.

dates = []
rainfalls = []
for a,b in session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > '2014-01-15').filter(Measurement.date < '2015-01-15').\
    order_by(Measurement.date).all():
        dates.append(a)
        rainfalls.append(b)
'''

@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    # query the data
    stations = []
    rainfalls = []
    results = []
    # get results for year 2017
    for a,b,c in session.query(Measurement.station, Measurement.prcp, Measurement.date).\
    filter(Measurement.date > '2017-01-01').\
    order_by(Measurement.station) .\
    order_by(Measurement.date).all():
        resultsdict = {}
        resultsdict["station"] = a
        resultsdict["rainfall"] = b
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
    print(data2)
    jsondata = data2.to_json(orient = "records")
    #print(jsondata)
   # return('hi')
    return(jsondata)




    return "hi"


'''/api/v1.0/<start>'''
'''
Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.

'''

@app.route("/api/v1.0/<start>")
def start(start):

    session = Session(engine)
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    # query the data
    min = 100
    max = 0
    sum = 0
    count = 0
    start = trim_word(start,1,1)

    # get results for year 2017
    for row in session.query(Measurement.tobs, Measurement.date).\
    filter(Measurement.date > start):
    #filter(Measurement.date > '2017-01-01'):

        val = row.tobs
        sum = sum + val
        if val < min:
            min = val
        if val > max:
            max = val
        count = count + 1


    session.close()



    if count == 0 :
        return("no results found. Query should be structured YYYY-MM-DD")
    else:
        resultsdict = {}
        resultsdict["TMIN"] = str(min)
        resultsdict["TMAX"] = str(max)
        resultsdict["TAVG"] = str(sum/count)
        result = json.dumps(resultsdict)
        return(result)


'''

/api/v1.0/<start>/<end>

'''


@app.route("/api/v1.0/<start>/<end>")
def startend(start, end):

    session = Session(engine)
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    # query the data
    min = 100
    max = 0
    sum = 0
    count = 0
    start = trim_word(start,1,1)
    end = trim_word(end,1,1)

    # get results for year 2017
    for row in session.query(Measurement.tobs, Measurement.date).\
    filter(Measurement.date > start).filter(Measurement.date < end):


        val = row.tobs
        sum = sum + val
        if val < min:
            min = val
        if val > max:
            max = val
        count = count + 1


    session.close()



    if count == 0 :
        return("no results found. Query should be structured YYYY-MM-DD/YYYY-MM-DD")
    else:
        resultsdict = {}
        resultsdict["TMIN"] = str(min)
        resultsdict["TMAX"] = str(max)
        resultsdict["TAVG"] = str(sum/count)
        result = json.dumps(resultsdict)
        return(result)
















if __name__ == '__main__':
    app.run(debug=True)

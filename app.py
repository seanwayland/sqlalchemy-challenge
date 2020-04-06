import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from collections import Counter

from flask import Flask, jsonify

import pandas as pd


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



#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/names<br/>"
        f"/api/v1.0/passengers"
    )
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









if __name__ == '__main__':
    app.run(debug=True)

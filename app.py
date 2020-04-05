import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

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



if __name__ == '__main__':
    app.run(debug=True)

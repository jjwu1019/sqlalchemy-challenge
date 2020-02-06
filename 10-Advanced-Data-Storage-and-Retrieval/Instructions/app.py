import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

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
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)

    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()


    all_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict[date] = prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)


@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)


    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_station = list(np.ravel(results))

    return jsonify(all_station)


@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)

    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    measurement_results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= query_date).all()

    session.close()


    all_tobs = []
    for date, tobs in measurement_results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
def start_temp(start):

    session = Session(engine)


    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    session.close()


    start_temp = list(np.ravel(results))

    return jsonify(start_temp)

@app.route("/api/v1.0/<start>/<end>")
def calc_temp(start, end):

    session = Session(engine)


    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()


    calc_temp = list(np.ravel(results))

    return jsonify(calc_temp)

if __name__ == '__main__':
    app.run(debug=True)

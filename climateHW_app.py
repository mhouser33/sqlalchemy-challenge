# --Climate APP

from flask import Flask, json, jsonify
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import inspect

engine = create_engine("sqlite:///Desktop/hawaii.sqlite", connect_args={'check_same_thread': False})
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

app = Flask(__name__) 

#Available Routes.
@app.route("/")
def home():
    print("In & Out of Home section.")
    return (
        f"Honolulu, Hawaii API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/8-24-16 to 8-23-17/"
    )

# Return the JSON representation of your dictionary
@app.route('/api/v1.0/precipitation/')
def precipitation():
    print("In Precipitation section.")
    
    date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date
    year = dt.datetime.strptime(date, '%Y-%m-%d') - dt.timedelta(days=365)

    rain_results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= year).\
    order_by(Measurement.date).all()

    p_dict = dict(rain_results)
    print(f"In Precipitation - {p_dict}")
    print("Out Precipitation section.")
    return jsonify(p_dict) 

# Return a JSON list of stations from the dataset
@app.route('/api/v1.0/stations/')
def stations():
    print("In Each Station")

 #query for the dates and temperature observations from a year from the last data point. 
    station_list = session.query(Station.station)\
    .order_by(Station.station).all() 
    print()
    print("Station List:")   
    for row in station_list:
        print (row[0])
    print("Outside Station section.")
    return jsonify(station_list)

#Return a JSON list of Temperature Observations (tobs) for the previous year
@app.route('/api/v1.0/tobs/')
def tobs():
    print("TOBS")
    
    previous_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date
    previous_year = dt.datetime.strptime(previous_date, '%Y-%m-%d') - dt.timedelta(days=365)

    temp_obs = session.query(Measurement.date, Measurement.tobs)\
        .filter(Measurement.date >= previous_year)\
        .order_by(Measurement.date).all()
    print()
    print("Temperature For All Stations")
    print(temp_obs)
    print("Out of TOBS")
    return jsonify(temp_obs)

# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start date
@app.route('/api/v1.0/<start_date>/')
def calc_temps_start(start_date):
    print("Start Date")
    print(start_date)
    
    select = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    result_temp = session.query(*select).\
        filter(Measurement.date >= start_date).all()
    print()
    print(f"Start date temp {start_date}")
    print(result_temp)
    print("Out of start date")
    return jsonify(result_temp)

if __name__ == "__main__":
    app.run(debug=True)
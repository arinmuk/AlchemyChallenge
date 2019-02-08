# 1. Import Flask
from flask import Flask, jsonify
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from dateutil.relativedelta import relativedelta
#added
from sqlalchemy.pool import SingletonThreadPool

#################################################
# Database Setup
#################################################
#engine = create_engine("sqlite:///Resources/hawaii.sqlite",poolclass=SingletonThreadPool)
engine = create_engine("sqlite:///Resources/hawaii.sqlite?check_same_thread=False")
#conn = engine.connect()
session = Session(engine)
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
#session = Session(engine)



# 2. Create an app
app = Flask(__name__)


# 3. Define static routes
@app.route("/")
def index():
    return (f"Welcome to the Hawaii Weather API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/Start_and_EndDate<br/>"
        f"about"
        )


@app.route("/about")
def about():
    name = "Peleke"
    location = "Tien Shan"

    return f"My name is {name}, and I live in {location}."


@app.route("/api/v1.0/precipitation")

def precipitation():
    results = session.query(Measurement.date , Measurement.prcp ).\
          filter(Measurement.date >= (dt.datetime.strptime((session.query(func.max(Measurement.date)).\
            scalar()), '%Y-%m-%d').date()+relativedelta(months=-12)),Measurement.prcp!=None).all()
    all_prcp = []
    for prcp in results:
        prcp_dict = {}
        prcp_dict["Date"] = prcp.date
        prcp_dict["Prcp"] = prcp.prcp
        
        all_prcp.append(prcp_dict)
       
    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    results1 = session.query(Station.station) 
    all_stations = []
    for stat in results1:
        all_stations.append(stat.station)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
     results = session.query(Measurement.date , Measurement.tobs ).\
          filter(Measurement.date >= (dt.datetime.strptime((session.query(func.max(Measurement.date)).\
            scalar()), '%Y-%m-%d').date()+relativedelta(months=-12)),Measurement.tobs!=None).all()
     all_tobs = []
     for tobs in results:
        tobs_dict = {}
        tobs_dict["Date"] = tobs.date
        tobs_dict["tobs"] = tobs.tobs
        
        all_tobs.append(tobs_dict)
     return jsonify(all_tobs)

@app.route("/api/v1.0/Start_and_EndDate")
def startstop():
    startdt = "2017-01-01"
    endt="2017-01-07"
    vr_res = session.query(Measurement.date,(func.Max(Measurement.tobs)),(func.Min(Measurement.tobs)),(func.avg(Measurement.tobs))).\
                    filter(Measurement.date >= startdt,Measurement.date <= endt)
    all_vtobs = []
    for vtobs in vr_res:
        vtobs_dict = {}
        vtobs_dict["Daterange"] = f" for the entire vacation Date range {startdt} and {endt} Max, Avg and Min Temps"
        vtobs_dict["TMax"] = vtobs[1]
        vtobs_dict["TMin"] = vtobs[2]
        vtobs_dict["TAvg"] = vtobs[3]        
        all_vtobs.append(vtobs_dict)
    
    vr1_res=session.query(Measurement.date,(func.Max(Measurement.tobs)),(func.Min(Measurement.tobs)),(func.avg(Measurement.tobs))).\
                    filter(Measurement.date >= startdt,Measurement.date <= endt).group_by(Measurement.date)

    
    for vtobs2 in vr1_res:
        vtobs2_dict = {}
        vtobs2_dict["Daterange"] = f" for the Date range {startdt} and {endt} Max, Avg and Min Temps for the day {vtobs2.date} of vacation"
        vtobs2_dict["TMax"] = vtobs2[1]
        vtobs2_dict["TMin"] = vtobs2[2]
        vtobs2_dict["TAvg"] = vtobs2[3]        
              
        all_vtobs.append(vtobs2_dict)

    vr_res1 = session.query(Measurement.date,(func.Max(Measurement.tobs)),(func.Min(Measurement.tobs)),(func.avg(Measurement.tobs))).\
                    filter(Measurement.date >= startdt)
    
    for vtobs1 in vr_res1:
        vtobs1_dict = {}
        vtobs1_dict["Daterange"] = f" for the Entire Date range {startdt} and No End Date  Max, Avg and Min Temps"
        vtobs1_dict["TMax"] = vtobs1[1]
        vtobs1_dict["TMin"] = vtobs1[2]
        vtobs1_dict["TAvg"] = vtobs1[3]  
    all_vtobs.append(vtobs1_dict)
    
    
    vr_res11 = session.query(Measurement.date,(func.Max(Measurement.tobs)),(func.Min(Measurement.tobs)),(func.avg(Measurement.tobs))).\
                    filter(Measurement.date >= startdt).group_by(Measurement.date)


    for vtobs22 in vr_res11:
        vtobs22_dict = {}
        vtobs22_dict["Daterange"] = f" for the Date range {startdt} and No End Date  Max, Avg and Min Temps for the day {vtobs22.date}"
        vtobs22_dict["TMax"] = vtobs22[1]
        vtobs22_dict["TMin"] = vtobs22[2]
        vtobs22_dict["TAvg"] = vtobs22[3]        
        all_vtobs.append(vtobs22_dict)

    return jsonify(all_vtobs)






# 4. Define main behavior
if __name__ == "__main__":
    app.run(debug=True)







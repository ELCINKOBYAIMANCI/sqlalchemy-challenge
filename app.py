{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "c80586d0",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Import the dependencies.\n",
    "import sqlalchemy\n",
    "from flask import Flask, jsonify\n",
    "import datetime as dt\n",
    "import numpy as np\n",
    "from sqlalchemy.ext.automap import automap_base\n",
    "from sqlalchemy.orm import Session\n",
    "from sqlalchemy import create_engine, func, inspect"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "d9316635",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Database Setup\n",
    "# create engine to hawaii.sqlite\n",
    "engine = create_engine(f\"sqlite:///Resources/hawaii.sqlite\")\n",
    "\n",
    "# reflect an existing database into a new model\n",
    "Base = automap_base()\n",
    "\n",
    "# reflect the tables\n",
    "Base.prepare(engine, reflect=True)\n",
    "\n",
    "# View all of the classes that automap found\n",
    "Base.classes.keys()\n",
    "\n",
    "# Save references to each table\n",
    "Measurement = Base.classes.measurement\n",
    "Station = Base.classes.station\n",
    "\n",
    "# Create our session (link) from Python to the DB\n",
    "session = Session(engine)\n",
    "\n",
    "#################################################\n",
    "# Flask Setup\n",
    "#################################################\n",
    "app = Flask(__name__)\n",
    "#################################################\n",
    "# Flask Routes\n",
    "#################################################\n",
    "@app.route(\"/\")\n",
    "def main():\n",
    "    return (\n",
    "        f\"Welcome to the Climate App Home Page!<br>\"\n",
    "        f\"Available Routes:<br>\"\n",
    "        f\"/api/v1.0/precipitation<br>\"\n",
    "        f\"/api/v1.0/stations<br>\"\n",
    "        f\"/api/v1.0/tobs<br>\"\n",
    "        f\"/api/v1.0/<start><br>\"\n",
    "        f\"/api/v1.0/<start>/<end><br>\"\n",
    "    )\n",
    "@app.route(\"/api/v1.0/precipitation\")\n",
    "def precip():\n",
    "    prev_year = dt.date(2017,8,23)- dt.timedelta(days=365)\n",
    "    results= session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).\\\n",
    "    order_by(Measurement.date).all()\n",
    "    result_dict = dict(results)\n",
    "    session.close()\n",
    "    return jsonify(result_dict)\n",
    "\n",
    "@app.route(\"/api/v1.0/stations\")\n",
    "def stations():\n",
    "    stations = session.query(Measurement.station, func.count(Measurement.id)).\\\n",
    "            group_by(Measurement.station).order_by(func.count(Measurement.id).desc()).all()\n",
    "\n",
    "    stations_dict = dict(stations)\n",
    "    session.close()\n",
    "    return jsonify(stations_dict)\n",
    "@app.route(\"/api/v1.0/tobs\")\n",
    "def tobs():\n",
    "    max_temp_obs = session.query(Measurement.station, Measurement.tobs).\\\n",
    "        filter(Measurement.date >= '2016-08-23').all()\n",
    "\n",
    "    tobs_dict = dict(max_temp_obs)\n",
    "    session.close()\n",
    "    return jsonify(tobs_dict)\n",
    "\n",
    "\n",
    "@app.route(\"/api/v1.0/<start>\")\n",
    "def start(start):\n",
    "    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),\\\n",
    "                                func.max(Measurement.tobs)).filter(Measurement.date >= start).all()\n",
    "    \n",
    "    session.close()\n",
    "    tobsall = []\n",
    "\n",
    "    for min,avg,max in result:\n",
    "        tobs_dict = {}\n",
    "        tobs_dict[\"Min\"] = min\n",
    "        tobs_dict[\"Average\"] = avg\n",
    "        tobs_dict[\"Max\"] = max\n",
    "        tobsall.append(tobs_dict)\n",
    "        \n",
    "    return jsonify(tobsall)\n",
    "\n",
    "@app.route('/api/v1.0/<start>/<end>')\n",
    "def start_end(start,end):\n",
    "    queryresult = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),\\\n",
    "                func.max(Measurement.tobs)).filter(Measurement.date >= start).\\\n",
    "                filter(Measurement.date <= end).all()\n",
    "\n",
    "    session.close()\n",
    "\n",
    "    tobsall = []\n",
    "    for min,avg,max in queryresult:\n",
    "        tobs_dict = {}\n",
    "        tobs_dict[\"Min\"] = min\n",
    "        tobs_dict[\"Average\"] = avg\n",
    "        tobs_dict[\"Max\"] = max\n",
    "        tobsall.append(tobs_dict)\n",
    "\n",
    "    return jsonify(tobsall)\n",
    "\n",
    "\n",
    "if __name__ == '__main__':\n",
    "    app.run(debug=True)\n"
   ]
  }
 ],
 "metadata": {
  "celltoolbar": "Raw Cell Format",
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.10.13"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
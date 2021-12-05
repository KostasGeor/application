from flask import Flask
from flask import render_template
from flaskext.sass import sass
from flask import request
import psycopg2
from flask_negotiate import consumes




app = Flask(__name__)
sass(app, input_dir='assets/scss', output_dir='static')


def geocode(location):
    import pandas as pd
    import numpy as np
    import json
    import requests
    URL = "https://geocode.search.hereapi.com/v1/geocode"
    api_key = 'LHAyyGMLIMuhN0b6c7i-A6k4kB4eEHgTAnjWC-pk01M'  # Acquire from developer.here.com
    i = 0
    loc = []
    coords = []
    location = location


    PARAMS = {'apikey': api_key, 'q': location}
    r = requests.get(url=URL, params=PARAMS)
    data = r.json()
    try:
        latitude = data['items'][0]['position']['lat']
        longitude = data['items'][0]['position']['lng']
        coords.append(latitude)
        coords.append(longitude)
        loc.append(coords)
    except IndexError:
        print('Error while geocoding')

    return loc


@app.route('/')
def hello_world():
  return render_template('index.html')


@app.route('/management')
def management():

    return render_template('mission_management.html')

@app.route('/flightmap')
def flightmap():

    return render_template('flightMap.html')

@app.route('/graphs')
def graphs():

    return render_template('graphs.html')

@app.route('/dbqueries')
def dbqueries():

    return render_template('database_queries.html')

@app.route('/mltool')
def mltool():

    return render_template('ml_tool.html')

@app.route('/reports')
def reports():

    return render_template('reports.html')

@app.route('/api/getMissionCoords',methods=['POST'])
def fetch():

    mission_id = int(request.form.get('mission_id'))

    conn = psycopg2.connect(
        host="localhost",
        database="delaer",
        user="postgres",
        password="stoapth1996")

    cur = conn.cursor()
    cur.execute("SELECT DISTINCT x,y,speed,height FROM flightpath JOIN flight On flight.id = flightpath.flightId WHERE flightpath.idrescuemission = " + str(mission_id))
    data = cur.fetchall()
    coords = []
    temp =[]
    for row in data:
        for el in row:
            temp.append(el)
        coords.append(temp)
        temp = []

    conn2 = psycopg2.connect(
        host="localhost",
        database="delaer_desired",
        user="postgres",
        password="stoapth1996")

    cur2 = conn2.cursor()
    cur2.execute(
        "SELECT DISTINCT x,y FROM missiondata WHERE missiondata.missionid = " + str(mission_id))
    data2 = cur2.fetchall()
    print(data2)
    coords2 = []
    temp2 = []
    for row in data2:
        print(row)
        for el in row:
            print(el)
            temp2.append(el)
        coords2.append(temp2)
        temp2 = []
    print(coords2)
    return render_template('flightMap.html', data = coords, data2 = coords2)





@app.route('/api/insertMissionData', methods=['POST'])
def insert():
    data = []
    id = int(request.form.get('mission_id'))
    d_point = request.form.get('d_point')
    m_point = request.form.getlist('m_point')
    a_point = request.form.get('a_point')
    option = request.form.getlist('sel1')
    no_item = request.form.getlist('no_item')

    geo_m_point = []
    geo_d_point = geocode(d_point)
    print(geo_d_point)
    for point in m_point:
        geo = geocode(point)
        geo_m_point.append(geo)

    geo_a_point = geocode(a_point)
    print(geo_a_point)
    conn = psycopg2.connect(
        host="localhost",
        database="delaer_desired",
        user="postgres",
        password="stoapth1996")

    cur = conn.cursor()
    postgres_insert_query = """ INSERT INTO missiondata (missionid, x, y,lifeboats,oxygenbottles,liferafts,
                                emergencybags,stretchers,lifejacket,adliferaft,equipment,transportboxes) 
                                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    record_to_insert1 = (id, geo_d_point[0][0] , geo_d_point[0][1],0,0,0,0,0,0,0,0,0)
    record_to_insert2 = (id, geo_a_point[0][0] , geo_a_point[0][1],0,0,0,0,0,0,0,0,0)



    cur.execute(postgres_insert_query, record_to_insert1)
    cur.execute(postgres_insert_query, record_to_insert2)

    for i in range(0,len(geo_m_point)-1):
        record_to_inser_gen = (id,geo_m_point[i][0][0],geo_m_point[i][0][1],0,0,0,0,0,0,0,0,0)
        cur.execute(postgres_insert_query, record_to_inser_gen)
    conn.commit()
    print('Data Sucesfully Inserted')

    return render_template('mission_management.html')


if __name__ == '__main__':
  app.run()

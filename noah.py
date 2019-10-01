#!/usr/bin/env python3
import requests
import time
import sys
import datetime
from google.cloud import bigquery

# --------- User Settings ---------
CITY = "hanoi"
TOKEN = # API Token
DATABASE = # BigQuery Database ID
TABLE = # BigQuery Table ID
INTERVAL = 60 # Waiting time (minutes) between jobs
# ---------------------------------

def get_data():
        url = "https://api.waqi.info/feed/" + CITY + "/?token=" + TOKEN
        try:
                response = requests.get(url)
        except:
                return []

        return response.json()

def pollutant_data(raw_data, p):
        iaqi = raw_data.get('iaqi')
        if iaqi:
                pollutant = iaqi.get(p)
                if pollutant:
                        return pollutant.get('v') 
        
        return -1

def insert_data(database, table, i):
        raw = get_data()
        raw_data = raw['data']

        # Requested data
        time = raw_data['time']['s'].split(' ')[1]
        date = raw_data['time']['s'].split(' ')[0]
        city = CITY.capitalize()
        aqi = raw_data['aqi']

        # Nullable data
        dominentPol = raw_data.get('dominentpol').upper()
        co = pollutant_data(raw_data, 'co')
        no2 = pollutant_data(raw_data, 'no2')
        o3 = pollutant_data(raw_data, 'o3')
        pm25 = pollutant_data(raw_data, 'pm25')
        dew = pollutant_data(raw_data, 'dew')

        data = (i, repr(time), repr(date), repr(city), aqi, repr(dominentPol), co, no2, o3, pm25, dew)
        # Insert data to BigQuery table
        query = "INSERT INTO {}.{} VALUES ({},{},{},{},{},{},{},{},{},{},{});".format(database, table, *data)

        return query


def main():
        
        previous_raw_data = None
        client = bigquery.Client()
        job = client.query('SELECT MAX(ID) FROM {}.{};'.format(DATABASE, TABLE))
        for row in job.result():
                current_index = row[0] + 1

        while True:

                raw_data = get_data()
                wait_time = INTERVAL
                delay = 0

                while raw_data == previous_raw_data:
                        time.sleep(300)
                        delay += 1
                        if delay == 60:
                                print("Unable to collect data from API.")
                                return None

                try:
                        query_addData = insert_data(DATABASE, TABLE, current_index)
                        client.query(query_addData)
                        current_index += 1

                        print("Data added at", datetime.datetime.now())
                except:
                        print("Error collecting data at " + str(datetime.datetime.now()) + " - " + sys.exc_info()[0])
                
                previous_raw_data = raw_data

                time.sleep(60 * (wait_time - delay))

if __name__ == "__main__":
        main()

import logging
import json
import os
from psycopg2 import connect, sql

from azure.functions import InputStream


def main(myblob: InputStream):
    logging.info(f"Python blob trigger function processed blob"
                f"Name: {myblob.name}"
                f"Blob Size: {myblob.length} bytes")
    logging.info(f"Processing blob: {myblob.name}")

    data = json.load(myblob)

    host=os.environ['host']
    user=os.environ['user']
    password=os.environ['password']

    conn = connect(
        host=host,
        database="postgres",
        user=user,
        password=password,
    )

    with conn.cursor() as cur:
        cur.execute(
            sql.SQL(
                """
                INSERT INTO public.station_data (timestamp, module, sensor_id, sensor_type, value, unit)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
            ),
            (
                data["timestamp"],
                data["module"],
                data["sensor_id"],
                data["sensor_type"],
                data["value"],
                data["unit"],
            ),
        )
        conn.commit()

    conn.close()

    logging.info(f"Data inserted successfully: {data}!")
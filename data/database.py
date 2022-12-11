import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def initialiseConnection():
    try:
        url = os.getenv("DATABASE_URL")
        connection = psycopg2.connect(url)

        print("DATABASE CONNECTED")
        return connection
    except (Exception, psycopg2.DatabaseError) as e:
        print("DATABASE NOT CONNECTED")
        print("CONNECTION Error: %s" % str(e))
        return None

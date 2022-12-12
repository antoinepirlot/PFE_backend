import os

import psycopg2
from dotenv import load_dotenv
from psycopg2 import pool

load_dotenv()


def initialiseConnection():
    try:
        user = os.getenv("USER")
        password = os.getenv("PASSWORD")
        host = os.getenv("HOST")
        url = os.getenv("DATABASE_URL")
        database = os.getenv("DATABASE")
        threaded_postgreSQL_pool = psycopg2.pool.ThreadedConnectionPool(1, 1, user=user,
                                                                    password=password,
                                                                    host=host,
                                                                    database=database) #TODO : put 5 connexions max


        if threaded_postgreSQL_pool:
            print("Connection pool created successfully using ThreadedConnectionPool")
        return threaded_postgreSQL_pool
    except (Exception, psycopg2.DatabaseError) as e:
        print("DATABASE NOT CONNECTED")
        print("CONNECTION Error: %s" % str(e))
        return None
def initConnection():
    try:
        url = os.getenv("DATABASE_URL")
        connection = psycopg2.connect(url)

        print("DATABASE CONNECTED")
        return connection
    except (Exception, psycopg2.DatabaseError) as e:
        print("DATABASE NOT CONNECTED")
        print("CONNECTION Error: %s" % str(e))
        return None



import os
import psycopg2
from psycopg2 import pool
from dotenv import load_dotenv

load_dotenv()


def initialiseConnection():
    try:
        user = os.getenv("USER")
        password = os.getenv("PASSWORD")
        host = os.getenv("HOST")
        database = os.getenv("DATABASE")
        threaded_postgreSQL_pool = psycopg2.pool.ThreadedConnectionPool(1, 5, user=user,
                                                                    password=password,
                                                                    host=host,
                                                                    database=database)
        if threaded_postgreSQL_pool:
            print("Connection pool created successfully using ThreadedConnectionPool")
        return threaded_postgreSQL_pool
    except (Exception, psycopg2.DatabaseError) as e:
        print("DATABASE NOT CONNECTED")
        print("CONNECTION Error: %s" % str(e))
        return None




# database.py

import mysql.connector

class Database:

    @staticmethod
    def get_connection():

        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            port=3306,
            database="billing_system"
        )
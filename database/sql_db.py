import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="learnTech@2022",
        database="mini_devin"
    )

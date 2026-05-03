import mysql.connector
import logging

logger = logging.getLogger('database')

def get_connection():
    """Create and return a MySQL database connection."""
    try:
        logger.debug("Creating MySQL database connection")
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="learnTech@2022",
            database="mini_devin"
        )
        logger.debug("MySQL database connection established successfully")
        return conn
    except Exception as e:
        logger.error(f"Failed to connect to MySQL database: {str(e)}", exc_info=True)
        raise

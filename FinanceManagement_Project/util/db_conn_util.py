import mysql.connector
from util.db_property_util import DBPropertyUtil

class DBConnUtil:
    @staticmethod
    def get_connection():
        try:
            config = DBPropertyUtil.get_connection_string('config/db.properties')
            conn = mysql.connector.connect(
                host=config['host'],
                port=config['port'],
                database=config['database'],
                user=config['user'],
                password=config['password']
            )
            return conn
        except Exception as e:
            print(f"Connection failed: {e}")
            return None

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from util.db_conn_util import DBConnUtil

conn = DBConnUtil.get_connection()
if conn:
    print("Connection successful!")
    conn.close()
else:
    print("Connection failed!")

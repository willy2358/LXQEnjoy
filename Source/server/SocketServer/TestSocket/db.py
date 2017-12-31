
import pymysql
import pymysql.cursors

dbConn = None

def get_connection():
    global dbConn
    if not dbConn:
        dbConn = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             db='SqlTest',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    return dbConn
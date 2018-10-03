

import pymysql
import pymysql.cursors



dbconn = "heell"

var1 = "hello"

def test1():
    global dbconn
    if not dbconn:
        print("None")
        dbconn = "connected"
    print(dbconn)


test1()

test1()

# def get_connection():
#     if not db_conn:
#         db_conn = pymysql.connect(host='localhost',
#                              user='root',
#                              password='root',
#                              db='SqlTest',
#                              charset='utf8mb4',
#                              cursorclass=pymysql.cursors.DictCursor)
#     else:
#         return db_conn
#
#
#
# try:
#     # with connection.cursor() as cursor:
#     #     # Create a new record
#     #     sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
#     #     cursor.execute(sql, ('webmaster@python.org', 'very-secret'))
#     #
#     # # connection is not autocommit by default. So you must commit to save
#     # # your changes.
#     # connection.commit()
#
#     with connection.cursor() as cursor:
#         # Read a single record
#         sql = "SELECT `userid`, `username` FROM `user` WHERE userid=29"
#         cursor.execute(sql)
#         result = cursor.fetchone()
#         print(result)
# finally:
#     connection.close()
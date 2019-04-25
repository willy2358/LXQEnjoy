

# import pymysql
# import pymysql.cursors

from Crypto.Hash import SHA
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
import base64



dbconn = "heell"

var1 = "hello"

def verify(data, signature):
	key = RSA.importKey(open('/Users/willy/MyCodes/lxqenjoy/Source/server/SocketServer/TestSocket/configs/clients/pub512.pem').read())
	h = SHA.new(data)
	verifier = PKCS1_v1_5.new(key)
	if verifier.verify(h, base64.b64decode(signature)):
		print("verified")
	else:
		print("invalid")


oriSalt = "e43879b5-4cf8-485c-939c-76ed531feee6"
sig = "FAoIWmjZRPmdOWj+LFL9LwpR6pTcVDGnI/nUgU/jIv8r4WXYE0M+cj2O/u+mjx76jKInKmsWn6jIZPJ/vVdlWQ=="
bys = oriSalt.encode('utf-8')
verify(bys, sig)
# def test1():
#     global dbconn
#     if not dbconn:
#         print("None")
#         dbconn = "connected"
#     print(dbconn)


# test1()
#
# test1()

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
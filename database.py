import mysql.connector as MYSQL
from decouple import config

def db_connector():
    # connects to database
    my_db = MYSQL.connect(host='localhost',username=config('user'),passwd=config('passwd'),database='wit_tnp')
    my_cursor = my_db.cursor()
    return my_db, my_cursor
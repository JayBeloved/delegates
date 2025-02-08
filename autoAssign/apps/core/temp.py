import pymysql

config = {
    'user': 'ruimun_db',
    'password': 'Ruimun1#',
    'host': '66.96.130.100',
    'database': 'ruimun',
    'port': 3306,
}

try:
    connection = pymysql.connect(**config)
    print("Connection successful!")
    connection.close()
except pymysql.MySQLError as err:
    print(f"Error: {err}")

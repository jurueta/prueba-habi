import json
from mysql.connector import connect
from mysql.connector.errors import ProgrammingError
import os

def connect_db():
    """
        Create conecction with the DataBase With credencials provide in .env
    """
    try:
        conection = connect(
            host = os.getenv("HOSTDB", "3.130.126.210"),
            port = os.getenv("PORTDB", "3309"),
            user = os.getenv("USERDB", "pruebas"),
            passwd = os.getenv("PASSWDDB", "VGbt3Day5R"),
            database = os.getenv("DATABASE", "habi_db")
        )
        return conection
    except Exception as error:
        raise(error)


def property(event, context):
    """
        EndPoint property:
            - only accept method get
            - Show all proprety in status pre_venta, en_venta, vendido
            - filters in year, city and status
    """
    try:
        db_connection = connect_db()
        cursor = db_connection.cursor(dictionary=True)
    except Exception:
        return response_api(500, {"message": "Error to connect with database"})

    query_property = """SELECT p.address, p.city, p.price, p.description, p.year, s.name as status
        FROM property p
        INNER JOIN status_history sh ON sh.id = (SELECT id 
        FROM status_history 
        WHERE property_id = p.id 
        ORDER BY update_date 
        DESC LIMIT 1)
        INNER JOIN status s ON s.id = sh.status_id
        WHERE sh.status_id IN (3,4,5) """
    
    # filters
    if event["multiValueQueryStringParameters"]:
        params = event["multiValueQueryStringParameters"]

        filters_data = {
            "year": " AND p.year = {}",
            "city": " AND p.city = '{}'",
            "status": " AND s.name = '{}'"
        }

        # List comprehension of filters
        query_conditions = " ".join([
            filters_data[param[0]].format(param[1][0]) 
            for param in params.items() 
            if param[0] in filters_data.keys()
            ])

        query_property += query_conditions

    # Show response
    try:
      cursor.execute(query_property)
      result_property = cursor.fetchall()
    except ProgrammingError:
        return response_api(400, {"message": "Check the filters"})

    return response_api(200, result_property)


def response_api(code, body):
    """ 
        Render response by code and body 
    """
    response = {
        "statusCode": code,
        "body": json.dumps(body)
        }
    return response

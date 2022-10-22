from flask import Flask, request
import psycopg2
import os
from configparser import ConfigParser
#from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

def config(filename = 'database.ini', section = 'postgresql'):
    parser = ConfigParser()
    parser.read(filename)
    
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    return db

conn = None
print(config())
print("!!!!!!!!!!!!!!!!!!!!!", os.getenv("USEREXAMPLE"))

#Index
@app.route("/")
def index():
    return "This is the app index"

#Add client and money
@app.route("/add", methods=['POST'])
def add_client():
    name=request.args.get('name')
    money= request.args.get('money')
    sql = """INSERT INTO clients(name, money)
                    VALUES(%s, %s) RETURNING id"""
    try:
        print(name)
        print(money)
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql, (name, money))
        id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        return "Client added with id={}".format(id)
    except (Exception, psycopg2.DatabaseError) as error:
        return str(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

#Get all clients
@app.route("/getall", methods=['GET'])
def get_all():
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        sql = """SELECT * FROM clients;"""
        cur.execute(sql)
        query = cur.fetchall()
        return query
    except (Exception, psycopg2.DatabaseError) as error:
        return str(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

# #Get client by ID
@app.route("/get/<id_>", methods=['GET'])
def get_by_id(id_):
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        sql = """SELECT * FROM clients c WHERE 
                    c.id = %s;"""
        cur.execute(sql, id_ )
        query = cur.fetchall()
        return query
    except (Exception, psycopg2.DatabaseError) as error:
        return str(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

#Get client by Name
@app.route("/getname/<name_>", methods=['GET'])
def get_by_name(name_):
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        print(name_)
        sql = """SELECT id, name, money FROM clients c WHERE 
                    c.name = %s;"""
        cur.execute(
                    """
                    SELECT id, name, money 
                    FROM clients c
                    WHERE c.name = %s;
                    """,
                    [name_,]
)
        query = cur.fetchall()
        print(query)
        return (query)
    except (Exception, psycopg2.DatabaseError) as error:
        return str(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

# if __name__ == '__main__':
#     app.run(host="0.0.0.0", port=80)

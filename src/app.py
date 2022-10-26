#Simple aplicación que se conecta con una bd de postggres para insertar y obtener infomación

from flask import Flask, request
import psycopg2
import os

app = Flask(__name__)


conn = None

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
        conn = psycopg2.connect(
            host        =   os.getenv('DB_HOST'),
            database    =   os.getenv('DB_NAME'),
            user        =   os.getenv('DB_USERNAME'),
            password    =   os.getenv('DB_PASSWORD')
        )
            
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
        conn = psycopg2.connect(
            host        =   os.getenv('DB_HOST'),
            database    =   os.getenv('DB_NAME'),
            user        =   os.getenv('DB_USERNAME'),
            password    =   os.getenv('DB_PASSWORD')
        )
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
        conn = psycopg2.connect(
            host        =   os.getenv('DB_HOST'),
            database    =   os.getenv('DB_NAME'),
            user        =   os.getenv('DB_USERNAME'),
            password    =   os.getenv('DB_PASSWORD')
        )
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
        conn = psycopg2.connect(
            host        =   os.getenv('DB_HOST'),
            database    =   os.getenv('DB_NAME'),
            user        =   os.getenv('DB_USERNAME'),
            password    =   os.getenv('DB_PASSWORD')
        )
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

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)

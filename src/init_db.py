import os
import psycopg2
from configparser import ConfigParser


#Este modulo servira para conectarnos a la db, volver a crear la tabla clients y llenarla con 2 clientes

#Datos necesarios para la conexion
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
try:
    #Borro la tabla si existe, luego inserto algunos registros
    sql = """INSERT INTO clients(name, money)
             VALUES(%s, %s) RETURNING id;"""
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    print('connected')
    cur.execute('DROP TABLE IF EXISTS clients;')
    cur.execute('CREATE TABLE clients (id serial PRIMARY KEY,'
                                       'name varchar (150) NOT NULL UNIQUE,'
                                       'money varchar (150) NOT NULL,'
                                      'date_added date DEFAULT CURRENT_TIMESTAMP);'
                                  )
    cur.execute(sql, ("Andres", 200,))
    cur.execute(sql, ("Camilo", 300,))
    cur.execute(sql, ("Laura", 400,))
    cur.execute(sql, ("Felipe", 400,))
    id = cur.fetchone()[0]
    print(id)
    conn.commit()
    cur.close()
except (Exception, psycopg2.DatabaseError) as error:
    print(error)
finally:
    if conn is not None:
        conn.close()
        print('Database connection closed.')


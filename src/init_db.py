import os
import psycopg2



#Este modulo servira para conectarnos a la db, volver a crear la tabla clients y llenarla con 2 clientes


    
conn = None
try:
    #Borro la tabla si existe, luego inserto algunos registros
    sql = """INSERT INTO clients(name, money)
             VALUES(%s, %s) RETURNING id;"""
    conn = psycopg2.connect(
            host        =   os.getenv('DB_HOST'),
            database    =   os.getenv('DB_NAME'),
            user        =   os.getenv('DB_USERNAME'),
            password    =   os.getenv('DB_PASSWORD')
        )
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


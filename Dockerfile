#Archivo usado para crear la imagen de docker que contiene la aplicacion de flask
#Simplemente copia los requerimientos, los instala y finalmente ejecuta la aplicación. 
#También expone el puerto 80, que es el puerto donde escucha la app
FROM python:3.8
WORKDIR /app
COPY src .
COPY requirements.txt .
RUN pip install -r requirements.txt 


CMD ["python", "app.py"]


EXPOSE 80
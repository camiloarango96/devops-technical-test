# Introducción

Este proyecto busca desplegar una aplicación muy simple hecha en Flask, la cual solo debe devolver al usuario información básica sobre un cliente, y también debe permitir insertar información de un cliente, en mi caso de una base de datos.

# Herramientas

## Terraform
Para el despliegue de infraestructura, decidí usar Terraform, pues ya estaba familiarizado con esta herramienta, y además, gracias a su buena documentación, se hace más fácil de usar

## Python
La escritura de algunos scripts fue necesaria, y para esto usé pyhton, junto con boto3, que es una librería que me permite interactuar con AWS

## EKS/Kubernetes
 Si bien es un aplicación muy básica, decidí usar EKS (AWS) para desplegarla, la razón de esto no fue más que desafiarme a aprender una nueva herramienta, aunque ya estaba familiarizado con Kubernetes, nunca había hecho el despliegue de un cluster de EKS usando Terraform

## RDS/Postgres
 Para la base de datos usé RDS, ya que estaba familiarizado con este servicio, al igual que con el motor de Postgres, así que para mi fue mucho más fácil modificar la app de Flask para crea una conexión con la base de datos Postgres creada en RDS

## Fluent Bit/Cloud Watch/Container Insights
De monitoreo no tenía mucho conocimiento, sin embargo encontré una solución, que era usar estas 3 herramientas para los logs, y me pareció fácil de implementar, otra ventaja que tiene es que puede ser accedido desde la misma consola de AWS

## GitHub Actions
Usé GitHub Actions para automatizar la integración y despliegue de la app, decidí usar esta herramienta porque ya venía integrada con GitHub, así que no requiere de muchas configuraciones adicionales para que funcione

## AWS
Usé AWS para toda la infraestructura, pues es la nube con la que mas familiarizado estoy y todos los recursos necesarios para el despliegue los encontré en esta nube. Otra ventaja fue la capa gratuita.

# Requisitos
### Dominio
En mi caso usé un dominio creado en Route53 de AWS (olimac.link)
### Certificado SSL
Para garantizar la conexión https, es necesario tener un certificado SSL, en mi casó creé uno en ACM, este certificado sirve para el dominio anteriormente mencionado.
##Credenciales
Se requieren de credenciales para AWS, las cuales serán guardadas como secrets en el repo, lo mismo sucede con las credenciales de Dockerhub, adicionalmente tambien se deben guardar como secretos las credenciales que se usarán para la creación de la RDS (usuario y contraseña)


# Arquitectura 
![alt text](https://github.com/camiloarango96/devops-technical-test/blob/main/arqui.png?raw=true)

Aquí se observa la arquitectura que tendrá la aplicación, en primer lugar esta el dominio, el cual tiene un record de tipo CNAME para apuntar al DNS del Balanceador de carga creado por kubernetes. Para dar acceso a internet al cluster de EKS es necesario crear VPC públicas en 2 zonas de disponibilidad, en mi caso fue en us-east-1a y us-east-1b, estas zonas cuentan con una route table, en la cual se indica que todo el tráfico que reciban, se envía al Internet Gateway, luego se tienen 2 VPC privadas, una en la AZ us-east-1a y la otra en us-east-1b, estas VPC cuentan con una route table en la que se indica que todo el tráfico se debe enviar al NAT Gateway. También se tiene el cluster de EKS, el cual cuenta inicialmente con 2 nodos, pero que puede escalar hasta 5 nodos. En estos nodos se encuentran algunos pods encargados enviar los logs a CloudWatch, pero tambien están los pods de la app de Flask, estos pods específicamente, se conectaran con la base de datos postgres, la cual se encuentra en una VPC aparte.


# Pipeline

## Creación de artefacto
En primer lugar es necesario la creación de un artefacto, para este caso se crea un imagen de Docker usando el DockerFile que se encuentra en la raíz del repositorio. Este artefacto, una vez creado, será almacenado en Dockerhub, para esto son necesarias las credenciales de Dockerhub

## Despliegue de infraestructura
Para este paso se accede a la carpeta iac, donde estaran todos los archivos de Terraform, con los cuales se desplegará la infraestructura. Aquí se depliegan todos los servicios que se ven en el diagrama de infraestructura, menos el dominio de Route 53 y CloudWatch

## Despligue Kubernetes
Una vez se tiene listo el cluster de EKS, es necesario comenzar con el despliegue de la aplicación, para esto se accede a la carpeta k8s y se aplican todos los archivos YAML, esto creará: Un autoscaler, para escalar la aplicación si es necesario, un balanceador de carga clásico y un despliegue de la aplicación de Flask, para este último elemento, se usa la imagen que se subió anteriormente a Dockerhub. Adicionalmetne se inyectan las credenciales de base de datos al despliegue de Flask. Es importante mencionar que al balanceador de carga se le indica el certificado SSL anteriormente creado (mediante un arn) para garantizar la conexión por https

## Creación de variables de entorno adicionales para la DB e inicialización
En este paso se accede a la carpeta scripts, y se ejecutan dbscript.py, lo que hace este script es que agrega 2 datos necesarios (Host y nobre de la base de datos) para la conexión a base de datos al despliegue de kubernetes, seguidamente crea una tabla clients en la BD postgres de RDS y agrega unos cuantos datos de prueba.

## Creación de record en Route 53
Para podernos conectar a la app, usando un dominio de Route 53, es necesario crear un record de tipo CNAME, que apunte al DNS del balanceador de carga. Esto también es necesario para poder usar el certificado. En mi caso el subdominio resultante para la app es: flask.olimac.link

## Monitoreo
En este último paso es necesario habilitar el logging de EKS, una vez se hace esto, se deben aplicar las configuraciones de fluent bit y crear un agente de CloudWatch. El monitoreo se podrá hacer usando Container Insights (CloudWatch)

# Uso de la aplicación

```python
[GET] flask.olimac.link/getall
Devuelve todos los registros de la base de datos (id, nombre y dinero)

[POST] flask.olimac.link/add?name=<name>&money=<money> 
Agrega un nuevo registro y se devuelve el id del cliente insertado

[GET] flask.olimac.link/get/<id>
Devuelve la informaci[on del cliente que tenga el id proporcionado

```




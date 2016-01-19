# Entorno de pruebas: [Docker](https://www.docker.com/)

El primer paso para crear la imagen es definir un archivo [Dockerfile](https://github.com/javiergarridomellado/IV_javiergarridomellado/blob/master/Dockerfile).  Docker usa dicho archivo para definir la imagen, en mi caso contiene lo siguiente:
```
FROM ubuntu:latest

#Autor
MAINTAINER Francisco Javier Garrido Mellado <franciscojaviergarridomellado@gmail.com>

#Actualización del Sistema 
RUN sudo apt-get -y update

#Descarga de la aplicación
RUN sudo apt-get install -y git
RUN sudo git clone https://github.com/javiergarridomellado/IV_javiergarridomellado.git

# Instalación de Python y PostgreSQL
RUN sudo apt-get install -y python-setuptools
RUN sudo apt-get -y install python-dev
RUN sudo apt-get -y install build-essential
RUN sudo apt-get -y install python-psycopg2
RUN sudo apt-get -y install libpq-dev
RUN sudo easy_install pip
RUN sudo pip install --upgrade pip

#Instalación de dependencias de la aplicacion

RUN cd IV_javiergarridomellado/ && sudo pip install -r requirements.txt

#Sincronización de la base de datos
RUN cd IV_javiergarridomellado/ && python manage.py syncdb --noinput

```
Después en la web de [Docker Hub](https://hub.docker.com/), se pulsa en "Create" y despues en "Create Automated Build" sobre el repositorio del proyecto, con esto se comienza a crear la imagen.

Puede verse a continuación el repositorio enlazado y la construcción automática de la imagen:

![repositorio](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/enlace_zpsmkcd2cx6.png)

![imagen](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/imagen_zpstbyi9pf3.png)

Por tanto, cada cambio que se realice al repositorio de Github se integra de manera automática y en tiempo real a la imagen de Docker Hub.Cada vez que se haga un "git push" llevará asociado un rebuild de la imagen.

Para crear el entorno de pruebas en nuestro ordenador se ha provisto de un script en la ruta `IV_javiergarridomellado/scripts`.Solo hay que ejecutar el archivo **docker_install_and_run.sh**(no olvidar dar permisos de ejecución con chmod al archivo):
```
./docker_install_and_run.sh
```
El contenido del archivo es el siguiente:
```
sudo apt-get update
sudo apt-get install -y docker.io
sudo docker pull javiergarridomellado/iv_javiergarridomellado:apuestas
sudo docker run -t -i javiergarridomellado/iv_javiergarridomellado:apuestas /bin/bash
```
Esto lo que hace es instalar Docker, crear el contenedor con la aplicación instalada en él y arrancar el entorno de pruebas.Solo queda ingresar en el directorio `IV_javiergarridomellado` y ejecutar `python manage.py runserver 0.0.0.0:1111`(puede usarse otro puerto).Otra manera de ejecutar la aplicación es ejecutar el archivo `run_app.sh` tal y como se explica en el Readme principal.
Hecho esto, solo queda acceder al navegador anfitrión e introducir la IP del contenedor Docker.

![automa](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/automa_zpsajhntukm.png)

![navegador](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/nav_zpszfauvqbh.png)

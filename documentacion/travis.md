# Integración continua con Travis

Para el uso de Travis los pasos seguidos han sido:
- Registrarse en la página y sincronizar el repositorio.
- Tener un archivo de testeo de la aplicación.
- Tener un archivo manage.py que facilite la automatización del testeo.
- Tener un archivo .yml donde se le indica los pasos a seguir para cumplir con la integración continua de manera correcta y eficiente.
- En *github*, en el apartado *Setting/Webhooks&services* hay que activar el apartado de *Travis*, seguidamente se pulsa *Test Service*.

El contenido del archivo *.travis.yml* es el siguiente:
```
language: python
python:
 - "2.7"

install:
 - pip install -r requirements.txt
script:
 - python manage.py test 
```
Por último una captura de una modificación realizada al código del repositorio:

![travis](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/travis_zpsjqr6xhcs.png)

# Integración continua con Snap CI

Se añade ademas un proceso de integración continua junto al despliegue en Heroku mediante [Snap-CI](https://snap-ci.com).Desde la interfaz web realizo la siguiente configuración:

![paso1](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/snap1_zpsgowrqt6s.png)

![paso2](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/snaptest_zpsjmbr7ezk.png)

![paso3](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/snapdespliegue_zpsgoc8n8bo.png)

![resultados1](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/snappasantest_zpstn0bgbtl.png)

![resultados2](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/snaptest2_zps2t6125ue.png)

![resultados3](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/snapdespliegue2_zpsgmdw0np4.png)

Con todo esto queda realizado la integración continua, cada vez que se haga un push al repositorio se pasan los tests y si son satisfactorio se levanta la app.

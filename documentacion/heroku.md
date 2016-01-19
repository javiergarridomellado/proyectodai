# Despliegue en un Paas: Heroku

Para su despliegue he necesitado de los siguientes archivos:
- [Procfile](https://github.com/javiergarridomellado/IV_javiergarridomellado/blob/master/Procfile):
```
web: gunicorn apuestas.wsgi --log-file -
```

- [runtime.txt](https://github.com/javiergarridomellado/IV_javiergarridomellado/blob/master/runtime.txt):
```
python-2.7.6
```
- [requirements.txt](https://github.com/javiergarridomellado/IV_javiergarridomellado/blob/master/requirements.txt)
```
Django==1.8.6
argparse==1.2.1
dj-database-url==0.3.0
dj-static==0.0.6
django-toolbelt==0.0.1
djangorestframework==3.3.1
foreman==0.9.7
futures==3.0.3
gunicorn==19.3.0
psycopg2==2.6.1
requests==2.8.1
requests-futures==0.9.5
static3==0.6.1
wheel==0.26.0
whitenoise==2.0.4
wsgiref==0.1.2
```
Puede verse que tambien se dispone de **whitenoise** para archivos estaticos, queda definido en **setting.py** para su uso si se requiere.
Tras el registro en Heroku hay que ejecutar una serie de comandos para tener apunto el despliegue:
```
wget -O- https://toolbelt.heroku.com/install-ubuntu.sh | sh   
heroku login
heroku create
git add .
git commit -m "subida"
heroku apps:rename apuestas
git push heroku master
```
Cuando la aplicación se encuentre desplegada en Heroku usará la base de datos **PostgreSQL** que nos proporcionan( se define en setting.py, asi cuando la aplicación se encuentre en Heroku usara dicha base de datos ), en local sigo usando **SQLite**, lo he realizado con estos pasos:
- Teniendo *psycopg2* para poder usar dicha base de datos.
- Tener instalado *dj_database_url*, tambien necesario para PostgreSQL.
- Abrir el archivo *setting.py* del proyecto y añadir lo siguiente( sacado del siguiente [enlace](http://stackoverflow.com/questions/26080303/improperlyconfigured-settings-databases-is-improperly-configured-please-supply)):
```
import dj_database_url

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
ON_HEROKU = os.environ.get('PORT')
if ON_HEROKU:
	DATABASE_URL='postgres://url_de_mi_bd'
	DATABASES = {'default': dj_database_url.config(default=DATABASE_URL)}

STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
```
- En el archivo **wsgi.py** hay que poner lo siguiente:
```
import os

from django.core.wsgi import get_wsgi_application
from dj_static import Cling
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apuestas.settings")

#from whitenoise.django import DjangoWhiteNoise
application = get_wsgi_application()


application = Cling(get_wsgi_application())
#application = DjangoWhiteNoise(application)
```
- Notar que en DATABASE_URL se pone la url de la base de datos PostgreSQL que Heroku nos ofrece, hay que darle a show para verlo.
- Subir cambios a github y hacer **git push heroku master**.
- Ejecutar los comando **heroku run python manage.py makemigrations**, **heroku run python manage.py migrate** y **heroku run python manage.py createsuperuser** para sincronizar la base de datos PostgreSQL.
 

La aplicacion [desplegada](https://apuestas.herokuapp.com/)

Si hay algun problema en algun push de heroku hacer:
```
heroku create --stack cedar
```

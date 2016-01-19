#!/bin/bash
sudo apt-get install wget
wget -O- https://toolbelt.heroku.com/install-ubuntu.sh | sh   # descargar herramienta heroku CLI
cd ..
sudo heroku login
sudo heroku create
sudo git add .
sudo git commit -m "heroku deploy"
sudo git push heroku master
sudo heroku run python manage.py syncdb --noinput
sudo heroku ps:scale web=1
#renombrada con este nombre para no machacar la que ya tengo funcionando
sudo heroku apps:rename pruebaheroku
sudo heroku open app

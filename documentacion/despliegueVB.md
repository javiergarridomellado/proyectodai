## Despliegue en VirtualBox

Para el despliegue en una máquina de VirtualBox he usado [Vagrant](https://www.vagrantup.com/) para la creación y [Ansible](http://www.ansible.com/) para su provisionamiento y despliegue de la aplicación.

El primer paso es instalar el provisionador de azure para vagrant
```
vagrant plugin install vagrant-azure
```

![installvagrantazure](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/installvagranazure_zpsad7pzrjg.png)


El siguiente paso es definir el archivo [Vagrantfile](https://github.com/javiergarridomellado/IV_javiergarridomellado/blob/master/VagrantLocal/Vagrantfile) que se encarga de la creación de la máquina virtual en VirtualBox:
```
Vagrant.configure('2') do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://atlas.hashicorp.com/search.
  config.vm.box = 'ubuntu'
  config.vm.network "forwarded_port", guest: 22, host:2222, id: "ssh", auto_correct: true
  config.vm.network "forwarded_port", guest: 80, host:8080, id: "web", auto_correct: true
  config.vm.define "localhost" do |l|
          l.vm.hostname = "localhost"
   end

   config.vm.provision "ansible" do |ansible|
      ansible.sudo = true
      ansible.playbook = "iv.yml"
      ansible.verbose = "v"
      ansible.host_key_checking = false
  end
end

```

En el primer bloque lo que hago es indicarle el box que va a usar, en este caso Ubuntu, que haga reenvio de puertos de SSH y Web y le aplico como hostname "localhost" para que Ansible pueda conectar con la máquina.

En el segundo bloque  se ejecuta el "playbook" de Ansible que se llama [iv.yml](https://github.com/javiergarridomellado/IV_javiergarridomellado/blob/master/VagrantLocal/iv.yml):
```
- hosts: localhost
  sudo: yes
  remote_user: vagrant
  tasks:
  - name: Actualizar sistema 
    apt: update_cache=yes upgrade=dist  
  - name: Instalar paquetes
    apt: name=python-setuptools state=present
    apt: name=build-essential state=present
    apt: name=python-pip state=present
    apt: name=git state=present
  - name: Ins Pyp
    action: apt pkg=python-pip
  - name: Postgre
    command: sudo easy_install pip
    command: sudo pip install --upgrade pip
    command: sudo apt-get install -y python-dev libpq-dev python-psycopg2
  - name: Obtener aplicacion git
    git: repo=https://github.com/javiergarridomellado/IV_javiergarridomellado.git  dest=DAI clone=yes force=yes
  - name: Permisos de ejecucion
    command: chmod -R +x DAI
  - name: Instalar requisitos
    command: sudo pip install -r DAI/requirements.txt
  - name: ejecutar
    command: nohup sudo python DAI/manage.py runserver 0.0.0.0:80
```

Aquí le indico como hosts "localhost" ya que esto se ejecuta dentro de la máquina.En los task se actualiza el sistema, se instalan paquetes necesarios, se instala PostgreSQL, se clona el repositorio y por último se ejecuta la aplicación.Se usa "nohup" para que siga ejecutando la aplicación cuando se cierre el terminal.

Para realizar el despliegue basta con ejecutar [create_and_run](https://github.com/javiergarridomellado/IV_javiergarridomellado/blob/master/VagrantLocal/create_and_run.sh) que consta de lo siguiente:
```
#!/bin/bash
vagrant box add ubuntu https://cloud-images.ubuntu.com/vagrant/trusty/current/trusty-server-cloudimg-amd64-vagrant-disk1.box
vagrant up
```
En él se le indica que debe descargar la "box" de Ubuntu y después realizar un "vagrant up". Ejecutado esto vemos como se crea la máquina y se provisiona. 
![ansible](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/vagrantupazure_zpscx7wl4dk.png)

Para visitar la aplicación desplegada solo es necesario usar la url *localhost:8080*:

![appdespl](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/vagrantlocalprac_zpsngaayexq.png)

![ssh](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/vagrantsshlocalprac_zpspgnpiqfp.png)


*Nota: Para su correcto funcionamiento es necesario tener instalado lo siguiente :*
```
$ sudo apt-get install nodejs-legacy
$ sudo apt-get install npm
$ sudo npm install -g azure-cli
$ sudo pip install paramiko PyYAML jinja2 httplib2 ansible
$ sudo dpkg -i vagrant_1.8.1_x86_64.deb
$ vagrant plugin install vagrant-azure
```



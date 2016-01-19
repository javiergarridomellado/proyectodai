## Despliegue en un Iaas: Azure

Para el despliegue en una máquina de Azure he usado [Vagrant](https://www.vagrantup.com/) para la creación y [Ansible](http://www.ansible.com/) para su provisionamiento y despliegue de la aplicación.

El primer paso es instalar el provisionador de azure para vagrant
```
vagrant plugin install vagrant-azure
```

![installvagrantazure](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/installvagranazure_zpsad7pzrjg.png)

El siguiente paso es loguearse y conseguir información de las credenciales de Azure( al ejecutar **azure account download** hay que acceder al enlace que nos facilita):
```
azure login
azure account download
```

Acto seguido importo a mi CLI de Azure mis credenciales:
```
azure account import Azure\ Pass-1-15-2016-credentials.publishsettings
```

![importarcredenciales](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/azureimport_zpsfwwiqjcc.png)


El siguiente paso es generar los certificados que se van a subir a Azure y nos va a permitir interaccionar con el:
```
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout azurevagrant.key -out azurevagrant.key
chmod 600 ~/.ssh/azurevagrant.key
openssl x509 -inform pem -in azurevagrant.key -outform der -out azurevagrant.cer
```

El siguiente paso es subir el archivo **.cer** a [Azure](https://manage.windowsazure.com/@franciscojaviergarmelhotmai.onmicrosoft.com#Workspaces/AdminTasks/ListManagementCertificates):


![certificado](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/subircredencial_zpshfktx7xg.png)

Para poder autenticar Azure desde Vagrantfile es necesario crear un archivo **.pem** y concatenarle el archivo **.key**, para ello:
```
openssl req -x509 -key ~/.ssh/id_rsa -nodes -days 365 -newkey rsa:2048 -out azurevagrant.pem
cat azurevagrant.key > azurevagrant.pem
```

Realizado estos pasos se procede a definir el archivo [Vagrantfile](https://github.com/javiergarridomellado/IV_javiergarridomellado/blob/master/VagrantAzure/Vagrantfile) que se encarga de la creación de la máquina virtual en Azure:
```
Vagrant.configure('2') do |config|

  config.vm.box = 'azure'
  config.vm.network "public_network"
  config.vm.network "private_network",ip: "192.168.56.10", virtualbox__intnet: "vboxnet0"
  config.vm.network "forwarded_port", guest: 80, host: 80
  config.vm.define "localhost" do |l|
          l.vm.hostname = "localhost"
   end

  config.vm.provider :azure do |azure, override|
      azure.mgmt_certificate = File.expand_path('/home/javi/Escritorio/VagrantIV/azurevagrant.pem') 
      azure.mgmt_endpoint = 'https://management.core.windows.net'
      azure.subscription_id = '477d87d6-b8d0-4025-8c1f-a3de5c520c99'
      azure.vm_image = 'b39f27a8b8c64d52b05eac6a62ebad85__Ubuntu-14_04_2-LTS-amd64-server-20150506-en-us-30GB'
      azure.vm_name = 'restaurante'
      azure.cloud_service_name = 'apuestas'  
      azure.vm_password = 'Clave#Javi#1'
      azure.vm_location = 'Central US' 
      azure.ssh_port = '22'
      azure.tcp_endpoints = '80:80'
  end	

  config.vm.provision "ansible" do |ansible|
      ansible.sudo = true
        ansible.playbook = "iv.yml"
        ansible.verbose = "v"
        ansible.host_key_checking = false
  end
end
```

En el primer bloque lo que hago es indicarle el box que va a usar, en este caso Azure, que tenga acceso a Internet mediante una red pública, una red privada, que haga reenvio de puertos y le aplico como hostname "localhost" para que Ansible pueda conectar con la máquina.

En el segundo bloque se configuran las propiedades de mi servicio de Azure, se le indica la ruta del certificado de Azure, el "endpoint", la imagen Ubuntu que va a usar, el nombre de la máquina, el nombre del cloud,la password,etc.

Por último, se ejecuta el "playbook" de Ansible que se llama [iv.yml](https://github.com/javiergarridomellado/IV_javiergarridomellado/blob/master/VagrantAzure/iv.yml):
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

Para realizar el despliegue basta con ejecutar [create_and_run](https://github.com/javiergarridomellado/IV_javiergarridomellado/blob/master/VagrantAzure/create_and_run.sh) que consta de lo siguiente:
```
#!/bin/bash
vagrant box add azure https://github.com/msopentech/vagrant-azure/raw/master/dummy.box
vagrant up --provider=azure
```
En él se le indica que debe descargar la "box" de Azure y después realizar un "vagrant up". Ejecutado esto vemos como se crea la máquina y se provisiona. 

![ansible](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/vagrantupazure_zpscx7wl4dk.png)

El enlace a la aplicación es el siguiente [http://apuestas.cloudapp.net/](http://apuestas.cloudapp.net/)

![appdespl](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/vagrantazureprac_zps0btpmjnn.png)




*Nota: Para su correcto funcionamiento es necesario tener instalado lo siguiente :*
```
$ sudo apt-get install nodejs-legacy
$ sudo apt-get install npm
$ sudo npm install -g azure-cli
$ sudo pip install paramiko PyYAML jinja2 httplib2 ansible
$ sudo dpkg -i vagrant_1.8.1_x86_64.deb
$ vagrant plugin install vagrant-azure
```




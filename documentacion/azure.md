##Configuración Máquina Azure

###Creación

Para ello hay que tener cuenta en Azure y crédito para usar sus servicios. El primer paso para crear la máquina virtual es pulsar en la pestaña de nuevo proceso y seleccionar una Ubuntu 14.04( he usado la opción "Administrador de recursos"). Después se le asigna un nombre al servidor, una contraseña y el tipo de suscripción:

![crear](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/1_zpsxeo9hnwy.png)

![crear2](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/2_zpsgvaw4tqr.png)

![crear3](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/4_zps4vukthux.png)

###Reglas de tráfico de red

El siguiente paso es indicarle a la máquina virtual las reglas de entrada y salida:

-Reglas de entrada:

![entrada](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/reglaentrada_zpsj2gxhn4y.png)

-Reglas de salida:

![reglassalida](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/reglasalida_zpsqlohycpd.png)

Falta definir el NAT para el contenedor (explicado en el apartado de [fabric](https://github.com/javiergarridomellado/IV_javiergarridomellado/blob/master/documentacion/fabfile.md)), esto se hará cuando se disponga de él. Si queda dudas sobre como configurar las reglas puede consultarse el siguiente [tutorial](https://azure.microsoft.com/es-es/documentation/articles/virtual-networks-create-nsg-arm-pportal/).

###Configurar nombre de DNS

Para ello hay que seleccionar la IP pública de la máquina y disociarla, posteriormente seleccionar configuración e indicarle el nombre de DNS que queremos para nuestra máquina, lo siguiente será volver a tener IP pública. Para ello, hay que seleccionar la pestaña de Direcciones IP y habilitar la dirección IP pública.Hecho esto queda configurado el nombre de DNS.

![asignardns](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/asignardominio_zpscpgt6ky6.png)

![ssh](http://i1045.photobucket.com/albums/b457/Francisco_Javier_G_M/ssh_zps47wbvejn.png)

Si surge alguna duda puede consultarse el siguiente [tutorial](https://azure.microsoft.com/es-es/documentation/articles/virtual-machines-create-fqdn-on-portal/)

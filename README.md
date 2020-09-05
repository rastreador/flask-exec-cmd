# flask-exec-cmd

[![Creative Commons License](https://licensebuttons.net/l/by-sa/4.0/88x31.png)](https://creativecommons.org/licenses/by-sa/4.0/ "CC BY-SA 4.0")

## Descripción

Esta pequeña aplicación está desarrollada en Flask y permite la ejecución de un comando de sistema a través de la web y que se muestre la salida del comando.

La aplicación la ejecuta un usuario con permisos limitados y el comando de bash necesitará permisos de sudo.

## Instalación

Creamos el usuario de sistema que va a ejecutar la aplicación.
```bash
adduser mi_usuario
```

Clonamos el proyecto en el equipo donde queremos que se ejecute y en la carpeta del usuario.

```bash
cd /home/mi_usuario
git clone https://github.com/rastreador/flask-exec-cmd.git
```

Hay que darle permisos de ejecución a la aplicación
```bash
chmod 755  /home/mi_usuario/flask-exec-cmd/app.py
```

Creamos el virtual enviroment y el directorio para los logs
```bash
virtualenv -p /usr/bin/python3 flask-exec-cmd
cd flask-exec-cmd
source bin/activate
mkdir logs
```

Instalamos Flask
```bash
pip install flask
```

Le damos permisos al usuario para ejecutar como root el comando que queremos ejecutar vía web editando el fichero /etc/sudoers como root y añadiendo al final:
```bash
mi_usuario ALL= NOPASSWD: /root/comando_a_ejecutar.sh
```

Se puede probar ejecutando desde mi_usuario:
```bash
sudo /root/comando_a_ejecutar.sh
```

Usaremos Supervisor para lanzar la aplicación
```bash
sudo apt-get install supervisor
```

Creamos el fichero de configuración para supervisor
```bash
sudo vim /etc/supervisor/conf.d/flask-exec-cmd.conf
```
```
[program:flask-exec-cmd]
environment=HOME="/home/mi_usuario/flask-exec-cmd",USER="mi_usuario"
user=mi_usuario
directory = /home/mi_usuario/flask-exec-cmd
#command = /home/mi_usuario/flask-exec-cmd/app.py
command = /home/mi_usuario/flask-exec-cmd/bin/python app.py
redirect_stderr = true
stdout_logfile = /home/mi_usuario/flask-exec-cmd/logs/out.log
stderr_logfile = /home/mi_usuario/flask-exec-cmd/logs/error.log
```
Activamos la configuración en supervisor

```bash
sudo supervisorctl update stats
sudo supervisorctl start stats
```

El programa se ejecutará en el puerto 5000, si tienes un firewall deberías de abrir ese puerto y acceder a través de la ip de tu servidor y el puerto 5000, por ejemplo:
http://1.2.3.4:5000

Si usas nginx puedes acceder a la aplicación con proxy_pass. Un ejemplo de configuración:
```
server {
    listen 80;
    server_name your_domain www.your_domain;

    location / {
        include proxy_params;
        proxy_pass http://127.0.0.1:5000;
    }
}
```

# myxterm
Detalles para la instalación con Docker Compose
Paso 1: Crear los archivos necesarios

1.	Dockerfile
Define el entorno para la aplicación.

2.	requirements.txt
Lista de dependencias de Python:

3.	docker-compose.yml
Configuración para orquestar los servicios:

Paso 2: Construcción e inicio de la aplicación

1.	Construir el contenedor:
docker-compose build

2.	Iniciar la aplicación:
docker-compose up -d

3.	Accede a la aplicación en http://localhost:5000.
Paso 3: Configuración adicional
•	Roles de usuario: Dentro de la aplicación, los administradores pueden registrar más usuarios con roles específicos utilizando el endpoint /register.
•	Queda pendiente Ampliar servicios: Puedes integrar otras bibliotecas como RDP (usando rdpy) y VNC (usando vncdotool) según los requisitos de conexión.

Hay una ruta /register que muestra una página donde los administradores pueden crear nuevos usuarios.
Asegúrate de agregar el archivo register.html en la carpeta de plantillas.

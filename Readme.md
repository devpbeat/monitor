# Panel de control - Las Ardenas S.A


# Instalación de ambiente de desarrollo

1. Clona este proyecto
2. Instala las dependencias.
    `cd frontend && npm install && cd ..`
3. Crea el archivo `.env` con las variables de entorno.
4. Levantar los servicios con el docker-compose.
    `docker-compose -f docker-compose.local.yml up --build -d`

# Creacion de super usuario para administracion mediante admin panel
1. Iniciar la consola ssh mediante el comando
`docker exec -it {nombre_del_contenedor} sh`
2. Crear el usuario mediante el comando `createsuperuser` del modulo manage de django
`python -m manage createsuperuser`
3. Iniciar sesion en 'http://localhost:8000/admin'
4. Administrar los modelos de forma correspondiente.

# Creacion de sources y updates
1. Configurar credenciales de los sources (AWS, Google Cloud, etc)
2. Crear sources de forma independiente (cthulhu1 status, cthulhu2 status, bastion1, bastion2, etc)
3. Luego de configurarlos, correr el proceso del updater para observar si este funciona de forma correcta.
Este proceso deberá actualizar todos los datos de las metricas existentes para cada source. (Observar proceso updater en app.views)

# Creacion de metricas y collections.
1. Crear artifactos y tipos de metricas.
2. Correr proceso de creacion de metricas (crea metricas para instancias EC2, agregar mas conforme vayan agregando nuevos tipos de datos. )
3. Ejecutar proceso de collector para guardar datos de los updates dentro de metric_data.

# Para mayor entendimiento de todo, visualzar el diagrama de entidad relacion y utilizar el collection de postman para ver los procesos existentes.
1. BASE_URL = 'http://localhost:8000/api'
2. Updater endpoint = '/updater'
3. Collector endpoint = '/collector'
4. Metrics creator endpoint = '/metrics_creator'
5. Get all metric data = '/metrics/all'


# Para datos de ejemplo en json, y ver el diagrama ER acceder al siguiente link

# Agradecimientos 

    A todos los desarrolladores de Las Ardenas S.A. 
    




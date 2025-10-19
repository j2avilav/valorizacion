# Versión Base de datos

- Activos TX DB: 2025-03-31 16:18 (Hora local Chile)

# Requisitos

- Python 3.13
- PostgreSQL 13.3
- Maria DB 10.6
- 16GB RAM

# Instalar en Windows

## Requisitos

- Windows 11
- Terminal Windows (recomendado)

## Instalación de Python 3.13

1. Descarga Python 3.13 desde la [página oficial de Python](https://www.python.org/downloads/)
2. Ejecuta el instalador y asegúrate de marcar la casilla "Add Python to PATH"
3. Selecciona "Install Now" para una instalación estándar o "Customize installation" para opciones avanzadas
4. Verifica la instalación abriendo Terminal Windows y ejecutando:
```
python --version
```
Deberás ver un mensaje indicando Python 3.13.x

## Instalación de PostgreSQL

1. Descarga PostgreSQL 13.3 desde la [página oficial](https://www.postgresql.org/download/windows/)
2. Ejecuta el instalador y sigue las instrucciones
3. Durante la instalación, anota la contraseña del usuario administrador (postgres)
4. Asegúrate de que el servicio de PostgreSQL esté corriendo

### Crear la base de datos y usuario PostgreSQL

Abre Terminal Windows como administrador y ejecuta:

```cmd
# Conectar a PostgreSQL como usuario postgres
psql -U postgres -h localhost

# Una vez dentro de psql, ejecuta los siguientes comandos:
CREATE USER valorizacion_user WITH PASSWORD 'valorizacion_password';
CREATE DATABASE valorizacion_db OWNER valorizacion_user;
GRANT ALL PRIVILEGES ON DATABASE valorizacion_db TO valorizacion_user;
\q
```

Alternativamente, puedes usar pgAdmin si lo instalaste durante el proceso de instalación de PostgreSQL.

## Instalación de MariaDB

1. Descarga MariaDB 10.6 desde la [página oficial](https://mariadb.org/download/)
2. Ejecuta el instalador y sigue las instrucciones
3. Durante la instalación, configura una contraseña para el usuario root
4. Asegúrate de que el servicio de MariaDB esté corriendo

### Crear la base de datos y usuario MariaDB

Abre Terminal Windows como administrador y ejecuta:

```cmd
# Conectar a MariaDB como usuario root
mysql -u root -p

# Una vez dentro de mysql, ejecuta los siguientes comandos:
CREATE USER 'valorizacion_user'@'localhost' IDENTIFIED BY 'valorizacion_password';
CREATE DATABASE valorizacion_db;
GRANT ALL PRIVILEGES ON valorizacion_db.* TO 'valorizacion_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

Alternativamente, puedes usar HeidiSQL o phpMyAdmin si los instalaste junto con MariaDB.

## Instalación del proyecto

1. Crea un entorno virtual y actívalo:
```
python -m venv venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
venv\Scripts\activate
```

2. Instala las dependencias:
```
pip install -e .
```

# Instalación en Linux

## Requisitos

- Ubuntu 22.04 LTS o superior
- Terminal

## Instalación de Python 3.13

1. Actualiza el sistema e instala las dependencias necesarias:
```
sudo apt update
sudo apt upgrade -y
sudo apt install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev
```

2. Descarga e instala Python 3.13:
```
wget https://www.python.org/ftp/python/3.13.0/Python-3.13.0.tgz
tar -xf Python-3.13.0.tgz
cd Python-3.13.0
./configure --enable-optimizations
make -j $(nproc)
sudo make altinstall
```

3. Verifica la instalación:
```
python3.13 --version
```
Deberás ver un mensaje indicando Python 3.13.x

## Instalación de PostgreSQL

```
sudo apt update
sudo apt install -y postgresql-13
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

Configura el usuario para PostgreSQL:
```
sudo passwd postgres
sudo -u postgres psql -c "CREATE USER valorizacion_user WITH PASSWORD 'valorizacion_password';"
sudo -u postgres psql -c "CREATE DATABASE valorizacion_db OWNER valorizacion_user;"
```

## Instalación de MariaDB

```
sudo apt update
sudo apt install -y mariadb-server
sudo systemctl start mariadb
sudo systemctl enable mariadb
```

Configura el usuario para MariaDB:
```
sudo mysql -e "CREATE USER 'valorizacion_user'@'localhost' IDENTIFIED BY 'valorizacion_password';"
sudo mysql -e "CREATE DATABASE valorizacion_db;"
sudo mysql -e "GRANT ALL PRIVILEGES ON valorizacion_db.* TO 'valorizacion_user'@'localhost';"
sudo mysql -e "FLUSH PRIVILEGES;"
```

## Instalación del proyecto

1. Crea un entorno virtual y actívalo:
```
python3.13 -m venv venv
source venv/bin/activate
```

2. Instala las dependencias:
```
pip install -e .
```

# Instalación en OSX

## Requisitos

- Homebrew (https://brew.sh/)


## Instalación de dependencias

```
brew install libpq python@3.13
```

# Documentación adicional

Para información específica sobre módulos especializados, consulta:

- [Antecedentes Complementarios](docs/antecedentes_complementarios.md) - Información sobre descarga y procesamiento de archivos complementarios, incluyendo soporte para RAR

# Configuración

La plataforma utiliza variables de entorno para configurar el acceso a las bases de datos y otros servicios.

## Archivo de configuración `.env`

Crea un archivo `.env` en la raíz del proyecto para configurar los parámetros de conexión. Puedes usar como referencia el archivo `.env.example. A continuación se detallan los parámetros disponibles:

### Configuración de MariaDB
```
# MariaDB Configuration
MARIADB_HOST=127.0.0.1
MARIADB_PORT=3306
MARIADB_DB=valorizacion_db
MARIADB_USER=valorizacion_user
MARIADB_PASSWORD=valorizacion_password
```

Si necesitas ajustar la ruta del cliente MariaDB, puedes configurar:
```
MARIADB_DUMP_PATH=mysqldump
```

### Configuración de PostgreSQL
```
# PostgreSQL Configuration
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
POSTGRES_DB=valorizacion_db
POSTGRES_USER=valorizacion_user
POSTGRES_PASSWORD=valorizacion_password
```

Si necesitas ajustar la ruta del cliente PostgreSQL (psql), puedes configurar:
```
POSTGRES_CLIENT_PATH=/ruta/a/psql
```

# Ejecución del programa

## 1. Calificación

Para ejecutar el proceso de calificación se requieren dos terminales:

### Terminal 1: Inicia el servidor de Prefect

```
prefect server start
```


### Terminal 2: Ejecuta el proceso de calificación

```
python -m scripts.setup
python -m scripts.workflow
```

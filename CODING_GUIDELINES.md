# Guía de Estilo para el Código

## Base de Datos

- Las tablas creadas por este programa que no existían en el coordinador deben cumplir las siguientes reglas:
  - Los nombres de las tablas deben:
    - Contener el prefijo `_`.
    - Estar en **singular**.
    - Utilizar el formato **snake_case**.
  - Los nombres de los campos deben utilizar el formato **snake_case**.
  - Evitar el prefijo `nombre_` en los campos. `nombre_campo` pasa a ser `campo`
- Creación de tablas debe estar centralizada en el archivo scripts/load/create_mariadb_schema.py

## Scripts

- Cada script debe poder ejecutarse de manera independiente para facilitar las pruebas durante el desarrollo.
- Todas las invocaciones a un script deben ser **idempotentes**.
  - Utilizar `TRUNCATE TABLE` antes de reescribir datos en una tabla


## Reportes

- Cada reporte debe estar referenciado en `script/reports/run_all.py` para permitir su ejecución automática al realizar un **push a mainline**.
- Los reportes deben generar su salida en la carpeta `output`.
- Se debe utilizar la función `get_output_folder()` para definir la ruta de salida.

# Tests

- Los tests deben solo hacer uso de MariaDB y no deben depender de PostgreSQL.

# Script de Copia de Seguridad a S3 Bucket de AWS

Este script automatiza la copia de seguridad de los directorios especificados y sube los archivos de copia de seguridad a un bucket de AWS S3. El script utiliza un único archivo de configuración (`config.json`) para todos los detalles de configuración necesarios, lo que lo hace más fácil y práctico para el usuario.

## Prerrequisitos

1. **Python 3.x** instalado en tu sistema.
2. **AWS CLI** instalado y configurado con tus credenciales de AWS.
3. **Paquetes de Python Requeridos**: Instala los paquetes requeridos usando pip:

   ```bash
   pip install boto3 jsonschema
   ```

## Configuración

### `config.json`

Crea un archivo `config.json` en el mismo directorio que tu script con la siguiente estructura:

```json
{
  "directories": [
    "/path/to/directory1",
    "/path/to/directory2"
  ],
  "aws": {
    "access_key_id": "your-access-key-id",
    "secret_access_key": "your-secret-access-key",
    "bucket_name": "your-s3-bucket-name"
  },
  "backup_output_dir": "/path/to/directory"
}
```

### Explicación:

- **directories**: Una lista de rutas de directorios que deseas respaldar.
- **aws**:
  - `access_key_id`: Tu ID de Clave de Acceso de AWS para la autenticación.
  - `secret_access_key`: Tu Clave de Acceso Secreta de AWS.
  - `bucket_name`: El nombre del bucket de S3 donde se subirán los archivos de copia de seguridad.
- **backup_output_dir**: El directorio donde se almacenarán temporalmente los archivos de copia de seguridad antes de subirlos a S3.

## Ejecutando el Script

1. **Crear `config.json`**:
   Crea un archivo `config.json` en el mismo directorio que tu script con los detalles de configuración apropiados.

2. **Ejecutar el Script**:
   Ejecuta el script para respaldar tus archivos en tu bucket de S3:

   ```bash
   python backup_script.py
   ```

## Descripción del Script

### `backup_script.py`

El script realiza los siguientes pasos:

1. **Registro**: Configura el registro en un archivo llamado `backup.log`.
2. **Carga de Configuración**: Carga la configuración desde `config.json`.
3. **Creación de Copia de Seguridad**: Crea una copia de seguridad de los directorios especificados y la guarda en `backup_output_dir`.
4. **Subida a S3**: Sube el archivo de copia de seguridad al bucket de S3 especificado.

### Funciones

- **setup_logging()**: Configura el registro.
- **create_backup(backup_dirs, output_dir)**: Crea una copia de seguridad de los directorios especificados.
- **upload_to_s3(file_path, aws_config)**: Sube el archivo de copia de seguridad a AWS S3.
- **validate_config(config)**: Valida la configuración usando el esquema JSON.
- **load_config()**: Carga la configuración desde `config.json`.
- **main()**: Función principal que orquesta el proceso de copia de seguridad.

## Verificación

1. **Revisar el Archivo de Registro**:
   - El script registra las actividades en un archivo llamado `backup.log`. Puedes revisar este archivo de registro para ver el estado del proceso de copia de seguridad.
   - Abre una terminal y ejecuta:
     ```bash
     cat backup.log
     ```

2. **Verificar Archivos de Copia de Seguridad**:
   - Después de que el script se ejecute, revisa el `backup_output_dir` (por ejemplo, `/home/elliot/backups`) para asegurarte de que se han creado los archivos de copia de seguridad.
   - Deberías ver archivos `.zip` nombrados con la fecha y hora actuales.

3. **Revisar el Bucket de S3**:
   - Verifica que los archivos de copia de seguridad se han subido a tu bucket de S3.
   - Puedes hacerlo a través de la Consola de Administración de AWS o usando la CLI de AWS:
     ```bash
     aws s3 ls s3://your-s3-bucket-name/
     ```

## Descripción General

1. **Archivo de Configuración**: Usa `config.json` para todos los datos de configuración, incluyendo los directorios a respaldar, las credenciales de AWS y el directorio de salida de la copia de seguridad.
2. **Cargar Configuración**: Carga la configuración desde `config.json` en la función `load_config`.
3. **Ejecutar el Script**: Ejecuta el script para respaldar tus archivos en tu bucket de S3.
4. **Verificación**: Revisa el archivo de registro, verifica los archivos de copia de seguridad y revisa el bucket de S3 para asegurarte de que el proceso de copia de seguridad esté funcionando correctamente.

Siguiendo estos pasos, puedes crear un sistema de copia de seguridad automatizado seguro y flexible que se adapte a tus necesidades.

Las contribuciones son bienvenidas.

---

# Automated Backup Script

This script automates the backup of specified directories and uploads the backup files to an AWS S3 bucket. The script uses a single configuration file (`config.json`) for all necessary configuration details, making it easier and more practical for the user.

## Prerequisites

1. **Python 3.x** installed on your system.
2. **AWS CLI** installed and configured with your AWS credentials.
3. **Required Python Packages**: Install the required packages using pip:

   ```bash
   pip install boto3 jsonschema
   ```

## Configuration

### `config.json`

Create a `config.json` file in the same directory as your script with the following structure:

```json
{
  "directories": [
    "/path/to/directory1",
    "/path/to/directory2"
  ],
  "aws": {
    "access_key_id": "your-access-key-id",
    "secret_access_key": "your-secret-access-key",
    "bucket_name": "your-s3-bucket-name"
  }
},
  "backup_output_dir": "/path/to/directory"
}
```

### Explanation:

- **directories**: A list of directory paths that you want to back up.
- **aws**:
  - `access_key_id`: Your AWS Access Key ID for authentication.
  - `secret_access_key`: Your AWS Secret Access Key.
  - `bucket_name`: The name of the S3 bucket where the backup files will be uploaded.
- **backup_output_dir**: The directory where the backup files will be temporarily stored before uploading to S3.

## Running the Script

1. **Create `config.json`**:
   Create a `config.json` file in the same directory as your script with the appropriate configuration details.

2. **Run the Script**:
   Execute the script to back up your files to your S3 bucket:

   ```bash
   python backup_script.py
   ```

## Script Overview

### `backup_script.py`

The script performs the following steps:

1. **Logging**: Sets up logging to a file named `backup.log`.
2. **Configuration Loading**: Loads configuration from `config.json`.
3. **Backup Creation**: Creates a backup of specified directories and saves it to the `backup_output_dir`.
4. **S3 Upload**: Uploads the backup file to the specified S3 bucket.

### Functions

- **setup_logging()**: Sets up logging.
- **create_backup(backup_dirs, output_dir)**: Creates a backup of specified directories.
- **upload_to_s3(file_path, aws_config)**: Uploads the backup file to AWS S3.
- **validate_config(config)**: Validates the configuration using JSON schema.
- **load_config()**: Loads configuration from `config.json`.
- **main()**: Main function that orchestrates the backup process.

## Verification

1. **Check the Log File**:
   - The script logs activities to a file named `backup.log`. You can check this log file to see the status of the backup process.
   - Open a terminal and run:
     ```bash
     cat backup.log
     ```

2. **Verify Backup Files**:
   - After the script runs, check the `backup_output_dir` (e.g., `/home/elliot/backups`) to ensure that the backup files have been created.
   - You should see `.zip` files named with the current date and time.

3. **Check S3 Bucket**:
   - Verify that the backup files have been uploaded to your S3 bucket.
   - You can do this via the AWS Management Console or using the AWS CLI:
     ```bash
     aws s3 ls s3://your-s3-bucket-name/
     ```

## Overview

1. **Configuration File**: Use `config.json` for all configuration data, including directories to back up, AWS credentials, and the backup output directory.
2. **Load Configuration**: Load configuration from `config.json` in the `load_config` function.
3. **Run the Script**: Execute the script to back up your files to your S3 bucket.
4. **Verification**: Check the log file, verify backup files, and check the S3 bucket to ensure the backup process is working correctly.

By following these steps, you can create a secure and flexible automated backup system that meets your needs.

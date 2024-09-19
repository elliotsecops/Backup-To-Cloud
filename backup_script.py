import os
import shutil
import zipfile
import boto3
from datetime import datetime
import logging
import jsonschema
import json

# Function to set up logging
def setup_logging():
    logging.basicConfig(filename='backup.log', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

# Function to create a backup of specified directories
def create_backup(backup_dirs, output_dir):
    try:
        backup_filename = os.path.join(output_dir, f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip")
        with zipfile.ZipFile(backup_filename, 'w') as zipf:
            for directory in backup_dirs:
                for root, dirs, files in os.walk(directory):
                    for file in files:
                        zipf.write(os.path.join(root, file),
                                   os.path.relpath(os.path.join(root, file),
                                                   os.path.join(directory, '..')))
        logging.info(f"Backup created: {backup_filename}")
        print(f"Backup created: {backup_filename}")
        return backup_filename
    except Exception as e:
        logging.error(f"Error creating backup: {e}")
        print(f"Error creating backup: {e}")
        return None

# Function to upload the backup file to AWS S3
def upload_to_s3(file_path, aws_config):
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_config['access_key_id'],
            aws_secret_access_key=aws_config['secret_access_key']
        )
        bucket_name = aws_config['bucket_name']
        file_name = os.path.basename(file_path)
        s3_client.upload_file(file_path, bucket_name, file_name)
        logging.info(f"Backup uploaded to S3: {file_name}")
        print(f"Backup uploaded to S3: {file_name}")
    except Exception as e:
        logging.error(f"Error uploading {file_name} to S3: {e}")
        print(f"Error uploading {file_name} to S3: {e}")

# Function to validate the configuration
def validate_config(config):
    schema = {
        "type": "object",
        "properties": {
            "directories": {"type": "array", "items": {"type": "string"}},
            "aws": {
                "type": "object",
                "properties": {
                    "access_key_id": {"type": "string"},
                    "secret_access_key": {"type": "string"},
                    "bucket_name": {"type": "string"}
                },
                "required": ["access_key_id", "secret_access_key", "bucket_name"]
            },
            "backup_output_dir": {"type": "string"}
        },
        "required": ["directories", "aws", "backup_output_dir"]
    }
    jsonschema.validate(config, schema)

# Function to load configuration from config.json
def load_config():
    try:
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
        return config
    except FileNotFoundError:
        logging.error("config.json file not found.")
        print("config.json file not found.")
        return None
    except json.JSONDecodeError:
        logging.error("Error decoding config.json.")
        print("Error decoding config.json.")
        return None

# Main function
def main():
    setup_logging()
    config = load_config()
    if not config:
        return
    try:
        validate_config(config)
    except jsonschema.exceptions.ValidationError as e:
        logging.error(f"Invalid configuration: {e}")
        print(f"Invalid configuration: {e}")
        return
    
    backup_dirs = config['directories']
    aws_config = config['aws']
    backup_output_dir = config['backup_output_dir']

    backup_file = create_backup(backup_dirs, backup_output_dir)
    if backup_file:
        upload_to_s3(backup_file, aws_config)
    else:
        logging.error("Backup creation failed, aborting S3 upload.")
        print("Backup creation failed.")

if __name__ == "__main__":
    main()
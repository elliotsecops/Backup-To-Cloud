import os
import shutil
import tarfile
import boto3
from datetime import datetime
import logging
import jsonschema
import json
from pathlib import Path
import sys
import tempfile
from botocore.exceptions import ClientError

# Function to set up logging
def setup_logging():
    logging.basicConfig(filename='backup.log', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

# Function to create a backup of specified directories
def create_backup(backup_dirs: list[str], output_dir: str) -> Path | None:
    """
    Creates a backup of specified directories and returns the path to the backup file.

    :param backup_dirs: List of directories to backup.
    :param output_dir: Directory where the backup file will be saved.
    :return: Path to the backup file or None if backup creation fails.
    """
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_backup_path = Path(tmpdir) / f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.tar.gz"
            with tarfile.open(temp_backup_path, "w:gz") as tar:
                for directory in backup_dirs:
                    if not os.path.exists(directory):
                        logging.warning(f"Directory {directory} does not exist. Skipping.")
                        continue
                    tar.add(directory, arcname=os.path.basename(directory))  # Use basename for the root arcname

            backup_filename = Path(output_dir) / temp_backup_path.name  # Final path in output_dir
            shutil.move(str(temp_backup_path), str(backup_filename))  # Move from temp to final location
            logging.info(f"Backup created: {backup_filename}")
            return backup_filename

    except Exception as e:
        logging.exception(f"Error creating backup: {e}")
        return None

# Function to upload the backup file to AWS S3
def upload_to_s3(file_path: Path, aws_config: dict) -> None:
    """
    Uploads the backup file to an AWS S3 bucket.

    :param file_path: Path to the backup file.
    :param aws_config: Dictionary containing AWS credentials and bucket name.
    """
    try:
        s3 = boto3.client(
            's3',
            aws_access_key_id=aws_config['access_key_id'],
            aws_secret_access_key=aws_config['secret_access_key']
        )
        bucket_name = aws_config['bucket_name']
        file_name = file_path.name
        s3.upload_file(str(file_path), bucket_name, file_name)
        logging.info(f"Backup uploaded to S3: {file_name}")
    except ClientError as e:  # Catch botocore.exceptions.ClientError
        logging.exception(f"Error uploading {file_name} to S3: {e}")
        if e.response['Error']['Code'] == 'NoSuchBucket':
            logging.error(f"Bucket {bucket_name} not found.")
        # Add other specific error handling as needed
    except Exception as e:  # Catch other unexpected errors
        logging.exception(f"An unexpected error occurred during S3 upload: {e}")

# Function to validate the configuration
def validate_config(config: dict):
    """
    Validates the configuration against a JSON schema.

    :param config: Dictionary containing the configuration.
    """
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
def load_config() -> dict | None:
    """
    Loads the configuration from config.json and environment variables.

    :return: Dictionary containing the configuration or None if loading fails.
    """
    try:
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)

        # Override with environment variables if available
        config['aws']['access_key_id'] = os.environ.get('AWS_ACCESS_KEY_ID', config['aws']['access_key_id'])
        config['aws']['secret_access_key'] = os.environ.get('AWS_SECRET_ACCESS_KEY', config['aws']['secret_access_key'])
        config['aws']['bucket_name'] = os.environ.get('AWS_BUCKET_NAME', config['aws']['bucket_name'])

        # Ensure all required AWS credentials are present
        if not all([config['aws']['access_key_id'], config['aws']['secret_access_key'], config['aws']['bucket_name']]):
            logging.error("Missing AWS credentials. Please set AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_BUCKET_NAME environment variables.")
            return None

        # Ensure backup output directory exists
        backup_output_dir = Path(config['backup_output_dir'])
        if not backup_output_dir.is_dir():
            backup_output_dir.mkdir(parents=True, exist_ok=True)
        config['backup_output_dir'] = str(backup_output_dir)  # Convert back to string if needed elsewhere

        return config
    except FileNotFoundError:
        logging.error("config.json file not found.")
        return None
    except json.JSONDecodeError:
        logging.error("Error decoding config.json.")
        return None

# Main function
def main():
    setup_logging()
    config = load_config()
    if not config:
        sys.exit(1)
    try:
        validate_config(config)
    except jsonschema.exceptions.ValidationError as e:
        logging.error(f"Invalid configuration: {e}")
        sys.exit(1)
    
    backup_dirs = config['directories']
    aws_config = config['aws']
    backup_output_dir = config['backup_output_dir']

    backup_file = create_backup(backup_dirs, backup_output_dir)
    if backup_file:
        upload_to_s3(backup_file, aws_config)
    else:
        logging.error("Backup creation failed, aborting S3 upload.")

if __name__ == "__main__":
    main()

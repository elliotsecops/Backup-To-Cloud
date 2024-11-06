# Automated Backup Script to S3 AWS Bucket

This script automates the backup of specified directories and uploads the backup files to an AWS S3 bucket. The script uses a single configuration file (`config.json`) for all necessary configuration details, making it easier and more practical for the user.

## Prerequisites

1. **Python 3.x** installed on your system.
2. **AWS CLI** installed and configured with your AWS credentials.
3. **Required Python Packages**: Install the required packages using pip:
   ```bash
   pip install boto3 jsonschema
   ```
4. **Standard Python Libraries**: Ensure the following standard libraries are available:
   - `os`
   - `shutil`
   - `tarfile`
   - `logging`
   - `jsonschema`
   - `json`
   - `pathlib`
   - `sys`
   - `tempfile`
   - `botocore.exceptions`

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
    "bucket_name": "your-s3-bucket-name"
  },
  "backup_output_dir": "/path/to/backup/output/dir"
}
```

### Explanation:

- **directories**: A list of directory paths that you want to back up. Replace `"/path/to/directory1"` and `"/path/to/directory2"` with the actual paths to the directories you want to back up.
- **aws**:
  - `bucket_name`: The name of the S3 bucket where the backup files will be uploaded. Replace `"your-s3-bucket-name"` with your actual S3 bucket name.
- **backup_output_dir**: The directory where the backup files will be temporarily stored before uploading to S3. Replace `"/path/to/backup/output/dir"` with the actual path to the directory where you want to store the backup files.

### Example:

Here’s an example of how the `config.json` file might look:

```json
{
  "directories": [
    "/home/user/documents",
    "/home/user/photos"
  ],
  "aws": {
    "bucket_name": "secure-backup-bucket"
  },
  "backup_output_dir": "/home/user/backups"
}
```

Make sure to replace the placeholders with your actual values before running the script.

### AWS Credentials

**Security Note:** Storing AWS credentials directly in configuration files is a significant security risk. Instead, use environment variables to provide your AWS credentials. The script will automatically retrieve these credentials from the environment.

Set the following environment variables in your shell or environment configuration file (e.g., `.bashrc`, `.zshrc`, or system environment variables):

- `AWS_ACCESS_KEY_ID`: Your AWS access key ID.
- `AWS_SECRET_ACCESS_KEY`: Your AWS secret access key.
- `AWS_BUCKET_NAME`: Your AWS S3 bucket name (optional, overrides the setting in `config.json` if present).

Example:

```bash
export AWS_ACCESS_KEY_ID="your-access-key-id"
export AWS_SECRET_ACCESS_KEY="your-secret-access-key"
export AWS_BUCKET_NAME="your-s3-bucket-name"
```

## Quick Start

1. **Install Dependencies:**
   ```bash
   pip install boto3 jsonschema
   ```
2. **Configure `config.json`:**
   Specify the directories to back up and the backup output directory. Set the `bucket_name` in `config.json` or as an environment variable. (See the Configuration section for details).
3. **Set Environment Variables:**
   Set `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and optionally `AWS_BUCKET_NAME`.
4. **Run the Script:**
   ```bash
   python backup_script.py
   ```
5. **Verify:**
   Check the `backup.log` file and your S3 bucket to ensure the backup was successful.

## Script Overview

### `backup_script.py`

The script performs the following steps:

1. **Logging**: Sets up logging to a file named `backup.log`.
2. **Configuration Loading**: Loads configuration from `config.json`.
3. **Backup Creation**: Creates a backup of specified directories and saves it to the `backup_output_dir`.
4. **S3 Upload**: Uploads the backup file to the specified S3 bucket.

### Functions

For detailed information about the functions, please refer to the docstrings in the `backup_script.py` file.

## Verification

1. **Check the Log File**:
   - The script logs activities to a file named `backup.log`. You can check this log file to see the status of the backup process.
   - Open a terminal and run:
     ```bash
     cat backup.log
     ```

2. **Verify Backup Files**:
   - After the script runs, check the `backup_output_dir` (e.g., `/home/user/backups`) to ensure that the backup files have been created.
   - You should see `.tar.gz` files named with the current date and time.

3. **Check S3 Bucket**:
   - Verify that the backup files have been uploaded to your S3 bucket.
   - You can do this via the AWS Management Console or using the AWS CLI:
     ```bash
     aws s3 ls s3://your-s3-bucket-name/
     ```

## Key points

1. **Configuration File**: Use `config.json` for all configuration data, including directories to back up, AWS bucket name, and the backup output directory.
2. **AWS Credentials**: Use environment variables for AWS credentials (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_BUCKET_NAME`).
3. **Run the Script**: Execute the script to back up your files to your S3 bucket.
4. **Verification**: Check the log file, verify backup files, and check the S3 bucket to ensure the backup process is working correctly.

By following these steps, you can create a secure and flexible automated backup system that meets your needs.

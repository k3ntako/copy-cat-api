import os
import json

from cryptography.fernet import Fernet

from src.utilities.file_io import write_to_file, read_file

def generate_key():
  return Fernet.generate_key()

def encrypt_secrets(secrets_path, key, str):
  encryptedStr = encrypt_str(key, str)
  write_to_file(secrets_path, encryptedStr)

def decrypt_str(key, str):
  fernet = Fernet(key)
  return fernet.decrypt(str.encode()).decode()

def encrypt_str(key, str):
  fernet = Fernet(key)
  return fernet.encrypt(str.encode()).decode()

def decrypt_secrets(secrets_path, key):
  content = read_file(secrets_path)
  return decrypt_str(key, content)

def generate_secrets_file():
  key = os.getenv('SECRETS_KEY', generate_key())

  secrets_json = {
    'RDS_USERNAME': os.getenv('TF_VAR_RDS_USERNAME'),
    'RDS_PASSWORD': os.getenv('TF_VAR_RDS_PASSWORD'),
    'RDS_HOSTNAME': os.getenv('RDS_HOSTNAME'),
    'RDS_PORT': os.getenv('TF_VAR_RDS_PORT'),
    'RDS_DB_NAME': os.getenv('TF_VAR_RDS_DB_NAME'),
  }
  encrypt_secrets("./encrypted-secrets-prod", key, json.dumps(secrets_json))

  print(f"key: {key}")
  print(decrypt_secrets("./encrypted-secrets-prod", key))

if __name__ == "__main__":
  generate_secrets_file()
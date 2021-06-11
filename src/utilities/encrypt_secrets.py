import sys

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

def generate_secrets_file_from_json_file():
  try:
    env = sys.argv[1]
  except:
    sys.exit("Environment (prod, dev, or testing) must be passed in")

  try:
    secrets = read_file(f"./decrypted-secrets-{env}.json")
  except FileNotFoundError:
    sys.exit("File not found. Make sure it's relative to where you are calling the function.")
  
  try:
    key = sys.argv[2]
  except:
    key = generate_key().decode()

  encrypt_secrets(f"./encrypted-secrets-{env}", key, secrets)

  print(f"key: {key}")
  print(decrypt_secrets("./encrypted-secrets-prod", key))
  print("!!! IMPORTANT: do not commit the original JSON file !!!")

if __name__ == "__main__":
  generate_secrets_file_from_json_file()
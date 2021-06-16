import argparse, sys

from cryptography.fernet import Fernet

from src.utilities.file_io import FileIO
from src.utilities.console_io import ConsoleIO

def generate_key():
  return Fernet.generate_key()

def encrypt_secrets(fileIO, secrets_path, key, str):
  fernet = Fernet(key)
  encryptedStr =  fernet.encrypt(str.encode()).decode()
  
  fileIO.write_to_file(secrets_path, encryptedStr)

def decrypt_secrets(fileIO, secrets_path, key):
  content = fileIO.read_file(secrets_path)

  fernet = Fernet(key)
  return fernet.decrypt(content.encode()).decode()


def generate_secrets_file_from_json_file(consoleIO, fileIO, env, key):
    try:
      secrets = fileIO.read_file(f"./decrypted-secrets-{env}.json")
    except FileNotFoundError:
      sys.exit("File not found. Make sure it's relative to where you are calling the function.")
    
    encrypt_secrets(fileIO, f"./encrypted-secrets-{env}", key, secrets)

    consoleIO.print(f'key: {key}')
    consoleIO.print(decrypt_secrets(fileIO, f"./encrypted-secrets-{env}", key))
    consoleIO.print("!!! IMPORTANT: do not commit the original JSON file !!!")

if __name__ == "__main__":
    fileIO = FileIO()
    consoleIO = ConsoleIO()

    parser = argparse.ArgumentParser(description='Encrypt secrets for repo')
    parser.add_argument('--env', dest='env', type=str, help='prod, testing, or dev')
    parser.add_argument('--key', dest='key', type=str, default=generate_key().decode(),
                        help='Key saved in 1Password. Will generate new one if blank')

    args = parser.parse_args()

    generate_secrets_file_from_json_file(consoleIO, fileIO, args.env, args.key)

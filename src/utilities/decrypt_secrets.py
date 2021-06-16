import argparse

from src.utilities.encrypt_secrets import decrypt_secrets
from src.utilities.file_io import FileIO

def decrypt_to_json_file(fileIO, env, key):
    secrets = decrypt_secrets(fileIO, f"./encrypted-secrets-{env}", key)
    fileIO.write_to_file(f"./decrypted-secrets-{env}.json", secrets)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Decrypt secrets for repo')
    parser.add_argument('--env', dest='env', type=str, help='prod, testing, or dev')
    parser.add_argument('--key', dest='key', type=str, help='Key saved in 1Password')

    args = parser.parse_args()

    fileIO = FileIO()

    decrypt_to_json_file(fileIO, args.env, args.key)
    
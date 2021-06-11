import sys

from src.utilities.encrypt_secrets import generate_key, decrypt_secrets
from src.utilities.file_io import write_to_file

if __name__ == "__main__":
  try:
    env = sys.argv[1]
  except:
    sys.exit("Environment (prod, dev, or testing) must be passed in")

  try:
    key = sys.argv[2]
  except:
    key = generate_key()

  secrets = decrypt_secrets(f"./encrypted-secrets-{env}", key)
  write_to_file(f"./decrypted-secrets-{env}.json", secrets)

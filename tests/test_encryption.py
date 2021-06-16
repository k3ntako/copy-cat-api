from tests.mocks.MockConsoleIO import MockConsoleIO
from tests.mocks.MockFileIO import MockFileIO
from cryptography.fernet import Fernet
from src.utilities.encrypt_secrets import generate_secrets_file_from_json_file

MOCK_SECRETS_JSON_STR = """{{
    "DATABASE_USER": "user",
    "DATABASE_PASSWORD": "password",
}}"""

MOCK_KEY = 'DBCMnOOMrhmEzu7fUcEp7frxdpgKPuc5USNDRiNyGac='

MOCK_ENCRYPTED_STR = 'gAAAAABgyn0YWitQ-Mb9nq5LcZkLWl4wJOnmQ3AhGgwi8e7nyKyycUuuaR1hA_Azcwo7alRJ5kn5f66YD6kG8--gSK_qkJ0MD2-5ClFyy1seB3XwdYHb2cE5rps8NniUi-JDXJlyG6YOOs4bp-3OuE0BnM-jJ-10Ddi40oGiCrGwJPMocoVkD3M='

def test_writes_encrypted_text():
    """Should read JSON and write encrypted text to file"""
    mock_console_io = MockConsoleIO()
    mock_file_io = MockFileIO([MOCK_SECRETS_JSON_STR, MOCK_ENCRYPTED_STR])
    generate_secrets_file_from_json_file(mock_console_io, mock_file_io, 'dev', MOCK_KEY)

    assert mock_file_io.read_file_path[0] == './decrypted-secrets-dev.json'

    # Encrypted string will change even given the same key and string,
    # so have to test the decrypted version.
    fernet = Fernet(MOCK_KEY)
    encoded_encrypted_text = mock_file_io.write_to_file_str[0].encode()
    expected_decrypted_text = fernet.decrypt(encoded_encrypted_text).decode()

    assert expected_decrypted_text == MOCK_SECRETS_JSON_STR
    assert mock_file_io.write_to_file_path[0] == './encrypted-secrets-dev'

def test_encrypt_prints():
    """Should print key, decrypted text, and warning after encryption"""
    mock_console_io = MockConsoleIO()
    mock_file_io = MockFileIO([MOCK_SECRETS_JSON_STR, MOCK_ENCRYPTED_STR])
    generate_secrets_file_from_json_file(mock_console_io, mock_file_io, 'dev', MOCK_KEY)

    assert mock_console_io.print_arg[0] == f'key: {MOCK_KEY}'
    assert mock_console_io.print_arg[1] == MOCK_SECRETS_JSON_STR
    assert mock_console_io.print_arg[2] == '!!! IMPORTANT: do not commit the original JSON file !!!'
    
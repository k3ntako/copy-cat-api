from tests.mocks.MockFileIO import MockFileIO
from src.utilities.decrypt_secrets import decrypt_to_json_file

MOCK_SECRETS_JSON_STR = """{{
    "DATABASE_USER": "user",
    "DATABASE_PASSWORD": "password",
}}"""

MOCK_KEY = 'DBCMnOOMrhmEzu7fUcEp7frxdpgKPuc5USNDRiNyGac='

MOCK_ENCRYPTED_STR = 'gAAAAABgyn0YWitQ-Mb9nq5LcZkLWl4wJOnmQ3AhGgwi8e7nyKyycUuuaR1hA_Azcwo7alRJ5kn5f66YD6kG8--gSK_qkJ0MD2-5ClFyy1seB3XwdYHb2cE5rps8NniUi-JDXJlyG6YOOs4bp-3OuE0BnM-jJ-10Ddi40oGiCrGwJPMocoVkD3M='

def test_decrypts_encrypted_file():
    """Should read JSON and write encrypted text to file"""
    mock_file_io = MockFileIO([MOCK_ENCRYPTED_STR])
    decrypt_to_json_file(mock_file_io, 'prod', MOCK_KEY)

    assert mock_file_io.read_file_path[0] == './encrypted-secrets-prod'
    assert mock_file_io.write_to_file_path[0] == './decrypted-secrets-prod.json'
    assert mock_file_io.write_to_file_str[0] == MOCK_SECRETS_JSON_STR

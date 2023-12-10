import os
import tempfile
import pytest
from modules.RSA import RSA


@pytest.fixture
def rsa_instance():
    return RSA()


@pytest.fixture
def temp_files():
    input_file = tempfile.NamedTemporaryFile(delete=False).name
    output_file = tempfile.NamedTemporaryFile(delete=False).name

    yield input_file, output_file

    os.remove(input_file)
    os.remove(output_file)


def test_generate_key_pair(rsa_instance):
    rsa_instance.generate_key_pair()
    assert os.path.exists(rsa_instance.private_key_path)
    assert os.path.exists(rsa_instance.public_key_path)


def test_encrypt_decrypt_message(rsa_instance):
    rsa_instance.generate_key_pair()

    original_message = "Hello, World!"
    ciphertext = rsa_instance.encrypt_message(original_message, rsa_instance.public_key_path)
    decrypted_message = rsa_instance.decrypt_message(ciphertext, rsa_instance.private_key_path)

    assert decrypted_message == original_message


def test_encrypt_decrypt_file(rsa_instance, temp_files):
    input_file, output_file = temp_files
    rsa_instance.generate_key_pair()

    test_data = b'This is a test data.'

    with open(input_file, 'wb') as f:
        f.write(test_data)

    rsa_instance.encrypt_file(input_file, output_file, rsa_instance.public_key_path)

    rsa_instance.decrypt_file(output_file, input_file, rsa_instance.private_key_path)

    with open(input_file, 'rb') as f:
        decrypted_data = f.read()

    assert decrypted_data == test_data

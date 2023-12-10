import os
import tempfile
import pytest
from modules.DSS import DSS


@pytest.fixture
def dss_instance():
    return DSS()


@pytest.fixture
def temp_files():
    input_file = tempfile.NamedTemporaryFile(delete=False).name
    output_file = tempfile.NamedTemporaryFile(delete=False).name
    signature_file = tempfile.NamedTemporaryFile(delete=False).name

    yield input_file, output_file, signature_file

    os.remove(input_file)
    os.remove(output_file)
    os.remove(signature_file)


def test_generate_key(dss_instance):
    dss_instance.generate_key()
    assert os.path.exists(dss_instance.private_key_path)
    assert os.path.exists(dss_instance.public_key_path)


def test_sign_verify_message(dss_instance):
    dss_instance.generate_key()

    original_message = "Hello, World!"
    private_key = dss_instance.load_private_key()
    public_key = dss_instance.load_public_key()

    signature = dss_instance.sign_message(original_message, private_key)
    assert dss_instance.verify_signature(original_message, signature, public_key)


def test_sign_verify_file(dss_instance, temp_files):
    input_file, output_file, signature_file = temp_files
    dss_instance.generate_key()

    # Generate some test data
    test_data = b'This is a test data.'

    # Write the test data to the input file
    with open(input_file, 'wb') as f:
        f.write(test_data)

    # Sign the test data
    private_key = dss_instance.load_private_key()
    dss_instance.sign_file(input_file, private_key, signature_file)

    # Verify the signature
    public_key = dss_instance.load_public_key()
    assert dss_instance.verify_file(input_file, public_key, signature_file)

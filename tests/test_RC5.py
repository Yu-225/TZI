import os
import tempfile

import pytest
from math import ceil

from modules.RC5 import RC5


@pytest.fixture
def rc5_instance():
    w = 64
    r = 8
    b = 32
    key_phrase = b'qwerty'
    return RC5(w, r, b, key_phrase)


@pytest.fixture
def temp_files():
    # Create temporary input and output files
    input_file = tempfile.NamedTemporaryFile(delete=False).name
    output_file = tempfile.NamedTemporaryFile(delete=False).name

    yield input_file, output_file

    # Clean up temporary files after the test
    os.remove(input_file)
    os.remove(output_file)


def test_init(rc5_instance):
    assert rc5_instance.w == 64
    assert rc5_instance.r == 8
    assert rc5_instance.b == 32
    assert rc5_instance.key_phrase == b'qwerty'
    assert rc5_instance.nulbits == 0
    assert rc5_instance.w4 == 64 // 4
    assert rc5_instance.u == 64 // 8
    assert rc5_instance.c == ceil(max(32, 1) / (64 // 8))
    assert rc5_instance.t == 2 * (8 + 1)
    assert rc5_instance.mod == (2 ** 64)
    assert rc5_instance.mask == (2 ** 64) - 1
    assert len(rc5_instance.L) == ceil(max(32, 1) / (64 // 8))
    assert len(rc5_instance.S) == (2 * (8 + 1))


def test_rotate_left(rc5_instance):
    res = rc5_instance._rotate_left(0b01, 1)
    assert res == 2


def test_rotate_right(rc5_instance):
    res = rc5_instance._rotate_right(0b100, 2)
    assert res == 1


def test_key_hash1(rc5_instance):
    rc5_instance.b = 8
    rc5_instance._key_hash()
    key = rc5_instance.K
    assert len(key) == 8


def test_key_hash2(rc5_instance):
    rc5_instance.b = 16
    rc5_instance._key_hash()
    key = rc5_instance.K
    assert len(key) == 16


def test_key_hash3(rc5_instance):
    rc5_instance.b = 32
    rc5_instance._key_hash()
    key = rc5_instance.K
    assert len(key) == 32


def test_encrypt_block(rc5_instance):
    data = b'testdata12345678'
    encrypted_data = rc5_instance.encrypt_block(data)
    assert encrypted_data == b'g\x90\xde\x19\xe3\x1a?\x832\x9e\xa56?,>\xcb'


def test_decrypt_block(rc5_instance):
    data = b'g\x90\xde\x19\xe3\x1a?\x832\x9e\xa56?,>\xcb'
    decrypted_data = rc5_instance.decrypt_block(data)
    assert decrypted_data == b'testdata12345678'


def test_encrypt_bytes(rc5_instance):
    data = b'test data 1234'
    encrypted_data = rc5_instance.encrypt_bytes(data)
    assert encrypted_data == b'\x9f\xcbs0\xc8I\xc1\xbe\xadW\xe6~\x7fk\xbd"'


def test_decrypt_bytes(rc5_instance):
    data = b'\x9f\xcbs0\xc8I\xc1\xbe\xadW\xe6~\x7fk\xbd"'
    decrypted_data = rc5_instance.decrypt_bytes(data)
    assert decrypted_data == b'test data 1234'


def test_encrypt_decrypt_file(rc5_instance, temp_files):
    input_file, output_file = temp_files

    test_data = b'This is a test data.'

    with open(input_file, 'wb') as f:
        f.write(test_data)

    rc5_instance.encrypt_file(input_file, output_file)

    rc5_instance.decrypt_file(output_file, input_file)

    rc5_instance._cut_off_this_fucking_null_bits(input_file)

    with open(input_file, 'rb') as f:
        decrypted_data = f.read()

    assert decrypted_data == test_data

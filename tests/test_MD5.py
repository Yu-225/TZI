import pytest
from bitarray import bitarray

from modules.MD5 import MD5, MD5Buffer


@pytest.fixture
def md5_instance():
    return MD5()


def test_step_1(md5_instance):
    result = md5_instance._step_1()
    assert isinstance(result, bitarray)
    assert len(result) % 512 == 448


def test_step_2(md5_instance):
    md5_instance._string = b"test"
    step_1_result = md5_instance._step_1()
    result = md5_instance._step_2(step_1_result)
    assert isinstance(result, bitarray)
    assert len(result) % 512 == 0




def test_step_3(md5_instance):
    md5_instance._buffers = {
        MD5Buffer.A: 0x12345678,
        MD5Buffer.B: 0x87654321,
        MD5Buffer.C: 0xabcdefab,
        MD5Buffer.D: 0xfedcba98,
    }
    md5_instance._step_3()
    assert md5_instance._buffers[MD5Buffer.A] == MD5Buffer.A.value
    assert md5_instance._buffers[MD5Buffer.B] == MD5Buffer.B.value
    assert md5_instance._buffers[MD5Buffer.C] == MD5Buffer.C.value
    assert md5_instance._buffers[MD5Buffer.D] == MD5Buffer.D.value


def test_step_4(md5_instance):
    md5_instance._string = b'test'
    step_2_result = md5_instance._step_2(md5_instance._step_1())
    md5_instance._step_3()

    md5_instance._step_4(step_2_result)

    assert md5_instance._buffers[MD5Buffer.A] == 3446378249
    assert md5_instance._buffers[MD5Buffer.B] == 1943216454
    assert md5_instance._buffers[MD5Buffer.C] == 2202984138
    assert md5_instance._buffers[MD5Buffer.D] == 4139001638


def test_step_5(md5_instance):
    result = md5_instance._step_5()
    assert isinstance(result, str)
    assert len(result) == 32
    assert all(char in "0123456789ABCDEF" for char in result)


def test_hash(md5_instance):
    result = md5_instance.hash("test")
    assert isinstance(result, str)
    assert len(result) == 32
    assert all(char in "0123456789ABCDEF" for char in result)


def test_update(md5_instance):
    md5_instance.update("test")
    result = md5_instance.hexdigest()
    assert isinstance(result, str)
    assert len(result) == 32
    assert all(char in "0123456789ABCDEF" for char in result)


def test_hexdigest(md5_instance):
    result = md5_instance.hexdigest()
    assert isinstance(result, str)
    assert len(result) == 32
    assert all(char in "0123456789ABCDEF" for char in result)


def test_digest(md5_instance):
    result = md5_instance.digest()
    assert isinstance(result, bytes)
    assert len(result) == 16
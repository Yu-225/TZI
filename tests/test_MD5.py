import pytest
from modules.MD5 import MD5


@pytest.fixture
def md_5():
    return MD5()


def test_init(md_5):
    assert md_5._string == b''


def test_hash(md_5):
    md_5.hash(b'a')
    result = md_5.hexdigest()
    assert result == "0CC175B9C0F1B6A831C399E269772661"

    md_5.hash('test_string')
    result = md_5.hexdigest()
    assert result == "3474851A3410906697EC77337DF7AAE4"


def test_update(md_5):
    md_5.update('a')
    result = md_5.digest()
    assert result == b'\x0c\xc1u\xb9\xc0\xf1\xb6\xa81\xc3\x99\xe2iw&a'
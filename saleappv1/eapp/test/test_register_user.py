from .base import test_app, test_session,mock_cloudinary
import pytest
from ..models import User
from ..dao import add_user
import hashlib

def test_register_success(test_session):
    add_user(name = "abc", username="tester", password="aBc@1234", avatar=None)
    u = User.query.filter(User.username.__eq__("tester")).first()
    assert u
    assert u.name == "abc"
    assert u.password == str(hashlib.md5("aBc@1234".encode("utf-8")).hexdigest())

def test_exsiting_username(test_session):
    add_user(name="abc", username="demodemo", password="aBc@1234", avatar=None)
    with pytest.raises(Exception):
        add_user(name="abc", username="demodemo", password="aBc@1234", avatar=None)

@pytest.mark.parametrize("password", [

    "1bB", "1"*8,'A'*8,'a'*8,'a1'*4,'aA'*4,
])
def test_invalid_password(password, test_session):
    with pytest.raises(ValueError):
        add_user(name="abc", username="demodemo", password=password, avatar=None)

def test_constrainst(test_session):
    with pytest.raises(Exception):
        add_user(name="abc", username="demodemo", password=password, avatar=None)

def test_avatar(test_session, mock_cloudinary):
    add_user(name="abc", username="demodemo", password="aBc!23451", avatar="Asdasfwef")

    u = User.query.filter(User.name.__eq__('abc')).first()

    assert u.avatar == "https://fake-image.com"
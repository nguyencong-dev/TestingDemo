from pytest_mock import mocker
from unicodedata import category

from eapp.test.base import test_client, test_app, test_session
from eapp.models import User, Product, ReceiptDetails, Receipt


def test_pay_success(test_client,mocker):
    class FakeUser:
        is_authenticated = True

    mocker.patch("flask_login.utils._get_user", return_value=FakeUser())
    mocker.patch('eapp.dao.current_user',return_value=FakeUser)


    with test_client.session_transaction() as sess:
        sess['cart'] = {
            "1": {
                "id": "1",
                "name": "aaaa",
                "price": 123,
                "quantity": 2
            },
            "2": {
                "id": "2",
                "name": "bbb",
                "price": 123,
                "quantity": 3
            }
        }

    receipt_add = mocker.patch('eapp.dao.add_receipt')

    res = test_client.post("/api/pay")

    assert res.status_code == 200
    assert res.get_json()['status'] == 200
    receipt_add.assert_called_once()


def test_pay_exception(test_client,mocker):
    class FakeUser:
        is_authenticated = True

    mocker.patch("flask_login.utils._get_user", return_value=FakeUser())
    mocker.patch('eapp.dao.current_user',return_value=FakeUser)


    with test_client.session_transaction() as sess:
        sess['cart'] = {
            "1": {
                "id": "1",
                "name": "aaaa",
                "price": 123,
                "quantity": 2
            },
            "2": {
                "id": "2",
                "name": "bbb",
                "price": 123,
                "quantity": 3
            }
        }

    receipt_add = mocker.patch('eapp.dao.add_receipt', side_effect=Exception('DB Error'))

    res = test_client.post("/api/pay")

    data = res.get_json()
    assert data['status'] == 400
    assert data['err_msg'] == 'DB Error'

    with test_client.session_transaction() as sess:
        assert  'cart' in sess

    receipt_add.assert_called_once()

def test_all(test_client, test_session, mocker):
    class FakeUser:
        is_authenticated = True

    mocker.patch("flask_login.utils._get_user", return_value=FakeUser())

    u = User(name='a', username='demo',password='123')
    test_session.add(u)

    p = Product(name='Xiami', price='50', category_id='2')
    test_session.add(p)
    test_session.commit()

    mocker.patch('eapp.dao.current_user', u)

    test_client.post('/api/carts',json={

            "id": "1",
            "name": "HueWei",
            "price": 123,
    })

    test_client.post('/api/carts', json={

        "id": "1",
        "name": "Honor",
        "price": 123,
    })

    res = test_client.post('/api/pay')
    assert res.status_code == 200

    with test_client.session_transaction() as sess:
        assert 'cart' not in sess

    assert Receipt.query.count() == 1
    assert ReceiptDetails.query.count() == 1
    d = ReceiptDetails.query.first()
    assert  d.product_id == 1
    assert d.quantity == 2


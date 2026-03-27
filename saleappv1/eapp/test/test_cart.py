from statistics import quantiles

from flask import session

from eapp.test.base import test_client, test_app

def test_add_to_cart_successful(test_client):
    res = test_client.post('api/carts',json={
        'id': 1,
        'name': 'iPhone 17',
        'price':50
    })

    assert res.status_code == 200

    data = res.get_json()

    assert data['total_quantity'] == 1
    with test_client.session_transaction() as sess:
        assert  'cart' in sess
        assert  '1' in sess['cart']


def test_cart_inscrease_quatity(test_client):
    test_client.post('api/carts', json={
        'id': 1,
        'name': 'iPhone 17',
        'price': 50
    })

    test_client.post('api/carts', json={
        'id': 1,
        'name': 'iPhone 17',
        'price': 50
    })

    res = test_client.post('api/carts',json={
        'id': 1,
        'name': 'iPhone 17',
        'price':50
    })

    data = res.json()

    assert data['total_quantity'] == 3
    assert data['total_amount'] == 150

    with test_client.session_transaction() as sess:
        assert len(sess['cart']) == 2
        assert sess['cart']['1']['quantity'] == 2
        assert sess['cart']['2']['quantity'] == 1

def test_update_cart(test_client):
    with test_client.session_transaction() as sess:
        sess['cart'] = {
            "1": {
                "id": "1",
                "name": "aaaa",
                "price": 123,
                "quantity": 2
            }
        }
    res = test_client.put('/api/carts/1', json={
        'quantity': 10
    })

    data = res.get_json()

    assert data['total_quantity'] == 10
    with test_client.session_transaction() as sess:
        assert len(sess['cart']) == 1
        assert sess['cart']['1']['quantity'] == 10


def test_del_cart_successful(test_client):
    with test_client.session_transaction() as sess:
        sess['cart'] = {
            "1": {
                "id": "1",
                "name": "aaaa",
                "price": 123,
                "quantity": 2
            }
        }

    res = test_client.delete('/api/carts/1')
    data = res.get_json()
    assert data['total_quantity'] == 0

    with test_client.session_transaction() as sess:
        assert len(sess['cart']) == 0
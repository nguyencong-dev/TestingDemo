from eapp.dao import load_products
from eapp.models import Product
from .base import test_app, test_session
import pytest

@pytest.fixture
def sample_products(test_session):
    p1 = Product(name="iPhone", price="30", category_id=1)
    p2 = Product(name="Xiaomi", price="20", category_id=2)
    p3 = Product(name="Samsung", price="36", category_id=1)
    p4 = Product(name="iPhone 17 pro max", price="46", category_id=3)
    p5 = Product(name="Honor magic 7 pro", price="71", category_id=2)

    test_session.add_all([p1,p2,p3,p4,p5])
    test_session.commit()
    return [p1,p2,p3,p4,p5]

def test_all(sample_products):
    actual_products = load_products()
    assert  len(actual_products) == len(sample_products)

def test_keywords(sample_products):
    actual_products = load_products(kw="Sa")
    assert len(actual_products) == 1
    assert all("Samsung" in p.name for p in actual_products)

def test_category(sample_products):
    actual_products = load_products(cate_id=1)
    assert len(actual_products) == 2
    assert all(p.category_id == 1 for p in actual_products)
    assert ("iPhone" in p.name for p in actual_products)
    assert ("Samsung" in p.name for p in actual_products)

def test_kw_cate(sample_products):
    actual_products = load_products(cate_id=2, kw="Ho")

    assert len(actual_products) == 1
    assert "Honor magic 7 pro" in actual_products[0].name
    assert actual_products[0].category_id == 2

def test_paging(sample_products):
    actual_products = load_products(page = 1)
    assert len(actual_products) == 2
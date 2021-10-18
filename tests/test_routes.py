"""
Shopcart API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
from unittest import TestCase
from unittest.mock import MagicMock, patch
from service import status  # HTTP Status Codes
from service.models import db
from service.routes import app, init_db
from tests.factories import ProductFactory, ShopcartFactory

BASE_URL = "/shopcarts"
CONTENT_TYPE_JSON = "application/json"

######################################################################
#  T E S T   C A S E S
######################################################################
class TestYourResourceServer(TestCase):
    """ REST API Server Tests """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        pass

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        pass

    def setUp(self):
        """ This runs before each test """
        self.app = app.test_client()

######################################################################
#  H E L P E R   M E T H O D S
######################################################################

    def _create_products_list(self, count):
        """Create a list with count number of random products"""
        products = []
        for _ in range(count):
            test_product = ProductFactory()
            resp = self.app.post(
                BASE_URL, json=test_product.serialize(), content_type=CONTENT_TYPE_JSON
            )
            self.assertEqual(
                resp.status_code, status.HTTP_201_CREATED, "Could not create test product list"
            )
            new_product = resp.get_json()
            test_product.id = new_product["id"]
            test_product.shopcart_id = new_product["shopcart_id"]
            test_product.product_id = new_product["product_id"]
            test_product.product_name = new_product["product_name"]
            test_product.price = new_product["price"]
            test_product.quantity = new_product["quantity"]
            test_product.in_stock = new_product["in_stock"]
            test_product.wishlist = new_product["wishlist"]
            products.append(test_product)
        return products
    
    def _create_shopcarts(self, test_products_list):
        """Create a random shopcart with existing product list"""
        shopcarts = []
        test_shopcart = ShopcartFactory()
        resp = self.app.post(
                f"{BASE_URL}/{test_shopcart.customer_id}", json=test_shopcart.serialize(), content_type=CONTENT_TYPE_JSON
        )
        new_shopcart = resp.get_json()
        test_shopcart.customer_id = new_shopcart["customer_id"]
        test_shopcart.product_list = test_products_list
        shopcarts.append(test_shopcart)
        return shopcarts

######################################################################
#  P L A C E   T E S T   C A S E S   H E R E
######################################################################

    def test_index(self):
        """ Test index call """
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_list_products_in_cart(self):
        
        """List all product of a shopcart"""
        products = self._create_products_list(5)
        test_shopcart = self._create_shopcarts(products)[0]
        resp = self.app.get(
            "/shopcarts/{}".format(test_shopcart.customer_id), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEquals( len(resp.data) > 0)
        

    def test_get_shopcarts(self):
        """Get a single Shopcart"""
        # get the id of a shopcart

        # Mucheng's version:
        products = self._create_products_list(5)
        test_shopcart = self._create_shopcarts(products)[0]
        # test_shopcart = self._create_shopcarts(1)[0]
        resp = self.app.get(
            "/shopcarts/{}".format(test_shopcart.customer_id), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        # TODO: WE DONT HAVE SHOPCART NAME FOR NOW
        # self.assertEqual(data["name"], test_shopcart.name)

    def test_create_shopcart(self):

        """Create a new Shopcart"""
        test_shopcart = ShopcartFactory()
        logging.debug(test_shopcart)
        resp = self.app.post(
            f"{BASE_URL}/{test_shopcart.customer_id}", json=test_shopcart.serialize(), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Check the data is correct
        new_shopcart = resp.get_json()
        self.assertEqual(new_shopcart["customer_id"], test_shopcart.customer_id, "Customer ids do not match")




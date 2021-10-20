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
DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/postgres"
)

######################################################################
#  T E S T   C A S E S
######################################################################
class TestYourResourceServer(TestCase):
    """ REST API Server Tests """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db()

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        db.session.close()

    def setUp(self):
        """ This runs before each test """
        db.drop_all()  # clean up the last tests
        db.create_all()  # create new tables
        self.app = app.test_client()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()

######################################################################
#  H E L P E R   M E T H O D S
######################################################################

    # this will be not useful for now, but will be kept here just in case it is needed in the future
    # def _create_products_list(self, count):
    #     """Create a list with count number of random products"""
    #     products = []
    #     for _ in range(count):
    #         test_product = ProductFactory()
    #         resp = self.app.post(
    #             BASE_URL, json=test_product.serialize(), content_type=CONTENT_TYPE_JSON
    #         )
    #         self.assertEqual(
    #             resp.status_code, status.HTTP_201_CREATED, "Could not create test product list"
    #         )
    #         new_product = resp.get_json()
    #         test_product.id = new_product["id"]
    #         test_product.shopcart_id = new_product["shopcart_id"]
    #         test_product.product_id = new_product["product_id"]
    #         test_product.product_name = new_product["product_name"]
    #         test_product.price = new_product["price"]
    #         test_product.quantity = new_product["quantity"]
    #         test_product.in_stock = new_product["in_stock"]
    #         test_product.wishlist = new_product["wishlist"]
    #         products.append(test_product)
    #     return products
    
    def _create_shopcarts(self, count):
        """Create shopcarts in bulk"""
        shopcarts = []
        for _ in range(count):
            test_shopcart = ShopcartFactory()
            resp = self.app.post(
                    "/shopcarts", json=test_shopcart.serialize(), content_type=CONTENT_TYPE_JSON
            )
            self.assertEqual(
                resp.status_code, status.HTTP_201_CREATED, "Could not create test Shopcart"
            )
            new_shopcart = resp.get_json()
            test_shopcart.customer_id = new_shopcart["customer_id"]
            shopcarts.append(test_shopcart)
        return shopcarts

######################################################################
#  P L A C E   T E S T   C A S E S   H E R E
######################################################################

    def test_index(self):
        """ Test index call """
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_list_shopcarts(self):
        
        """List all shopcarts"""
        self._create_shopcarts(3)
        resp = self.app.get("/shopcarts")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEquals( len(data), 3)
        

    def test_get_shopcarts(self):
        """Get a single Shopcart"""
        # get the id of a shopcart

        test_shopcart = self._create_shopcarts(1)[0]
        resp = self.app.get("/shopcarts/{}".format(test_shopcart.customer_id))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["customer_id"], test_shopcart.customer_id)

    def test_create_shopcart(self):

        """Create a new Shopcart"""
        test_shopcart = ShopcartFactory()
        logging.debug(test_shopcart)
        resp = self.app.post(
            "/shopcarts", json=test_shopcart.serialize(), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # Check the location is correct
        location = resp.headers.get("Location", None)
        self.assertIsNotNone(location)
        
        # Check the data is correct
        new_shopcart = resp.get_json()
        self.assertEqual(new_shopcart["product_list"], test_shopcart.product_list, "Product list do not match")


    def test_delete_shopcart(self):
        """Delete a shopcart"""
        test_shopcart = self._create_shopcarts(1)[0]
        resp = self.app.delete(
            "{0}/{1}".format(BASE_URL, test_shopcart.customer_id), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        # make sure they are deleted
        resp = self.app.get(
            "{0}/{1}".format(BASE_URL, test_shopcart.customer_id), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_shopcart(self):
        """Update a shopcart"""

        #create the shopcart
        test_cart = ShopcartFactory()
        logging.debug(test_cart.serialize())
        resp = self.app.post(
            "/shopcarts", 
            json=test_cart.serialize(), 
            content_type=CONTENT_TYPE_JSON
        )

        #test add a product price to the shopcart
        test_cart.customer_id = resp.get_json()["customer_id"]
        test_product = ProductFactory()
        test_product.shopcart_id = test_cart.customer_id
        logging.debug(test_product.serialize())
        resp = self.app.put(
            "/shopcarts/{}".format(test_cart.customer_id), 
            json=test_product.serialize(), 
            content_type=CONTENT_TYPE_JSON
        )
        logging.debug(resp.get_json)
        self.assertEqual(resp.status_code, status.HTTP_202_ACCEPTED)
        
        #test update product price in the shopcart
        test_product.price = 10
        resp = self.app.put(
            "/shopcarts/{}".format(test_cart.customer_id),
            json=test_product.serialize(),
            content_type=CONTENT_TYPE_JSON
        )
        logging.debug(resp.get_json())
        self.assertEqual(resp.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(resp.get_json()["product_list"][0]["price"], 10.0)
        
        #test add one more product to the shopcart
        test_product = ProductFactory()
        test_product.shopcart_id = test_cart.customer_id
        resp = self.app.put(
            "/shopcarts/{}".format(test_cart.customer_id),
            json=test_product.serialize(),
            content_type=CONTENT_TYPE_JSON
        )
        logging.debug(resp.get_json())
        self.assertEqual(resp.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(len(resp.get_json()["product_list"]), 2)
        #test delete one more product to the shopcart
        
        test_product.quantity = -test_product.quantity
        resp = self.app.put(
            "/shopcarts/{}".format(test_cart.customer_id),
            json=test_product.serialize(),
            content_type=CONTENT_TYPE_JSON
        )
        logging.debug(resp.get_json())
        self.assertEqual(resp.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(len(resp.get_json()["product_list"]), 1)


    def test_list_products_in_shopcart(self):
        shopcart = self._create_shopcarts(1)[0]
        products = []
        for _ in range(2):
            product = ProductFactory()
            products.append(product)
        
        resp = self.app.post(
            "/shopcarts/{}/products".format(shopcart.customer_id),
            json = products[0].serialize(),
            content_type = "application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        resp = self.app.post(
            "/shopcarts/{}/products".format(shopcart.customer_id),
            json = products[1].serialize(),
            content_type = "application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        resp = self.app.get(
            "/shopcarts/{}/products".format(shopcart.customer_id),
            content_type = "applicationn/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        data = resp.get_json()
        self.assertEqual(len(data), 2)

    def test_add_product(self):
        shopcart = self._create_shopcarts(1)[0]
        product = ProductFactory()
        resp = self.app.post(
            "/shopcarts/{}/products".format(shopcart.customer_id),
            json = product.serialize(),
            content_type = "application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        data = resp.get_json()
        logging.debug(data)

        self.assertEqual(data["product_id"], product.product_id)
        self.assertEqual(data["product_name"], product.product_name)
        self.assertEqual(data["quantity"], product.quantity)
        self.assertEqual(data["price"], product.price)
        self.assertEqual(data["in_stock"], product.in_stock)
        self.assertEqual(data["wishlist"], product.wishlist)

    def test_create_bad_content_type(self):
        """Create shopcart with Bad Content Type """
        test_shopcart = ShopcartFactory()
        logging.debug(test_shopcart)
        resp = self.app.post(
            "/shopcarts", json=test_shopcart.serialize(), content_type='text/html'
        )
        self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_create_bad_method(self):
        """Create shopcart with Bad Method Type """
        test_shopcart = ShopcartFactory()
        logging.debug(test_shopcart)
        resp = self.app.put(
            "/shopcarts", json=test_shopcart.serialize(), content_type='text/html'
        )
        self.assertEqual(resp.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)




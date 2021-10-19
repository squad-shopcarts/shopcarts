"""
Test cases for Shopcart Model

"""
import logging
import unittest
import os
from service.models import Shopcart, Product, DataValidationError, db
from service import app
from .factories import ShopcartFactory, ProductFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/testdb"
)

######################################################################
#  SHOPCART   M O D E L   T E S T   C A S E S
######################################################################
class TestShopcartModel(unittest.TestCase):
    """ Test Cases for Shopcart Model """

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Shopcart.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        pass

    def setUp(self):
        db.drop_all()  # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()
        db.drop_all()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_a_shopcart(self):
        """Create a Shopcart and assert that it exists"""
        shopcart = Shopcart(customer_id=123456)
        self.assertTrue(shopcart != None)
        self.assertEqual(shopcart.customer_id, 123456)

        shopcart = Shopcart()
        self.assertEqual(shopcart.customer_id, None)

    def test_update_a_shopcart(self):
        """Update a customer shopcart"""
        shopcart = ShopcartFactory()
        shopcart.create()
        self.assertEqual(len(Shopcart.all()), 1)
        product = ProductFactory()
        product.shopcart_id = shopcart.customer_id
        shopcart.product_list.append(product)
        shopcart.update()
        self.assertEqual(len(shopcart.product_list),1)

    def test_delete_a_shopcart(self):
        """Delete a customer shopcart"""
        shopcart = ShopcartFactory()
        shopcart.create()
        self.assertEqual(len(Shopcart.all()), 1)
        # delete the order and make sure it isn't in the database
        shopcart.delete()
        self.assertEqual(len(Shopcart.all()), 0)

    def test_Serialize_a_shopcart(self):
        """Serialize a shopcart"""
        #create the shopcart
        test_cart = ShopcartFactory()
        serialized_info = test_cart.serialize()
        self.assertEqual(serialized_info["customer_id"], test_cart.customer_id)

    def test_deserialize_a_shopcart(self):
        """Deserialize a shopcart"""
        #create the shopcart
        shopcart = ShopcartFactory()
        shopcart.create()
        product = ProductFactory()
        product.shopcart_id = shopcart.customer_id
        shopcart.product_list.append(product)
        shopcart.update()
        new_shopcart = ShopcartFactory()
        new_shopcart.deserialize(shopcart.serialize())
        logging.debug(shopcart.serialize())
        self.assertEqual(len(new_shopcart.product_list), 1)

    def test_add_a_shopcart(self):
        """Create a shopcart and add it to the database"""
        shopcarts = Shopcart.all()
        self.assertEqual(shopcarts, [])
        shopcart = Shopcart(
            product_list = []
        )
        self.assertTrue(shopcart != None)
        shopcart.create()
        self.assertEqual(shopcart.customer_id, 1)
        shopcarts = Shopcart.all()
        self.assertEqual(len(shopcarts), 1)

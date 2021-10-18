"""
Test cases for Shopcart Model

"""
import logging
import unittest
import os
from service.models import Shopcart, Product, DataValidationError, db
from service import app

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
        db.session.close()

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


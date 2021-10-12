"""
Models for YourResourceModel

All of the models are stored in this module
"""
import logging
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """

    pass

class Product(db.Model):
    """
    Class that represents a Shopcart
    """

    app = None

    # Table Schema
    product_id = db.Column(db.Integer, primary_key=True)
    in_stock  = db.Column(db.Boolean(), nullable=False)
    price  = db.Column(db.Float, nullable=False)
    wishlist = db.Column(db.Boolean(), nullable=False)

    def serialize(self):
        """ Serializes a Shopcart into a dictionary """
        return {"product_id": self.product_id,
                 "in_stock": self.in_stock,
                 "price": self.price,
                 "wishlist": self.wishlist}

    # create deserialize(self, data)

class Shopcart(db.Model):
    """
    Class that represents a Shopcart
    """

    app = None

    # Table Schema
    customer_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    unit_price  = db.Column(db.Float, nullable=False)
    quantity  = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<Shopcart for user_id: %s>" % (self.customer_id)

    def create(self):
        """
        Creates a Shopcart to the database
        """
        logger.info("Creating shopcart for user_id: %s", self.customer_id)
        #self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def save(self):
        """
        Updates a Shopcart to the database
        """
        logger.info("Saving %s", self.customer_id)
        db.session.commit()

    def delete(self):
        """ Removes a Shopcart from the data store """
        logger.info("Deleting %s", self.customer_id)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes a Shopcart into a dictionary """
        return {"customer_id": self.customer_id,
                 "product_id": self.product_id,
                 "unit_price": self.unit_price,
                 "quantity": self.quantity}

    def deserialize(self, data):
        """
        Deserializes a Shopcart from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.product_id = data["product_id"]
            self.unit_price = data["unit_price"]
            self.quantity = data ["quantity"]

        except KeyError as error:
            raise DataValidationError(
                "Invalid Shopcart: missing " + error.args[0]
            )
        except TypeError as error:
            raise DataValidationError(
                "Invalid Shopcart: body of request contained bad or no data"
            )
        return self

    @classmethod
    def init_db(cls, app):
        """ Initializes the database session """
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """ Returns all of the YourResourceModels in the database """
        logger.info("Processing all YourResourceModels")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """ Finds a YourResourceModel by it's ID """
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)

    @classmethod
    def find_or_404(cls, by_id):
        """ Find a YourResourceModel by it's id """
        logger.info("Processing lookup or 404 for id %s ...", by_id)
        return cls.query.get_or_404(by_id)

    @classmethod
    def find_by_name(cls, name):
        """Returns all YourResourceModels with the given name

        Args:
            name (string): the name of the YourResourceModels you want to match
        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)

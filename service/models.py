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

######################################################################
#  P R O D U C T   M O D E L
######################################################################
class Product(db.Model):
    """
    Class that represents an Product in each shopping cart
    """
    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    shopcart_id = db.Column(db.Integer, db.ForeignKey('customer_order.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=True)
    price = db.Column(db.Float, nullable=False)
    item_name = db.Column(db.String(120), nullable=False)

    def delete(self):
        pass

    def add(self):
        pass

    def serialize(self):
        pass

    def deserialize(self, data):
        pass

######################################################################
#  S H O P C A R T   M O D E L
######################################################################
class Shopcart(db.Model):

    """
    Class that represents a Shopcart
    """

    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String(63))
    # total_price = db.Column(db.Float, nullable=False)
    # total_quatinty = db.Column(db.Integer, nullable=True)
    products = db.relationship('Product', backref='shopcart', lazy=True)  

    def __repr__(self):
        return "<YourResourceModel %r id=[%s]>" % (self.name, self.id)

    def create(self):
        """
        Creates a YourResourceModel to the database
        """
        logger.info("Creating %s", self.name)
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def save(self):
        """
        Updates a YourResourceModel to the database
        """
        logger.info("Saving %s", self.name)
        db.session.commit()

    def delete(self):
        """ Removes a YourResourceModel from the data store """
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes a YourResourceModel into a dictionary """
        return {"id": self.id, "name": self.name}

    def deserialize(self, data):
        """
        Deserializes a YourResourceModel from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.name = data["name"]
        except KeyError as error:
            raise DataValidationError(
                "Invalid YourResourceModel: missing " + error.args[0]
            )
        except TypeError as error:
            raise DataValidationError(
                "Invalid YourResourceModel: body of request contained bad or no data"
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

    # @classmethod
    # def all(cls):
    #     """ Returns all of the YourResourceModels in the database """
    #     logger.info("Processing all YourResourceModels")
    #     return cls.query.all()

    # @classmethod
    # def find(cls, by_id):
    #     """ Finds a YourResourceModel by it's ID """
    #     logger.info("Processing lookup for id %s ...", by_id)
    #     return cls.query.get(by_id)

    # @classmethod
    # def find_or_404(cls, by_id):
    #     """ Find a YourResourceModel by it's id """
    #     logger.info("Processing lookup or 404 for id %s ...", by_id)
    #     return cls.query.get_or_404(by_id)

    # @classmethod
    # def find_by_name(cls, name):
    #     """Returns all YourResourceModels with the given name

    #     Args:
    #         name (string): the name of the YourResourceModels you want to match
    #     """
    #     logger.info("Processing name query for %s ...", name)
    #     return cls.query.filter(cls.name == name)

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
    Class that represents a Shopcart
    """

    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    shopcart_id = db.Column(db.Integer, db.ForeignKey('shopcart.customer_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=True)
    price  = db.Column(db.Float, nullable=False)
    in_stock  = db.Column(db.Boolean(), nullable=False)
    wishlist = db.Column(db.Boolean(), nullable=False)


    def delete(self):
        pass

    def add(self):
        pass

    def serialize(self):
        """ Serializes a Shopcart into a dictionary """
        return {"product_id": self.id,
                "quantity": self.quantity,
                "price": self.price,
                "shopcart_id":self.shopcart_id,
                 "in_stock": self.in_stock,
                 "wishlist": self.wishlist
                }

    def deserialize(self, data):
        try:
            self.shopcart_id = int(data["shopcart_id"])
            self.product_id = int(data["name"])
            self.name = data["name"]
            self.quantity = int(data["quantity"])
            self.price = float(data["price"])
            if data['in_stock'] == 'True':
                self.in_stock = True
            else:
                self.in_stock = False
            if data['wishlist'] == 'True': 
                self.wishlist = True
            else:
                self.wishlist = False

        except KeyError as error:
            raise DataValidationError("Invalid Address: missing " + error.args[0])
        except TypeError as error:
            raise DataValidationError(
                "Invalid Address: body of request contained" "bad or no data"
            )
        return self

######################################################################
#  S H O P C A R T   M O D E L
######################################################################
class Shopcart(db.Model):

    """
    Class that represents a Shopcart
    """
    app = None

    # Table Schema

    customer_id = db.Column(db.Integer, primary_key=True)
    # total_price  = db.Column(db.Float, nullable=False)
    # total_quantity  = db.Column(db.Integer, nullable=False)
    products = db.relationship('Product', backref='shopcart', lazy=True)  

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
        shopcart =  {
            "customer_id": self.customer_id,
            "products":[]
        }
        for product in self.products:
            shopcart["products"].append(product.serialize())
        return shopcart

    def deserialize(self, data):
        """
        Deserializes a Shopcart from a dictionary
        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.name = data["customer_id"]
            # handle inner list of addresses
            product_list = data.get("products")
            for json_product in product_list:
                product = Product()
                product.deserialize(json_product)
                self.products.append(product)
        except KeyError as error:
            raise DataValidationError("Invalid Account: missing " + error.args[0])
        except TypeError as error:
            raise DataValidationError(
                "Invalid Account: body of request contained" "bad or no data"
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

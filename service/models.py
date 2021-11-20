"""
Models for YourResourceModel
All of the models are stored in this module
"""
import logging
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()

# def init_db(app):
#     """Initialies the SQLAlchemy app"""
#     Pet.init_db(app)


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
    customer_id = db.Column(db.Integer, db.ForeignKey(
        'shopcart.customer_id'), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    product_name = db.Column(db.String(120), nullable=False)
    quantity = db.Column(db.Integer, nullable=True)
    price = db.Column(db.Float, nullable=False)
    instock = db.Column(db.Boolean(), nullable=False)
    wishlist = db.Column(db.Boolean(), nullable=False)

    def delete(self):
        logger.info("Deleting Product %s", self.id)
        db.session.delete(self)
        db.session.commit()

    def create(self):
        """
        Creates a Product to the database
        """
        logger.info("Creating %s", self.id)
        self.id = None
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates a product to the database
        """
        logger.info("Saving %s", self.id)
        db.session.commit()

    def serialize(self):
        """ Serializes a Shopcart into a dictionary """
        return {"id": self.id,
                "customer_id": self.customer_id,
                "product_id": self.product_id,
                "product_name": self.product_name,
                "quantity": self.quantity,
                "price": self.price,
                "instock": str(self.instock).lower(),
                "wishlist": str(self.wishlist).lower()
                }

    def deserialize(self, data):
        # logging.debug(data["customer_id"])
        try:
            self.customer_id = int(data["customer_id"])
            self.product_id = int(data["product_id"])
            self.product_name = data["product_name"]
            self.quantity = int(data["quantity"])
            self.price = float(data["price"])
            self.instock = (data["instock"] == 'true')
            self.wishlist = (data["wishlist"] == 'true')
            logging.debug(self.wishlist)
        except KeyError as error:
            raise DataValidationError(
                "Invalid Address: missing " + error.args[0])
        except TypeError as error:
            raise DataValidationError(
                "Invalid Address: body of request contained" "bad or no data"
            )
        return self

    ##################################################
    # CLASS METHODS
    ##################################################

    @classmethod
    def find(cls, by_id):
        """ Finds a product by it's product.id """
        logger.info("Processing lookup for Product.id %s ...", by_id)
        return cls.query.get(by_id)

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
    product_list = db.relationship('Product', backref='shopcart', lazy=True)
    # total_price  = db.Column(db.Float, nullable=False)
    # total_quantity  = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<Shopcart for customer_id: %s>" % (self.customer_id)

    def create(self):
        """
        Creates a Shopcart to the database
        """
        logger.info("Creating shopcart for customer_id: %s", self.customer_id)
        self.customer_id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def update(self):
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
        shopcart = {
            "customer_id": self.customer_id,
            "product_list": []
        }
        for product in self.product_list:
            shopcart["product_list"].append(product.serialize())
        return shopcart

    def deserialize(self, data):
        """
        Deserializes a Shopcart from a dictionary
        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            # handle inner list of addresses
            product_list = data["product_list"]
            for json_product in product_list:
                product = Product()
                product.deserialize(json_product)
                product.create()
                self.product_list.append(product)
        except KeyError as error:
            raise DataValidationError(
                "Invalid Account: missing " + error.args[0])
        except TypeError as error:
            raise DataValidationError(
                "Invalid Account: body of request contained" "bad or no data"
            )
        return self

    ##################################################
    # CLASS METHODS
    ##################################################

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
    def find(cls, customer_id):
        """ Finds a shopcart by it's ID """
        logger.info("Processing lookup for customer_id %s ...", customer_id)
        return cls.query.get(customer_id)

    @classmethod
    def all(cls):
        """ Returns all of the Shopcarts in the database """
        logger.info("Processing all Shopcarts")
        return cls.query.all()

    # @classmethod
    # def find_or_404(cls, by_id):
    #     """ Find a YourResourceModel by it's id """
    #     logger.info("Processing lookup or 404 for id %s ...", by_id)
    #     return cls.query.get_or_404(by_id)

    # @classmethod
    # def find_by_name(cls, name):
    #     """Returns all YourResourceModels with the given name
    #     Args:
    #     name (string): the name of the YourResourceModels you want to match
    #     """
    #     logger.info("Processing name query for %s ...", name)
    #     return cls.query.filter(cls.name == name)

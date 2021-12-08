######################################################################
# Copyright 2016, 2020 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################

"""
Shopcarts Service with Swagger

Paths:
------
GET / - Displays a UI for Selenium testing
GET /shopcarts - Returns a list all of the Shopcarts
GET /shopcarts/{id} - Returns the Shopcart with a given id number
POST /shopcarts - creates a new Shopcart record in the database
PUT /shopcarts/{id} - updates a Shopcart record in the database
DELETE /shopcarts/{id} - deletes a Shopcart record in the database
DELETE /shopcarts/{id}/products/{id} - deletes a product record in the shopcart
"""

import sys
import secrets
import logging
from functools import wraps
from flask import jsonify, request, url_for, make_response, render_template
from flask_restx import Api, Resource, fields, reqparse, inputs
from service.models import Product, Shopcart, DataValidationError, DatabaseConnectionError
from . import app, status    # HTTP Status Codes

# Document the type of autorization required
# authorizations = {
#     'apikey': {
#         'type': 'apiKey',
#         'in': 'header',
#         'name': 'X-Api-Key'
#     }
# }


######################################################################
# Configure the Root route before OpenAPI
######################################################################
@app.route('/')
def index():
    """ Index page """
    return app.send_static_file('index.html')


######################################################################
# GET HEALTH CHECK
######################################################################
@app.route('/healthcheck')
def healthcheck():
    """ Let them know our heart is still beating """
    return make_response(jsonify(status=200, message='Healthy'), status.HTTP_200_OK)


######################################################################
# Configure Swagger before initializing it
######################################################################
api = Api(app,
          version='1.0.0',
          title='Shopcart RESTX API Service',
          description='This is a server for Shopcarts service.',
          default='shopcarts',
          default_label='shopcart operations',
          doc='/apidocs',  # default also could use doc='/apidocs/'
          #   authorizations=authorizations,
          #   prefix='/api'
          )


# Define the model so that the docs reflect what can be sent
product_model = api.model('Product', {
    "customer_id": fields.Integer,
    "product_id": fields.Integer,
    "product_name": fields.String,
    "quantity": fields.Integer,
    "price": fields.Float,
    "instock": fields.Boolean,
    "wishlist": fields.Boolean,

})

shopcart_model = api.model('Shopcart', {
    'customer_id': fields.Integer(description='The customer id of the shopcart'),
    'product_list': fields.List(fields.Nested(product_model),
                                description='The List of Product in Shopcart'),
})

# shopcart_model = api.inherit(
#     'ShopcartModel',
#     create_model,
#     {
#         '_id': fields.String(readOnly=True,
#                              description='The unique id assigned internally by service'),
#     }
# )


# query string arguments
shopcart_args = reqparse.RequestParser()
shopcart_args.add_argument('customer-id', type=int, required=False,
                           help='List Wishlisted Items')

######################################################################
# Special Error Handlers
######################################################################


@api.errorhandler(DataValidationError)
def request_validation_error(error):
    """ Handles Value Errors from bad data """
    message = str(error)
    app.logger.error(message)
    return {
        'status_code': status.HTTP_400_BAD_REQUEST,
        'error': 'Bad Request',
        'message': message
    }, status.HTTP_400_BAD_REQUEST


@api.errorhandler(DatabaseConnectionError)
def database_connection_error(error):
    """ Handles Database Errors from connection attempts """
    message = str(error)
    app.logger.critical(message)
    return {
        'status_code': status.HTTP_503_SERVICE_UNAVAILABLE,
        'error': 'Service Unavailable',
        'message': message
    }, status.HTTP_503_SERVICE_UNAVAILABLE


######################################################################
# Authorization Decorator
######################################################################
# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = None
#         if 'X-Api-Key' in request.headers:
#             token = request.headers['X-Api-Key']

#         if app.config.get('API_KEY') and app.config['API_KEY'] == token:
#             return f(*args, **kwargs)
#         else:
#             return {'message': 'Invalid or missing token'}, 401
#     return decorated


######################################################################
# Function to generate a random API key (good for testing)
######################################################################
# def generate_apikey():
#     """ Helper function used when testing API keys """
#     return secrets.token_hex(16)

######################################################################
#  PATH: /shopcarts
######################################################################
@api.route('/shopcarts', strict_slashes=False)
class ShopcartCollection(Resource):
    """ Handles all interactions with collections of Shopcarts """

    # ------------------------------------------------------------------
    # CREATE A NEW SHOPCART
    # ------------------------------------------------------------------
    @api.doc('create_shopcart')
    @api.response(400, 'The posted Shopcart data was not valid')
    @api.expect(shopcart_model)
    @api.marshal_with(shopcart_model)
    def post(self):
        """
        Creates a Shopcart
        This endpoint will create a Shopcart based the data in the body that is posted
        """
        app.logger.info('Request to Create a Shopcart')
        shopcart = Shopcart()
        app.logger.debug('Payload = %s', api.payload)
        shopcart.deserialize(api.payload)
        shopcart.create()
        app.logger.info(
            'Shopcart with new id [%s] created!', shopcart.customer_id)
        location_url = api.url_for(
            ShopcartResource, customer_id=shopcart.customer_id, _external=True)
        return shopcart.serialize(), status.HTTP_201_CREATED, {'Location': location_url}

    # ------------------------------------------------------------------
    # LIST ALL SHOPCARTS
    # ------------------------------------------------------------------
    @api.doc('list_shopcarts')
    @api.marshal_list_with(shopcart_model)
    def get(self):
        """ Returns all of the Shopcarts """
        app.logger.info("Request for all shopcarts")
        shopcarts = Shopcart.all()
        app.logger.info('[%s] Shopcarts returned', len(shopcarts))
        results = [shopcart.serialize() for shopcart in shopcarts]
        return results, status.HTTP_200_OK


######################################################################
#  PATH: /shopcarts/{customer_id}
######################################################################
@api.route('/shopcarts/<int:customer_id>')
@api.param('customer_id', 'The shopcart identifier')
class ShopcartResource(Resource):
    """
    Shopcart Resource class

    Allows the manipulation of a single Shopcart
    GET /shopcarts/{id} - Returns a Shopcart with the id
    PUT /shopcarts/{id} - Update a Shopcart with the id
    DELETE /shopcarts/{id} -  Deletes a Shopcart with the id
    """

    # ------------------------------------------------------------------
    # RETRIEVE A Shopcart
    # ------------------------------------------------------------------
    @api.doc('get_shopcart')
    @api.response(404, 'Shopcart not found')
    @api.marshal_with(shopcart_model)
    def get(self, customer_id):
        """
        Retrieve a single Shopcart

        This endpoint will return a shopcart based on it's id
        """
        app.logger.info(
            f"Request to Retrieve a shopcart with id {customer_id}")
        shopcart = Shopcart.find(customer_id)
        if not shopcart:
            abort(status.HTTP_404_NOT_FOUND,
                  f"Shopcart with id {customer_id} was not found.")
        return shopcart.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # DELETE A SHOPCART
    # ------------------------------------------------------------------
    @api.doc('delete_shopcart')
    @api.response(204, 'Shopcart deleted')
    def delete(self, customer_id):
        """
        Delete a Shopcart

        This endpoint will delete a Shopcart based the customer_id specified in the path
        """
        app.logger.info(
            'Request to Delete a Shopcart with id [%s]', customer_id)
        shopcart = Shopcart.find(customer_id)
        if shopcart:
            shopcart.delete()
            app.logger.info(
                'Shopcart with customer_id [%s] was deleted', customer_id)
        return '', status.HTTP_204_NO_CONTENT

######################################################################
#  PATH: /shopcarts/{customer_id}/products
######################################################################


@api.route('/shopcarts/<customer_id>/products')
@api.param('customer_id', 'The Shopcart identifier')
class ProductResource(Resource):
    # ------------------------------------------------------------------
    # GET PRODUCTS IN A SHOPCART
    # ------------------------------------------------------------------
    @api.doc('get_products_list')
    @api.marshal_list_with(product_model)
    def get(self, customer_id):
        """
        Return the product list of a shopcart 
        """
        app.logger.info("Request for product list in a shopcart")
        shopcart = Shopcart.find(customer_id)
        results = [product.serialize() for product in shopcart.product_list]
        return results, status.HTTP_200_OK

    # ------------------------------------------------------------------
    # ADD A PRODUCT TO A SHOPCART
    # ------------------------------------------------------------------
    @api.doc('purchase_product')
    def post(self, customer_id):
        """
        Add a product to a shopcart

        This endpoint will purchase a Shopcart and make it unavailable
        """
        app.logger.info("Request to add a product into a shopcart")
        shopcart = Shopcart.find(customer_id)
        app.logger.warning(f"Found Shopcart with id {shopcart.customer_id}")
        product = Product()
        product.deserialize(request.get_json())
        app.logger.warning(
            f"Created Product with info:"
            f"id {product.id}\n"
            f"customer_id {product.customer_id}\n"
            f"product_id {product.product_id}\n"
            f"price {product.price}\n"
            f"quantity {product.quantity}\n"
            f"instock {product.instock}\n"
            f"wishlist {product.wishlist}\n"
        )
        shopcart.product_list.append(product)
        shopcart.update()
        return product.serialize(), status.HTTP_201_CREATED


######################################################################
#  PATH: /shopcarts/{customer_id}/products/{product_id}
######################################################################
@api.route('/shopcarts/<int:customer_id>/products/<int:product_id>')
@api.param('customer_id', 'The shopcart identifier')
@api.param('product_id', 'The product identifier')
class ProductCollection(Resource):
    """ Handles all product in Shopcart with collections of Prodcut """
    # ------------------------------------------------------------------
    # UPDATE AN EXISTING Shopcart
    # ------------------------------------------------------------------
    @api.doc('update_shopcart')
    @api.response(404, 'Shopcart not found')
    @api.response(400, 'The posted Product data was not valid')
    @api.response(404, 'Product not found')
    @api.expect(product_model)
    @api.marshal_with(product_model)
    def put(self, customer_id, product_id):
        """
        Update a Shopcart

        This endpoint will update a Shopcart based the body that is posted
        """
        app.logger.info(f'Request to Update a Shopcart with id {customer_id}, product id {product_id}')
        app.logger.debug('Payload = %s', api.payload)
        data = api.payload
        if int(data["quantity"]) <= 0:
            abort(status.HTTP_400_BAD_REQUEST,
                  f"Quantity have to be a POSITIVE INTEGER.")
        shopcart = Shopcart.find(customer_id)
        if not shopcart:
            abort(status.HTTP_404_NOT_FOUND,
                  f"Shopcart with id {customer_id} was not found.")
        shopcart_info = shopcart.serialize()
        if (len(shopcart_info["product_list"]) == 0) or (
                not any(p["product_id"] == product_id for p in shopcart_info["product_list"])):
            product = Product()
            product.deserialize(data)
            product.create()
            shopcart.product_list.append(product)
            shopcart.update()
            return product.serialize(), status.HTTP_200_OK
        else:
            for json_product in shopcart_info["product_list"]:
                if json_product["product_id"] == product_id:
                    product = Product.find(int(json_product["id"]))
                    product.product_name = data["product_name"]
                    product.quantity = int(data["quantity"])
                    product.price = float(data["price"])
                    product.instock = (data["instock"] == "true")
                    product.wishlist = (data["wishlist"] == "true")
                    product.update()
                    return product.serialize(), status.HTTP_200_OK
        abort(status.HTTP_404_NOT_FOUND,
              "Product with id {} not found".format(product_id))

    # ------------------------------------------------------------------
    # GET A PRODUCT IN A SHOPCART
    # ------------------------------------------------------------------
    @api.doc('get_a_product')
    @api.response(404, 'Shopcart not found')
    @api.response(404, 'Product not found')
    @api.marshal_with(product_model)
    def get(self, customer_id, product_id):
        """
        Retrieve a single Product

        This endpoint will return a product of a shopcart 
        """
        app.logger.info("Request to get a product in a shopcart")
        shopcart = Shopcart.find(customer_id)
        if not shopcart:
            abort(status.HTTP_404_NOT_FOUND,
                  "shopcart with id {} not found".format(customer_id))
        products = shopcart.product_list
        for product in products:
            if product.product_id == product_id:
                return product.serialize(), status.HTTP_200_OK
        abort(status.HTTP_404_NOT_FOUND, "can not find product with id {} in shopcart {}".format(
            product_id, customer_id))

    # ------------------------------------------------------------------
    # DELETE A PRODUCT IN A SHOPCART
    # ------------------------------------------------------------------

    @api.doc('delete_a_product')
    @api.response(404, 'Shopcart not found')
    @api.response(404, 'Product not found')
    @api.response(204, 'Product deleted')
    def delete(self, customer_id, product_id):
        """
        Delete a product in a Shopcart

        This endpoint will delete a product in a shopcart based the customer_id and product_id specified in the path
        """
        app.logger.info(
            "Request to delete a product with product_id in a shopcart with customer_id: %s", customer_id)
        shopcart = Shopcart.find(customer_id)
        if shopcart:
            products = shopcart.product_list
            for product in products:
                if product.product_id == product_id:
                    product.delete()
                    app.logger.info(
                        'Product with product_id [%s] in the shopcart with customer_id [%s] was deleted', product_id, customer_id)
                    return product.serialize(), status.HTTP_204_NO_CONTENT
            abort(status.HTTP_404_NOT_FOUND, "can not find product with id {} in shopcart {}".format(
                product_id, customer_id))
        else:
            abort(status.HTTP_404_NOT_FOUND,
                  "shopcart with id {} not found".format(customer_id))


######################################################################
# PATH: /shopcarts/<int:customer_id>/products/<int:product_id>/reversewishlist
######################################################################


@api.route('/shopcarts/<int:customer_id>/products/<int:product_id>/reversewishlist')
@api.param('customer_id', 'The shopcart identifier')
@api.param('product_id', 'The product identifier')
class ReverseWishlistCollection(Resource):
    """Handles reverse product wishlist in Shopcart with action of resource"""
    # ------------------------------------------------------------------
    # REVERSE AN EXISTING product in Shopcart
    # ------------------------------------------------------------------
    @api.doc('reverse_wishlist')
    @api.response(404, 'Object not found')
    @api.response(400, 'The Product is not valid for reverse')
    @api.marshal_with(product_model)
    def put(self, customer_id, product_id):
        """
        Reverse a product wishlist state
        """
        app.logger.info(f'Request to Find a shopcart with id {customer_id}')
        shopcart = Shopcart.find(customer_id)
        if not shopcart:
            return (f"Account with id {customer_id} was not found",
                    status.HTTP_404_NOT_FOUND)
        shopcart_info = shopcart.serialize()
        if (len(shopcart_info["product_list"]) == 0) or (
                not any(p["product_id"] == product_id for p in shopcart_info["product_list"])):
            return (f"Product with product_id {product_id} was not found",
                    status.HTTP_404_NOT_FOUND)
        else:
            for json_product in shopcart_info["product_list"]:
                if json_product["product_id"] == product_id:
                    product = Product.find(int(json_product["id"]))
                    product.wishlist = not product.wishlist
                    product.update()
                    app.logger.info(
                        f'Product wishlist Status now {product.wishlist}')
                    app.logger.info(product.serialize())
                    return product, status.HTTP_200_OK

######################################################################
#  PATH: /shopcarts/wishlist
######################################################################


@api.route('/shopcarts/wishlist', strict_slashes=False)
class WishlistResource(Resource):
    # ------------------------------------------------------------------
    # LIST ALL WISHLISTED ITEMS
    # ------------------------------------------------------------------
    @api.doc('list_wishlisted_products')
    @api.response(400, 'Missing customer id from query string')
    @api.response(404, 'Shopcart not found')
    @api.expect(shopcart_args, validate=True)
    @api.marshal_list_with(product_model)
    def get(self):
        """
        List a shopcart wishlist
        """
        customer_id = request.args.get('customer-id', None)
        if not customer_id:
            abort(
                status.HTTP_400_BAD_REQUEST,
                "Missing customer id from query string"
            )
        shopcart = Shopcart.find(customer_id)
        if not shopcart:
            abort(
                status.HTTP_404_NOT_FOUND,
                "shopcart with id {customer_id} not found",
            )
        products = [product.serialize() for product in shopcart.product_list]
        wishlisted_items = []
        
        for product in products:
            if product['wishlist'] == 'true':
                wishlisted_items.append(product)
        app.logger.info(f"Request for cart {customer_id} to return Wishlisted Items: {wishlisted_items}")
        return wishlisted_items, status.HTTP_200_OK


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################
def abort(error_code: int, message: str):
    """Logs errors before aborting"""
    app.logger.error(message)
    api.abort(error_code, message)


@ app.before_first_request
def init_db():
    """ Initlaize the model """
    global app
    Shopcart.init_db(app)

# load sample data


# def data_load(payload):
#     """ Loads a Shopcart into the database """
#     Shopcart = Shopcart(payload['customer_id'], payload['product_list'])
#     Shopcart.create()


# def data_reset():
#     """ Removes all Shopcarts from the database """
#     Shopcart.remove_all()

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
# pet_args = reqparse.RequestParser()
# pet_args.add_argument('name', type=str, required=False,
#                       help='List Shopcarts by name')
# pet_args.add_argument('category', type=str, required=False,
#                       help='List Shopcarts by category')
# pet_args.add_argument('available', type=inputs.boolean,
#                       required=False, help='List Shopcarts by availability')

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
#  PATH: /shopcarts/{customer_id}/product/{product_id}
######################################################################


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
    # RETRIEVE A PET
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
                  f"Shopcart with id '{customer_id}' was not found.")
        return shopcart.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # UPDATE AN EXISTING PET
    # ------------------------------------------------------------------
    # @api.doc('update_pets', security='apikey')
    # @api.response(404, 'Pet not found')
    # @api.response(400, 'The posted Pet data was not valid')
    # @api.expect(pet_model)
    # @api.marshal_with(pet_model)
    # @token_required
    # def put(self, pet_id):
    #     """
    #     Update a Pet

    #     This endpoint will update a Pet based the body that is posted
    #     """
    #     app.logger.info('Request to Update a pet with id [%s]', pet_id)
    #     pet = Pet.find(pet_id)
    #     if not pet:
    #         abort(status.HTTP_404_NOT_FOUND,
    #               "Pet with id '{}' was not found.".format(pet_id))
    #     app.logger.debug('Payload = %s', api.payload)
    #     data = api.payload
    #     pet.deserialize(data)
    #     pet.id = pet_id
    #     pet.update()
    #     return pet.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # DELETE A PET
    # ------------------------------------------------------------------
    # @api.doc('delete_pets', security='apikey')
    # @api.response(204, 'Pet deleted')
    # @token_required
    # def delete(self, pet_id):
    #     """
    #     Delete a Pet

    #     This endpoint will delete a Pet based the id specified in the path
    #     """
    #     app.logger.info('Request to Delete a pet with id [%s]', pet_id)
    #     pet = Pet.find(pet_id)
    #     if pet:
    #         pet.delete()
    #         app.logger.info('Pet with id [%s] was deleted', pet_id)

    #     return '', status.HTTP_204_NO_CONTENT


######################################################################
#  PATH: /pets
######################################################################
# @api.route('/shopcarts', strict_slashes=False)
# class ShopcartCollection(Resource):
#     """ Handles all interactions with collections of Shopcarts """
#     ------------------------------------------------------------------
#     LIST ALL PETS
#     ------------------------------------------------------------------
    # @api.doc('list_pets')
    # @api.expect(pet_args, validate=True)
    # @api.marshal_list_with(pet_model)
    # def get(self):
    #     """ Returns all of the Pets """
    #     app.logger.info('Request to list Pets...')
    #     pets = []
    #     args = pet_args.parse_args()
    #     if args['category']:
    #         app.logger.info('Filtering by category: %s', args['category'])
    #         pets = Pet.find_by_category(args['category'])
    #     elif args['name']:
    #         app.logger.info('Filtering by name: %s', args['name'])
    #         pets = Pet.find_by_name(args['name'])
    #     elif args['available'] is not None:
    #         app.logger.info('Filtering by availability: %s', args['available'])
    #         pets = Pet.find_by_availability(args['available'])
    #     else:
    #         app.logger.info('Returning unfiltered list.')
    #         pets = Pet.all()

    #     app.logger.info('[%s] Pets returned', len(pets))
    #     results = [pet.serialize() for pet in pets]
    #     return results, status.HTTP_200_OK

    # ------------------------------------------------------------------
    # ADD A NEW PET
    # ------------------------------------------------------------------

    # @api.doc('create_shopcarts')  # security = 'apikey'
    # @api.response(400, 'The posted data was not valid')
    # @api.expect(shopcart_model)
    # @api.marshal_with(shopcart_model, code=201)
    # @token_required
    # def post(self):
    #     """
    #     Creates a Pet
    #     This endpoint will create a Pet based the data in the body that is posted
    #     """
    #     app.logger.info('Request to Create a Pet')
    #     shopcart = Shopcart()
    #     app.logger.debug('Payload = %s', api.payload)
    #     shopcart.deserialize(api.payload)
    #     shopcart.create()
    #     app.logger.info('Pet with new id [%s] created!', shopcart.customer_id)
    #     location_url = api.url_for(
    #         PetResource, customer_id=shopcart.customer_id, _external=True)
    #     return shopcart.serialize(), status.HTTP_201_CREATED, {'Location': location_url}

    # ------------------------------------------------------------------
    # DELETE ALL PETS (for testing only)
    # ------------------------------------------------------------------
    # @api.doc('delete_all_pets', security='apikey')
    # @api.response(204, 'All Pets deleted')
    # @token_required
    # def delete(self):
    #     """
    #     Delete all Pet

    #     This endpoint will delete all Pet only if the system is under test
    #     """
    #     app.logger.info('Request to Delete all pets...')
    #     if "TESTING" in app.config and app.config["TESTING"]:
    #         Pet.remove_all()
    #         app.logger.info("Removed all Pets from the database")
    #     else:
    #         app.logger.warning(
    #             "Request to clear database while system not under test")

    #     return '', status.HTTP_204_NO_CONTENT


######################################################################
#  PATH: /pets/{id}/purchase
######################################################################
# @api.route('/pets/<pet_id>/purchase')
# @api.param('pet_id', 'The Pet identifier')
# class PurchaseResource(Resource):
#     """ Purchase actions on a Pet """
#     @api.doc('purchase_pets')
#     @api.response(404, 'Pet not found')
#     @api.response(409, 'The Pet is not available for purchase')
#     def put(self, pet_id):
#         """
#         Purchase a Pet

#         This endpoint will purchase a Pet and make it unavailable
#         """
#         app.logger.info('Request to Purchase a Pet')
#         pet = Pet.find(pet_id)
#         if not pet:
#             abort(status.HTTP_404_NOT_FOUND,
#                   'Pet with id [{}] was not found.'.format(pet_id))
#         if not pet.available:
#             abort(status.HTTP_409_CONFLICT,
#                   'Pet with id [{}] is not available.'.format(pet_id))
#         pet.available = False
#         pet.update()
#         app.logger.info('Pet with id [%s] has been purchased!', pet.id)
#         return pet.serialize(), status.HTTP_200_OK


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################

def abort(error_code: int, message: str):
    """Logs errors before aborting"""
    app.logger.error(message)
    api.abort(error_code, message)


@app.before_first_request
def init_db():
    """ Initlaize the model """
    global app
    Shopcart.init_db(app)

# load sample data


# def data_load(payload):
#     """ Loads a Pet into the database """
#     Shopcart = Shopcart(payload['customer_id'], payload['product_list'])
#     Shopcart.create()


# def data_reset():
#     """ Removes all Pets from the database """
#     Shopcart.remove_all()

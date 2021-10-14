"""
Shopcarts Service

"""

import os
import sys
print(sys.path)
import logging
from flask import Flask, jsonify, request, url_for, make_response, abort
from . import status  # HTTP Status Codes
from werkzeug.exceptions import NotFound

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from flask_sqlalchemy import SQLAlchemy
from models import Shopcart, Product, DataValidationError

# Import Flask application
from . import app

######################################################################
# GET INDEX
######################################################################


@app.route("/shopcarts")
def index():
    """ Root URL response """
    return (
        "Route of shopcart service",
        status.HTTP_200_OK,
    )


@app.route("/shopcarts/<int:customer_id>", methods=["GET"])
def list_cart(customer_id):

    # Retrieve a shopcart
    # This endpoint will return a shopcart item list based
    # the id specified customer_id in the path

    app.logger.info(f"Request for shopcart with id: {customer_id}")

    return (
        "Shopcart Item List",
        status.HTTP_200_OK,
    )


@app.route("/shopcarts/<int:customer_id>", methods=["POST"])
def create_cart(customer_id):
    """
    Create a shopcart
    This endpoint will create a shopcart based the id specified in the path
    """
    app.logger.info(f"A shopcart for user with id: {customer_id} created")
    return (
        f"Shopcart for user {customer_id} created",
        status.HTTP_200_OK,
    )

######################################################################
# RETRIEVE A SHOPCART
######################################################################


@app.route("/shopcatrs/<int:customer_id>", methods=["GET"])
def get_shopcarts(customer_id):
    """
    Retrieve a single Shopcart
    This endpoint will return a Shopcart based on it's id
    """
    app.logger.info("Request for shopcart with id: %s", customer_id)
    shopcart = Shopcart.find(customer_id)
    if not shopcart:
        raise NotFound(
            "Shopcart with id '{}' was not found.".format(customer_id))

    # TODO: WE DONT HAVE A SHOPCART NAME RIGHTNOW
    # app.logger.info("Returning shopcart: %s", shopcart.name)
    return make_response(jsonify(shopcart.serialize()), status.HTTP_200_OK)


@app.route("/shopcarts/<int:customer_id>", methods=["PUT"])
def update_cart(customer_id):
    """
    Update a shopcart
    This endpoint will update a shopcart based on the body it post
    """
    update_receive = request.get_json()
    shopcart = Shopcart.find(customer_id)
    if not shopcart:
        raise NotFound(f"Account with id '{customer_id}' was not found.")
    shopcart_info = shopcart.serialize()
    for json_product in shopcart_info['products']:
        if json_product['product_id'] == update_receive['product_id']:
            # not finished
        else:
            new_product = Product()
            new_product.deserialize(update_receive)
            shopcart.products.append(new_product)

    return (
        "Shopcart Item <itemid> updated",
        status.HTTP_202_ACCEPTED,
    )


@app.route("/shopcarts/<int:customer_id>", methods=["DELETE"])
def delete_cart(customer_id):
    """
    Delete a Shopcart
    This endpoint will delete a Shopcart based the id specified in the path
    """
    app.logger.info(f"Shopcart for user: {customer_id} deleted")
    return (
        f"No Shopcart for customer: {customer_id} anymore",
        status.HTTP_200_OK,
    )

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


# def init_db():
#     """ Initialies the SQLAlchemy app """
#     global app
#     YourResourceModel.init_db(app)

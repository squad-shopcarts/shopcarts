"""
Shopcarts Service

"""

from . import app
from service.models import Shopcart, Product, DataValidationError
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import NotFound
from . import status  # HTTP Status Codes
from flask import Flask, jsonify, request, url_for, make_response, abort
import logging
import os
import sys
print(sys.path)

# For this example we"ll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL

# Import Flask application

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

######################################################################
# LIST ALL PRODUCTS IN SHOPCART
######################################################################


@app.route("/shopcarts/<int:customer_id>", methods=["GET"])
def list_products_in_cart(customer_id):
    """
    Retrieve products in shopcart with specific customer_id
    This endpoint will return a shopcart products list based the customer_id in the path
    """
    app.logger.info(
        "Request for all products in shopcart with id: %s", customer_id)
    shopcart = Shopcart.find(customer_id)
    if not shopcart:
        return(f"Shopcart with id {customer_id} was not found",
               status.HTTP_404_NOT_FOUND)

    product_list = shopcart.serialize()# ["product_list"]
    return make_response(jsonify(product_list), status.HTTP_200_OK)


@app.route("/shopcarts/<int:customer_id>", methods=["POST"])
def create_cart(customer_id):
    """
    Create a shopcart
    This endpoint will create a shopcart based the id specified in the path
    """
    
        return (
            f"Shopcart for user {customer_id} existed",
            status.HTTP_200_OK,
        )

######################################################################
# RETRIEVE A SHOPCART
######################################################################


@app.route("/shopcatrs/<int:customer_id>", methods=["GET"])
def get_shopcarts(customer_id):
    """
    Retrieve a single Shopcart
    This endpoint will return a Shopcart based on it"s id
    """
    app.logger.info("Request for shopcart with id: %s", customer_id)
    shopcart = Shopcart.find(customer_id)
    if not shopcart:
        return(
            f"Shopcart with id {customer_id} was not found",
            status.HTTP_404_NOT_FOUND
        )
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
        return (f"Account with id {customer_id} was not found",
            status.HTTP_404_NOT_FOUND)
    shopcart_info = shopcart.serialize()
    for json_product in shopcart_info["product_list"]:
        if json_product["product_id"] == int(update_receive["product_id"]):
            update_product = Product.find(int(json_product["id"]))
            update_product.quantity += json_product["quantity"]
            update_product.price = json_product["price"]
            update_product.update()
            break
    else:
        new_product = Product()
        new_product.deserialize(update_receive)
        new_product.create()
        shopcart.product_list.append(new_product)
        shopcart.update()

    return (
        f"Shopcart {customer_id} updated",
        status.HTTP_202_ACCEPTED)


@app.route("/shopcarts/<int:customer_id>", methods=["DELETE"])
def delete_cart(customer_id):
    """
    Delete a Shopcart
    This endpoint will delete a Shopcart based the id specified in the path
    """
    
    return (
        f"No Shopcart for customer: {customer_id} anymore",
        status.HTTP_200_OK,
    )

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def init_db():
    """ Initialies the SQLAlchemy app """
    global app
    Shopcart.init_db(app)

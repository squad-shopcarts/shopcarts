"""
Shopcarts Service

"""

import os
import sys
import logging
from flask import Flask, jsonify, request, url_for, make_response, abort
from . import status  # HTTP Status Codes

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from flask_sqlalchemy import SQLAlchemy
from service.models import Shopcart, DataValidationError

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


@app.route("/shopcarts/<userid>", methods=["GET"])
def list_cart():
    """
    Retrieve a shopcart
    This endpoint will return a shopcart item list based the id specified userid in the path
    """
    app.logger.info(f"Request for shopcart with id: {userid}")

    return (
        "Shopcart Item List",
        status.HTTP_200_OK,
    )


@app.route("/shopcarts/<userid>", methods=["POST"])
def create_shopcarts():
    """
    Create a shopcart
    This endpoint will create a shopcart based the id specified in the path
    """

    app.logger.info("Request to create a shopcart")
    check_content_type("application/json")
    shopcart = Shopcart()
    shopcart.deserialize(request.get_json())
    shopcart.create(userid)
    message = shopcart.serialize()
    # location_url = url_for("get_shopcarts", userid=userid, _external=True)
    app.logger.info(f"A shopcart for user with id: {userid} created")
    return make_response(
        jsonify(message),
        {f"Shopcart created for user: {userid}"},
        status.HTTP_200_OK
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
        raise NotFound("Shopcart with id '{}' was not found.".format(customer_id))

    # TODO: WE DONT HAVE A SHOPCART NAME RIGHTNOW
    # app.logger.info("Returning shopcart: %s", shopcart.name)
    return make_response(jsonify(shopcart.serialize()), status.HTTP_200_OK)


@app.route("/shopcarts/<userid>", methods=["PUT"])
def update_cart():
    """
    Update a shopcart
    This endpoint will update a shopcart based on the body it post
    """
    app.logger.info(f"Update shopcart for user: {userid} with item: {itemid}")
    return (
        "Shopcart Item <itemid> updated",
        status.HTTP_200_OK,
    )


@app.route("/shopcarts/<userid>", methods=["DELETE"])
def delete_cart():
    """
    Delete a Shopcart
    This endpoint will delete a Shopcart based the id specified in the path
    """
    app.logger.info(f"Shopcart for user: {userid} deleted")
    return (
        "No Shopcart for customer: <userid> anymore",
        status.HTTP_200_OK,
    )

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


# def init_db():
#     """ Initialies the SQLAlchemy app """
#     global app
#     YourResourceModel.init_db(app)

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
from service.models import YourResourceModel, DataValidationError

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
def update_cart():
    """
    Create a shopcart
    This endpoint will create a shopcart based the id specified in the path
    """
    app.logger.info(f"A shopcart for user with id: {userid} created")
    return (
        "Shopcart for user <userid> created",
        status.HTTP_200_OK,
    )


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

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


@app.route("/")
def index():
    """ Root URL response """
    return (
        "Route of shopcart service",
        status.HTTP_200_OK,
    )

######################################################################
# LIST ALL SHOPCARTS
######################################################################


@app.route("/shopcarts", methods=["GET"])
def list_shopcarts():
    """
    Retrieve shopcart if there is customer_id
    Or just retrieve all shopcarts as a list
    """
    app.logger.info(
        "Request for all shopcarts" )
    shopcarts = Shopcart.all()

    results = [ shopcart.serialize() for shopcart in shopcarts]
    return make_response(jsonify(results), status.HTTP_200_OK)

@app.route("/shopcarts", methods=["POST"])
def create_shopcart():
    """
    Create a shopcart
    This endpoint will create a shopcart 
    """
    if request.method != 'POST':
        return make_response("Method Not allow", status.HTTP_405_METHOD_NOT_ALLOWED)
    app.logger.info("Request to create a shopcart")
    check_content_type("application/json")
    shopcart = Shopcart()
    shopcart.deserialize(request.get_json())
    message = shopcart.serialize()
    shopcart.create()
    location_url = url_for("get_shopcarts", customer_id=shopcart.customer_id, _external=True)
    return make_response(
        jsonify(shopcart.serialize()), status.HTTP_201_CREATED, {"Location": location_url})

######################################################################
# RETRIEVE A SHOPCART
######################################################################


@app.route("/shopcarts/<int:customer_id>", methods=["GET"])
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

######################################################################
# UPDATE A SHOPCART
######################################################################

# @app.route("/shopcarts/<int:customer_id>", methods=["PUT"])
# def update_cart(customer_id):
#     """
#     Update a shopcart
#     This endpoint will update a shopcart based on the body it post
#     """
#     app.logger.info("Update for shopcart with id: %s", customer_id)
#     update_receive = request.get_json()
#     logging.debug("routesget:"+str(update_receive))
#     shopcart = Shopcart.find(customer_id)
#     if not shopcart:
#         return (f"Account with id {customer_id} was not found",
#             status.HTTP_404_NOT_FOUND)
#     shopcart_info = shopcart.serialize()
#     if len(shopcart_info["product_list"]) == 0:
#         new_product = Product()
#         new_product.deserialize(update_receive)
#         new_product.create()
#         logging.debug("routesnewproduct:"+str(shopcart.serialize()))
#         shopcart.update()
#     else :
#         for json_product in shopcart_info["product_list"]:
#             if json_product["product_id"] == update_receive["product_id"]:
#                 update_product = Product.find(int(json_product["id"]))
#                 update_product.quantity += int(update_receive["quantity"])
#                 update_product.price = float(update_receive["price"])
#                 logging.debug("routesupdateexist:" +
#                               str(update_receive["price"]))
#                 update_product.in_stock = update_receive["in_stock"]
#                 update_product.wishlist = update_receive["wishlist"]
#                 update_product.update()
#                 if update_product.quantity == 0:
#                     update_product.delete()
#                 break
#         else:
#             new_product = Product()
#             new_product.deserialize(update_receive)
#             new_product.create()
#             shopcart.product_list.append(new_product)
#             shopcart.update()

#     return make_response(
#         shopcart.serialize(),
#         status.HTTP_202_ACCEPTED
#     )

######################################################################
# UPDATE A ITEM IN SHOPCART 
######################################################################


@app.route("/shopcarts/<int:customer_id>/products/<int:product_id>", methods=["PUT"])
def update_cart(customer_id, product_id):
    """
    Update a item in a shopcart
    This endpoint will update a shopcart based on the body it post
    """
    app.logger.info(
        f"Update item: {product_id} for shopcart with id: {customer_id}", )
    update_receive = request.get_json()
    logging.debug("routesget:"+str(update_receive))
    shopcart = Shopcart.find(customer_id)
    if not shopcart:
        return (f"Account with id {customer_id} was not found",
            status.HTTP_404_NOT_FOUND)
    shopcart_info = shopcart.serialize()
    shopcart_info = shopcart.serialize()
    if len(shopcart_info["product_list"]) == 0:
        new_product = Product()
        new_product.deserialize(update_receive)
        new_product.create()
        logging.debug("routesnewproduct:"+str(shopcart.serialize()))
        shopcart.update()
    else:
        for json_product in shopcart_info["product_list"]:
            if json_product["product_id"] == product_id:
                update_product = Product.find(int(json_product["id"]))
                update_product.quantity += int(update_receive["quantity"])
                update_product.price = float(update_receive["price"])
                logging.debug("routesupdateexist:" +
                              str(update_receive["price"]))
                update_product.in_stock = update_receive["in_stock"]
                update_product.wishlist = update_receive["wishlist"]
                update_product.update()
                if update_product.quantity == 0:
                    update_product.delete()
                break
        else:
            new_product = Product()
            new_product.deserialize(update_receive)
            new_product.create()
            shopcart.product_list.append(new_product)
            shopcart.update()

    return make_response(
        shopcart.serialize(),
        status.HTTP_200_OK
    )

######################################################################
# RETRIVE PRODUCT LIST
######################################################################

@app.route("/shopcarts/<int:customer_id>/products", methods=["GET"])
def list_products_in_shopcart(customer_id):
    """
    Return the product list of a shopcart 
    """
    app.logger.info("Request for product list in a shopcart")
    shopcart = Shopcart.find(customer_id)
    results = [ product.serialize() for product in shopcart.product_list]
    return make_response(jsonify(results), status.HTTP_200_OK)

######################################################################
# ADD A PRODUCT INTO A SHOPCART
######################################################################

@app.route("/shopcarts/<int:customer_id>/products", methods=["POST"])
def create_products(customer_id):
    """
    Add a product into a shopcart
    """
    app.logger.info("Request to add a product into a shopcart")
    check_content_type("application/json")
    shopcart = Shopcart.find(customer_id)
    product = Product()
    product.deserialize(request.get_json())
    shopcart.product_list.append(product)
    shopcart.update()
    message = product.serialize()
    return make_response(jsonify(message), status.HTTP_201_CREATED)

# @app.route("/shopcarts/<int:customer_id>", methods=["DELETE"])
# def delete_cart(customer_id):
#     """
#     Delete a Shopcart
#     This endpoint will delete a Shopcart based the id specified in the path
#     """
    
#     return (
#         f"No Shopcart for customer: {customer_id} anymore",
#         status.HTTP_200_OK,
#     )

######################################################################
#  DELETE A SHOPCART
######################################################################
@app.route("/shopcarts/<int:customer_id>", methods=["DELETE"])
def delete_carts(customer_id):
    """
    Delete a Shopcart
    This endpoint will delete a shopcart based the customer_id specified in the path
    """
    app.logger.info("Request to delete a shopcart with customer_id: %s", customer_id)
    shopcart = Shopcart.find(customer_id)
    if shopcart:
        shopcart.delete()
        app.logger.info('Shopcart with customer_id [%s] was deleted', customer_id)
    return make_response("", status.HTTP_204_NO_CONTENT)

######################################################################
#  DELETE A PRODUCT IN A SHOPCART
######################################################################
@app.route("/shopcarts/<int:customer_id>/products/<int:product_id>", methods=["DELETE"])
def delete_a_product_in_shopcart(customer_id, product_id):
    """
    Delete a product in a Shopcart
    This endpoint will delete a product in a shopcart based the customer_id and product_id specified in the path
    """
    app.logger.info("Request to delete a product with product_id in a shopcart with customer_id: %s", customer_id)
    shopcart = Shopcart.find(customer_id)
    if shopcart:
        products = shopcart.product_list
        for product in products:
            if product.id == product_id:
                product.delete()
                app.logger.info('Product with product_id [%s] in the shopcart with customer_id [%s] was deleted', product_id,customer_id)
                return make_response("", status.HTTP_204_NO_CONTENT)
    else:
        abort(status.HTTP_404_NOT_FOUND,
                  f"shopcart with id {customer_id} not found")
    return make_response(
        "can not find product with id {product_id} in shopcart {customer_id}", 
        status.HTTP_404_NOT_FOUND
    )
    

######################################################################
#  GET A PRODUCT IN A SHOPCART
######################################################################
@app.route("/shopcarts/<int:customer_id>/products/<int:product_id>", methods=["GET"])
def get_a_product_in_shopcart(customer_id, product_id):
    """
    Return a product of a shopcart 
    """
    app.logger.info("Request to get a product in a shopcart")
    shopcart = Shopcart.find(customer_id)
    if not shopcart:
        return make_response(
                "shopcart with id {customer_id} not found",
                status.HTTP_404_NOT_FOUND
        )
    products = shopcart.product_list
    for product in products:
        if product.id == product_id:
            return make_response(
                jsonify(product.serialize()),
                status.HTTP_200_OK
            )
    return make_response(
        "can not find product with id {product_id} in shopcart {customer_id}", 
        status.HTTP_404_NOT_FOUND
    )

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def init_db():
    """ Initialies the SQLAlchemy app """
    global app
    Shopcart.init_db(app)

def check_content_type(media_type):
    """Checks that the media type is correct"""
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        "Content-Type must be {}".format(media_type),
    )

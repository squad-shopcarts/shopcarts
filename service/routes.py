"""
Shopcarts Service
"""
import logging
import sys
from flask import Flask, jsonify, request, url_for, make_response, abort
from . import app

from service.models import Shopcart, Product, DataValidationError
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import NotFound
from . import status  # HTTP Status Codes

print(sys.path)

# For this example we"ll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL

# Import Flask application

######################################################################
# GET HEALTH CHECK
######################################################################


@app.route("/healthcheck")
def healthcheck():
    """Let them know our heart is still beating"""
    return make_response(jsonify(status=200, message="Healthy"), status.HTTP_200_OK)

######################################################################
# GET INDEX
######################################################################


@app.route("/")
def index():
    return app.send_static_file("index.html")

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
        "Request for all shopcarts")
    shopcarts = Shopcart.all()

    results = [shopcart.serialize() for shopcart in shopcarts]
    return make_response(jsonify(results), status.HTTP_200_OK)


@app.route("/shopcarts", methods=["POST"])
def create_shopcart():
    """
    Create a shopcart
    This endpoint will create a shopcart 
    """
    if request.method != 'POST':
        return make_response("Method Not allow", status.HTTP_405_METHOD_NOT_ALLOWED)
    # app.logger.info("Request to create a shopcart")
    check_content_type("application/json")
    shopcart = Shopcart()
    shopcart.deserialize(request.get_json())
    message = shopcart.serialize()
    shopcart.create()
    app.logger.info(f"Request to create a shopcart id: {shopcart.customer_id}")
    location_url = url_for(
        "get_shopcarts", customer_id=shopcart.customer_id, _external=True)
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
# UPDATE A ITEM IN SHOPCART
######################################################################


@app.route("/shopcarts/<int:customer_id>/products/<int:product_id>", methods=["PUT"])
def update_cart(customer_id, product_id):
    """
    Update a item in a shopcart
    This endpoint will update a shopcart based on the body it post
    """
    app.logger.info(
        f"Start to update item: {product_id} for shopcart with id: {customer_id}", )
    update_receive = request.get_json()
    logging.debug("routesget:"+str(update_receive))
    if int(update_receive['quantity']) <= 0:
        return make_response("Quantity have to be a POSITIVE INTEGER", status.HTTP_400_BAD_REQUEST)
    shopcart = Shopcart.find(customer_id)
    if not shopcart:
        app.logger.info(
            f"Error to update item: {product_id} for shopcart with id: {customer_id}", )
        return (f"Account with id {customer_id} was not found",
                status.HTTP_404_NOT_FOUND)
    app.logger.info(
        f"Update item: {product_id} for shopcart with id: {customer_id}", )
    shopcart_info = shopcart.serialize()
    if len(shopcart_info["product_list"]) == 0:
        product = Product()
        product.deserialize(update_receive)
        product.create()
        logging.debug("routesnewproduct:"+str(shopcart.serialize()))
        shopcart.update()
    else:
        for json_product in shopcart_info["product_list"]:
            if json_product["product_id"] == product_id:
                product = Product.find(int(json_product["id"]))
                product.quantity = int(update_receive["quantity"])
                product.price = float(update_receive["price"])
                logging.debug("routesupdateexist:" +
                              str(update_receive["price"]))
                product.instock = (update_receive["instock"] == 'true')
                product.wishlist = (update_receive["wishlist"] == 'true')
                product.update()
                if product.quantity <= 0:
                    product.delete()
                    return make_response("", status.HTTP_204_NO_CONTENT)
                break
        else:
            product = Product()
            product.deserialize(update_receive)
            product.create()
            shopcart.product_list.append(product)
            shopcart.update()

    return make_response(
        product.serialize(),
        status.HTTP_200_OK
    )

######################################################################
# STATEFUL ACTION REVERSE WISHLIST STATUS
######################################################################


@app.route("/shopcarts/<int:customer_id>/products/<int:product_id>/reversewishlist", methods=["PUT"])
def stateful_reverse_wl(customer_id, product_id):
    """
    Convert a item wishlist status
    This endpoint will make the wishlist status of a item been reversed
    """
    # app.logger.info(
    #     f"Update item: {product_id} for shopcart with id: {customer_id}", )
    shopcart = Shopcart.find(customer_id)
    if not shopcart:
        return (f"Account with id {customer_id} was not found",
                status.HTTP_404_NOT_FOUND)
    shopcart_info = shopcart.serialize()
    if len(shopcart_info["product_list"]) == 0:
        return (f"Product with product_id {product_id} was not found",
                status.HTTP_404_NOT_FOUND)
    else:
        for json_product in shopcart_info["product_list"]:
            if json_product["product_id"] == product_id:
                update_product = Product.find(int(json_product["id"]))
                update_product.wishlist = not update_product.wishlist
                update_product.update()
                break
        else:
            return (f"Product with product_id {product_id} was not found",
                    status.HTTP_404_NOT_FOUND)

    return make_response(
        update_product.serialize(),
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
    results = [product.serialize() for product in shopcart.product_list]
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
    message = product.serialize()
    return make_response(jsonify(message), status.HTTP_201_CREATED)

######################################################################
#  DELETE A SHOPCART
######################################################################


@app.route("/shopcarts/<int:customer_id>", methods=["DELETE"])
def delete_carts(customer_id):
    """
    Delete a Shopcart
    This endpoint will delete a shopcart based the customer_id specified in the path
    """
    app.logger.info(
        "Request to delete a shopcart with customer_id: %s", customer_id)
    shopcart = Shopcart.find(customer_id)
    if shopcart:
        shopcart.delete()
        app.logger.info(
            'Shopcart with customer_id [%s] was deleted', customer_id)
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
        if product.product_id == product_id:
            return make_response(
                jsonify(product.serialize()),
                status.HTTP_200_OK
            )
    return make_response(
        "can not find product with id {product_id} in shopcart {customer_id}",
        status.HTTP_404_NOT_FOUND
    )

######################################################################
#  GET WISHLISTED ITEMS IN A SHOPCART
######################################################################


@app.route("/shopcarts/wishlist", methods=["GET"])
def get_wishlist_items():
    """ Returns all wishlisted items in a customers cart"""

    customer_id = request.args.get('customer-id', None)

    if not customer_id:
        return(
            f"Missing customer id from query string",
            status.HTTP_400_BAD_REQUEST
        )

    shopcart = Shopcart.find(customer_id)

    if not shopcart:
        return make_response(
            f"shopcart with id {customer_id} not found",
            status.HTTP_404_NOT_FOUND
        )

    products = [product.serialize() for product in shopcart.product_list]

    wishlisted_items = []

    for product in products:
        if product['wishlist'] == 'true':
            wishlisted_items.append(product)

    return make_response(jsonify(wishlisted_items), status.HTTP_200_OK)

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

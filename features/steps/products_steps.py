"""
Pet Steps

Steps file for Pet.feature

For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""
import json
import requests
from behave import given
from compare import expect

@given('the following products')
def step_impl(context):
    """ Load products """
    headers = {'Content-Type': 'application/json'}
    
    # load the database with new products
    for row in context.table:
        customer_id = context.customer_ids[int(row["shopcart"])]
        product_id = int(row["product_id"])
        print(customer_id, product_id)

        create_url = context.base_url + f'/shopcarts/{customer_id}/products'

        data = {
            "id": customer_id,
            "customer_id": customer_id,
            "product_id": row['product_id'],
            "product_name": row['product_name'],
            "price": row['price'],
            "quantity": row['quantity'],
            "instock": row['instock'],
            "wishlist": row['wishlist']
            }

        payload = json.dumps(data)
        context.resp = requests.post(create_url, data=payload, headers=headers)
        expect(context.resp.status_code).to_equal(201)


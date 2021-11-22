######################################################################
# Copyright 2016, 2021 John J. Rofrano. All Rights Reserved.
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
Shopcarts Steps

Steps file for Shopcarts.feature

For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""
import json
import requests
from behave import given
from compare import expect
from service.models import Shopcart, db
from flask_sqlalchemy import SQLAlchemy
from service import app
# db = SQLAlchemy()
# Shopcart.clear()
# Shopcart.clear()


@given('the following shopcarts')
def step_impl(context):
    """ Delete all Shopcarts and load new ones """
    headers = {'Content-Type': 'application/json'}

    # list all of the shopcarts and delete them one by one
    # context.resp = requests.get(
    #     context.base_url + '/shopcarts', headers=headers)
    # expect(context.resp.status_code).to_equal(200)
    # for shopcart in context.resp.json():
    #     context.resp = requests.delete(
    #         context.base_url + '/shopcarts/' + str(shopcart["customer_id"]), headers=headers)
    #     expect(context.resp.status_code).to_equal(204)

    # load the database with new shopcarts

    for row in context.table:
        get_url = context.base_url + '/shopcarts/' + str(row['shopcart'])
        get_cart_resp = requests.get(get_url, data="", headers=headers)
        if get_cart_resp.status_code == 200:
            continue
        else:
            create_url = context.base_url + '/shopcarts'
            data = {
                "product_list": []
            }
            payload = json.dumps(data)
            context.resp = requests.post(
                create_url, data=payload, headers=headers)
            expect(context.resp.status_code).to_equal(201)

        # we have no control currently over the customer_id so we have to capture it when we create a shopcart
        # context.customer_ids[i] = context.resp.headers.get(
        #     "Location", None).split('/')[-1]
        # i += 1

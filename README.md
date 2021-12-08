[![CI Build](https://github.com/squad-shopcarts/shopcarts/actions/workflows/docker-image.yml/badge.svg)](https://github.com/squad-shopcarts/shopcarts/actions/workflows/docker-image.yml)
[![codecov](https://codecov.io/gh/squad-shopcarts/shopcarts/branch/master/graph/badge.svg?token=QTIVMHFLFM)](https://codecov.io/gh/squad-shopcarts/shopcarts)

# nyu-devops-fall2021-squad-shopcarts
This is the repository for the Homework on NYU DevOps and Agile Methodologies
This repository is part of the NYU class **CSCI-GA.2810-001: DevOps and Agile Methodologies** taught by John Rofrano, Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science.

## Resource:
Resource URL: /shopcarts

## Project Overview
This project contains code for the shopcart service. The `/service` folder contains `models.py` file our shopcart and product model and a `routes.py` file for flask service. The `/tests` folder has tdd test case starter code for testing the model and the service separately. The `/features` folder has bdd test case starter code for testing the model, the service and the UI separately.

## Contents
The project contains the following:

```text
.coveragerc         - settings file for code coverage options
.devcontainers      - support for VSCode Remote Containers
.gitignore          - this will ignore vagrant and other metadata files
dot-env-example     - copy to .env to use environment variables
requirements.txt    - list if Python libraries required by your code
config.py           - configuration parameters
Procfile            - configuration honcho
manifest.yml        - configuration cloud foundry

service/                - service python package
├── __init__.py         - package initializer
├── models.py           - module with business models
├── routes.py           - module with service routes
├── status.py           - HTTP status constants
└── static              - frontend UI files
    ├── css                 - CSS files for UI
    ├── images              - images for UI
    ├── js                  - JavaScript support UI action
    └── index.html          - frontend HTML file

tests/              - TDD cases package
├── __init__.py     - package initializer
├── test_models.py  - test suite for busines models
└── test_routes.py  - test suite for service routes

features/               - BDD test case package
├── environment.py      - environment initializer
├── shopcarts.feature   - BDD test steps config file
└── steps               - BDD suite for model and UI
    ├── products_steps.py   - BDD suite for product model
    ├── shopcarts_steps.py  - BDD suite for shopcart model
    └── web_steps.py        - BDD suite for UI

Vagrantfile         - Vagrant file that installs Python 3 and PostgreSQL
```

**Note:** This repo has `.devcontainer` so it can run locally via VS Code (with devcontainer CLI):

```
devcontainer open
nosetests
honcho start
```
And run BDD test in a separate shell by running:
```
behave
```

These are the RESTful routes for `shopcart` and `product`
```
Endpoint                     Methods  Rule
---------------------------  -------  -----------------------------------------------
main_page                    GET      /
health_check                 GET      /healthcheck
list_shopcarts               GET      /shopcarts
create_a_shopcart            POST     /shopcarts
query_wishlist               GET      /shopcarts/<customer_id>
retrieve_a_shopcart          GET      /shopcarts/<customer_id>
delete_a_shopcart            DELETE   /shopcarts/<customer_id>
retrieve_product_list        GET      /shopcarts/<customer_id>/products
add_product_to_shopcarts     POST     /shopcarts/<customer_id>/products
update_item_in_shopcart      PUT      /shopcarts/<customer_id>/products/<product_id>
delete_product_in_shopcart   DELETE   /shopcarts/<customer_id>/products/<product_id>
retrieve_single_product      GET      /shopcarts/<customer_id>/products/<product_id>
reverse_item_wishlist_status PUT      /shopcarts/<customer_id>/products/<product_id>/wishlist
```

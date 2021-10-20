# nyu-devops-fall2021-squad-shopcarts
This is the repository for the Homework on NYU DevOps and Agile Methodologies

##Track List
Track List: https://www.notion.so/DevOps-Team-SC-0b9465760ff547a9964e9718e9a1afbe

## Resource:
Resource URL: /shopcarts

## Project Description:
The shopcarts resource allow customers to make a collection of products that they want to purchase. It should contain a reference to a product and the quantity the customer wants to buy. It may also contain the price of the product at the time they placed it in the cart. A customer will only have one shopcart. Since this is really a collection of product items, you will need to implement a subordinate REST API to place items into the shopcarts collection (e.g., / shopcarts/{id}/items). You also will need to associate the shopcart with a customer preferably through their customer id.

## Template Overview
This project template contains starter code for your class project. The `/service` folder contains your `models.py` file for your model and a `routes.py` file for your service. The `/tests` folder has test case starter code for testing the model and the service separately. All you need to do is add your functionality. You can use the [lab-flask-rest](https://github.com/nyu-devops/lab-flask-rest) for code examples to take from.

## Automatic Setup
The best way to use this repo is to start your own repo using it as a git template. To do this just press the green **Use this template** button in GitHub and this will become the source for your repository.

## Manual Setup
You can also clone this repository and then copy and paste the starter code into your project repo folder on your local computer. Be careful not to copy over your own README.md file so be selective in what you copy.

There are two hidden files that you will need to copy manually if you use the Finder to copy files from this folder into your repo folder. They are:

```bash
    cp .coveragerc ../<your_repo_folder>/
    cp .gitignore  ../<your_repo_folder>/
```

## Contents
The project contains the following:

```text
.coveragerc         - settings file for code coverage options
.devcontainers      - support for VSCode Remote Containers
.gitignore          - this will ignore vagrant and other metadata files
dot-env-example     - copy to .env to use environment variables
requirements.txt    - list if Python libraries required by your code
config.py           - configuration parameters

service/                - service python package
├── __init__.py         - package initializer
├── error_handlers.py   - HTTP error handling code
├── models.py           - module with business models
├── routes.py           - module with service routes
└── status.py           - HTTP status constants

tests/              - test cases package
├── __init__.py     - package initializer
├── test_models.py  - test suite for busines models
└── test_routes.py  - test suite for service routes

Vagrantfile         - sample Vagrant file that installs Python 3 and PostgreSQL
```

This repository is part of the NYU class **CSCI-GA.2810-001: DevOps and Agile Methodologies** taught by John Rofrano, Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science.


**Note:** This repo has a `Vagrantfile` so the easiest way to play with it is to:

```bash
vagrant up
vagrant ssh
cd /vagrant
nosetests
flask run -h 0.0.0.0
```

These are the RESTful routes for `shopcart` and `product`
```
Endpoint                     Methods  Rule
---------------------------  -------  -----------------------------------------------
index                        GET      /

list_shopcarts               GET      /shopcarts
create_shopcart              POST     /shopcarts
get_shopcarts                GET      /shopcarts/<customer_id>
update_cart                  PUT      /shopcarts/<customer_id>
delete_carts                 DELETE   /shopcarts/<customer_id>

list_products_in_shopcart    GET      /shopcarts/<int:customer_id>/products
create_products              POST     /shopcarts/<customer_id>/products
```

The test cases have 95% test coverage and can be run with `nosetests`
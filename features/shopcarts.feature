Feature: The shopcarts service back-end
    As a shopcarts manager
    I need a RESTful catalog service
    So that I can keep track of all products in shopcart

Background:
    Given the following shopcarts
        | shopcart |
        | 1        |
        | 2        |
        | 3        |

    Given the following products
        | customer_id | product_id | product_name | quantity | price  | instock | wishlist |
        | 1           | 9          | apple        | 3        | 2.0    | true    | false    |
        | 1           | 8          | orange       | 2        | 1.50   | true    | false    |
        | 2           | 7          | mouse        | 100      | 1500.0 | false   | true     |
        | 2           | 22         | keyboard     | 10       | 400.0  | true    | false    |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Shopcarts RESTful Service" in the title
    And I should not see "404 Not Found"


Scenario: Create a Shopcart
    When I visit the "Home Page"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "customer_id" field
    And I set the "product_id" to "123"
    And I set the "product_name" to "egg"
    And I set the "product_quantity" to "12"
    And I set the "product_price" to "3.99"
    And I select "False" in the "wishlist" dropdown
    And I select "True" in the "instock" dropdown
    And I press the "Update" button
    And I press the "Clear" button
    And I paste the "customer_id" field
    And I press the "Retrieve" button
    Then I should see "egg" in the search_results


Scenario: Retrieve a Customer's Wishlisted Products
    When I visit the "Home Page"
    And I set the "customer_id" to "2"
    And I press the "Retrieve-Wishlist" button
    Then I should see "mouse" in the wishlist results
    Then I should not see "apple" in the wishlist results

Scenario: Change a Product's Wishlist Status
    When I visit the "Home Page"
    And I set the "customer_id" to "1"
    And I set the "product_id" to "9"
    And I press the "Change-Wishlist" button
    Then I should see "True" in the "Wishlist" dropdown
    When I press the "Change-Wishlist" button
    Then I should see "False" in the "Wishlist" dropdown


# Scenario: List all pets
#     When I visit the "Home Page"
#     And I press the "Search" button
#     Then I should see "fido" in the results
#     And I should see "kitty" in the results
#     And I should not see "leo" in the results

# Scenario: Search all dogs
#     When I visit the "Home Page"
#     And I set the "Category" to "dog"
#     And I press the "Search" button
#     Then I should see "fido" in the results
#     And I should not see "kitty" in the results
#     And I should not see "leo" in the results

# Scenario: Update a Product in shopcart
#     When I visit the "Home Page"
#     And I press the "create" button
#     Then I should see ID in the "Customer ID" field
#     When I set the "Prouduct Name" to "egg"
#     And I set the "Quantity" to "1"
#     And I set the "Price" to "1.29"
#     And I set the "Instock" to "True"
#     And I set the "Wishlist" to "False"
#     And I press the "Update" button
#     Then I should see the message "Success"
#     When I set the "Prouduct Name" to "egg"
#     And I should see "egg" in the results
#     And I update the "Quantity" to "2"
#     And I set the "Instock" to "True"
#     And I set the "Wishlist" to "False"
#     And I press the "Update" button
#     Then I should see the message "Success"
#     And I should see "egg" "quantity" is "2" in the results

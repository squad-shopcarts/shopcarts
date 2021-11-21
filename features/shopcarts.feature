Feature: The shopcarts service back-end
    As a shopcarts manager
    I need a RESTful catalog service
    So that I can keep track of all products in shopcart 

Background:
    Given the following shopcarts
        |   shopcart  |
        |      1      |
        |      2      |
        |      3      |
    
    Given the following products
        | shopcart    | product_id | product_name | quantity | price | instock | wishlist  |
        |      0      | 9          |    apple     |    3     | 2.0   | true    | false     |
        |      1      | 8          |    orange    |    2     | 1.50  | true    | false     |
        |      2      | 7          |   mouse      |   100    | 1500.0| false   | true      |
        |      2      | 22         |   keyboard   |   10     | 400.0 | true    | false     |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Shopcarts RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Retrieve a Customer's Wishlisted Products
    When I visit the "Home Page"
    And I set the "customer_id" to "3"
    And I press the "Retrieve-Wishlist" button
    Then I should see "mouse" in the wishlist results
    And I should not see "keyboard" in the wishlist results

Scenario: Change a Product's Wishlist Status
    When I visit the "Home Page"
    And I set the "customer_id" to "1"
    And I set the "product_id" to "9"
    And I press the "Change-Wishlist" button
    Then I should see "True" in the "Wishlist" dropdown
    When I press the "Change-Wishlist" button
    Then I should see "False" in the "Wishlist" dropdown


# Scenario: Create a Pet
#     When I visit the "Home Page"
#     And I set the "Name" to "Happy"
#     And I set the "Category" to "Hippo"
#     And I select "False" in the "Available" dropdown
#     And I press the "Create" button
#     Then I should see the message "Success"
#     When I copy the "Id" field
#     And I press the "Clear" button
#     Then the "Id" field should be empty
#     And the "Name" field should be empty
#     And the "Category" field should be empty
#     When I paste the "Id" field
#     And I press the "Retrieve" button
#     Then I should see "Happy" in the "Name" field
#     And I should see "Hippo" in the "Category" field
#     And I should see "False" in the "Available" dropdown

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

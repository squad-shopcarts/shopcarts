"""
Test Factory to make fake objects for testing
"""
import factory
from factory.fuzzy import FuzzyChoice
from service.models import Product, Shopcart

class ProductFactory(factory.Factory):
    class Meta:
        model = Product
    
    id = 0
    #shopcart_id = factory.Sequence(lambda n: n)
    #product_id = factory.Sequence(lambda n: n)
    product_name = FuzzyChoice(choices=["apple", "banana", "peach"])
    #quantity = factory.Sequence(lambda n: n)
    #price  = factory.Sequence(lambda n: n)

    shopcart_id = 3
    product_id = 4
    quantity = 5
    price  = 6
    
    in_stock  = FuzzyChoice(choices=[True, False])
    wishlist = FuzzyChoice(choices=[True, False])

class ShopcartFactory(factory.Factory):
    class Meta:
        model = Shopcart

    customer_id = 0
    product_list = []
"""
Test Factory to make fake objects for testing
"""
import factory
from factory.fuzzy import FuzzyChoice
from service.models import Product, Shopcart

class ProductFactory(factory.Factory):
    class Meta:
        model = Product
    
    id = factory.Sequence(lambda n: n)
    shopcart_id = factory.Sequence(lambda n: n)
    product_id = factory.Sequence(lambda n: n)
    product_name = FuzzyChoice(choices=["apple", "banana", "peach"])
    quantity = factory.Sequence(lambda n: n)
    price  = factory.Sequence(lambda n: n)
    in_stock  = FuzzyChoice(choices=[True, False])
    wishlist = FuzzyChoice(choices=[True, False])

class ShopcartFactory(factory.Factory):
    class Meta:
        model = Shopcart

    customer_id = factory.Sequence(lambda n: n)
    product_list = []
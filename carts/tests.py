from django.test import TestCase
from models import Cart, Order

class cartModelTest(TestCase):
    def test_criacao_cart(self):
        cart = Cart.objects.create()

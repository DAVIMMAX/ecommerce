from django.test import TestCase
from carts.models import Cart, Order
from clientes.models import User
from produtos.models import Produto, Categoria
from django.db.utils import IntegrityError #testa a integridade de um teste basead

#<=---------------------------Testes para os Carrinhos------------------------------------>
class carinho_ModelTest(TestCase):
    def setUp(self): #Mais uma vez a classe que cria carrinhos necessita do precarregamento de um  usuário
        self.user = User.objects.create(email="user@user.com", password="123abc")

    def teste_criacao_cart(self): 
        cart = Cart.objects.create(user=self.user)
        self.assertEqual(cart.user, self.user)
    
    def teste_criacao_sem_user(self):
        with self.assertRaises(IntegrityError):
            Cart.objects.create(user=None)  

#<=---------------------------Testes para os Carrinhos------------------------------------>
class Ordem_Modelo_teste(TestCase):
    def setUp(self): #Pré-carregamento das classes necessárias
        self.user = User.objects.create(email="user@user.com", password="123abc")
        self.cart = Cart.objects.create(user=self.user)
        self.categoria = Categoria.objects.create(nome="Informática")
        self.product = Produto.objects.create(nome="Notebook", preco=3000.00, discount=5, categoria=self.categoria)
    def teste_criacao_compra(self): #Teste para criação de uma compra (ordem)
        order = Order.objects.create(product=self.product, cart=self.cart, quantity=2)
        self.assertEqual(order.product, self.product)
        self.assertEqual(order.cart, self.cart)
        self.assertEqual(order.quantity, 2)

#<------------------------------Testes de Inconsistências------------------------------------>

    def teste_compra_sem_carrinho(self): #testando se é possível fazer uma compra sem um carrinho.
        with self.assertRaises(IntegrityError):
            Order.objects.create(product=self.product, cart=None, quantity=5)
    
    def compra_em_quantidade_negativa(self): #vamos ver se o cliente poderá doar compras.
        with self.assertRaises(IntegrityError):
            Order.objects.create(product=self.product, cart=None, quantity=-5)
    
    def compra_zerada_quantidade_zerada(self): #testando se o cliente pode fazer uma compra com zero produtos
        with self.assertRaises(IntegrityError): #Nesse cenário, infelizmente, o resultado foi 
            Order.objects.create(product=self.product, cart=None, quantity=0)
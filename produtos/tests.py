from django.test import TestCase # Módulo padrão de testes
from django.utils import timezone #Necessário para comparações de tempo. 
from produtos.models import Produto, Categoria #Módulos que deverão ser testados
import time
from django.core.exceptions import ValidationError #Necessário nos testes de validação 


class CriarCategoriaTeste(TestCase):#testando a criação de uma nova categoria.
    def testar_criar_categoria(self):
        categoria = Categoria.objects.create(
            nome = "Petshop"
        )
        self.assertEqual(categoria.nome, "Petshop")
        

class CriarProdutoTeste(TestCase):
    def setUp(self): #Convenção do framework para testes, ele vai "setar" esse objeto para que as funções de teste referenciem o objeto criado aqui. 
        self.categoria = Categoria.objects.create(nome="Informática")# Por se tratar de 
    
    def teste_cria_produto(self):
        produto = Produto.objects.create(
            nome="Notebook",
            preco=3500.00,
            imagem="produtos/img/Notebook.jpg",
            categoria= self.categoria, #aqui, o correto deveria seria referenciar o objeto categoria na classe Categoria em categoria.py,
            #mas como o objetivo é fazer testes unitários, atribuimos um valor e pronto.
            discount=10
        )

        self.assertEqual(produto.nome, "Notebook") #Informa se o nome foi inserido;
        self.assertEqual(produto.preco, 3500.00) #informa se o preço foi digitado corretamente
        self.assertEqual(produto.categoria, Categoria.objects.filter(nome="Informática").first()) #self.categoria, coloquei a busca completa apenas para testar o ORM.
        self.assertEqual(produto.discount, 10) #Informa se o desconto foi inserido corretamente.
        self.assertEqual(produto.discounted_price(), 3150.00)#verifica se o valor retornado é o desconto correto.
        
        array = {produto.nome,produto.preco,produto.categoria,produto.discount,produto.discounted_price(),produto.criado_em}
        for a in array: #Sei que os testes passaram, mas é sempre bom conferir. também gostaria de verificar se realmente a função discounted_price estava correta.
            print(a)

#<-------------------------testando inserções incorretas de dados ----------------------------->

    def teste_cria_produto_preco_negativo(self):
        produto = Produto.objects.create(
            nome="Produto_teste",
            preco=-5000,
            imagem="produtos/img/Notebook.jpg",
            categoria= self.categoria, #aqui, o correto deveria seria referenciar o objeto categoria na classe Categoria em categoria.py,
            #mas como o objetivo é fazer testes unitários, atribuimos um valor e pronto.
            discount=10
        )

        with self.assertRaises(ValidationError):
            produto.full_clean() #O modelo deveria filtrar esse tipo de valor, 
            #o Lojista vai pagar pro cliente e ainda vai dar o notebook?

    def teste_data_criacao(self): #uma função importante do objeto, precisamos verificar se está sendo criado corretamente. 
        produto = Produto.objects.create(
            nome="Produto_teste",
            preco=3.500,
            imagem="produtos/img/Notebook.jpg",
            categoria= self.categoria, #aqui, o correto deveria seria referenciar o objeto categoria na classe Categoria em categoria.py,
            #mas como o objetivo é fazer testes unitários, atribuimos um valor e pronto.
            discount=10
        )

        time.sleep(1)
        agora = timezone.now() #um segundo para garantir uma margem de inserção no banco de dados e não ficarem datas e horas iguais
        delta = timezone.timedelta(seconds=5)  # +5 segundos de diferença para garantir
        self.assertTrue(produto.criado_em <= (agora + delta))
        
        print( produto.criado_em)

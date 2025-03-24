from django.test import TestCase
from .models.user import User
from django.db.utils import IntegrityError

#Para rodar os testes unitários: python manage.py test nomeDoApp.tests.UserModelTest.teste_criacao_usuario(ou outro).

#O Django cria os testes baseados 

class UserModelTest(TestCase): 
    def teste_criacao_usuario(self): #testando as funcionalidades de criação de usuários
        user = User.objects.create_user(email = "teste@email.com", password="123abc")
        self.assertEqual(user.email, "teste@email.com") #testando se a resposta de user.email sera teste#email.com
        self.assertTrue(user.check_password("123abc")) #testando se é verdadeiro que euser.check_passwort é senha123
        self.assertTrue(user.is_active) #responde se o usuário está ativo no sistema
        self.assertFalse(user.is_admin) #responmde se o usuário criado é administrador do sistema ou não.
        #Caso todos os testes automatizados sejam falso, obteremos um Ok no final.

class AdminUserModelTest(TestCase):
    def teste_criacao_admin(self):
        admin = User.objects.create_superuser(email= "admin@admin.com", password="123abc")# cria o modelo admin com email e senha
        self.assertEqual(admin.email, "admin@admin.com") #checa se o e-mail pertence ao administrador do sistema
        self.assertTrue(admin.is_admin) #checa se o usuário criado é ou não um admin
        self.assertTrue(admin.is_staff) #Mostra se o usuário criado é do tipo staff do sistema. 
# Create your tests here.

# <-----------------------------Testes de validação abaixo----------------------------------------->

class UsuarioEmBrancoTests(TestCase): #É acrescentado o valor ValueError dentro de assrtRaises para que o erro seja capturado se houver.
    def teste_criacao_usuario_email_em_branco(self):
        with self.assertRaises(ValueError): #Verificação com o campo e-mail não marcado.
            User.objects.create_user(email="", password="senha1234")
    def teste_criacao_usuario_senha_em_branco(self):
        with self.assertRaises(ValueError): #verificação com o campo senha não marcado.
            User.objects.create_user(email="admin@admin.com", password="")
            #Conforme podemos observar, o campo de senhas está retornando mensagens em branco. 

class EmailUnicoTest(TestCase):
    def teste_email_unico(self):
        User.objects.create_user("email@email.com", password="123abc")
        with self.assertRaises(IntegrityError):# Ao reinserir o mesmo email para outra conta, deve informar uma mensagem de erro.
            User.objects.create_user("email@email.com", password="abc123") #foi inserida uma senha diferente para teste.

class UsuarioGeneroVedadeiroTeste(TestCase):
    def tesando_genero_valido_m(self):
        user = User.objects.create_user(email="teste@teste.com", password="123abc")
        user.gender = 'm'
        user.save()
        self.assertEqual(user.gender, 'm')
    def testando_genero_valido_f(self):
        user = User.objects.create_user(email="teste@teste.com", password="123abc")
        user.gender = 'f'
        user.save()
        self.assertEqual(user.gender, 'f')

class UsuarioGeneroFalsoTeste(TestCase):
     def testando_genero_invalido_x(self):
         user = User.objects.create_user(email="teste@teste.com", password="123abc")
         with self.assertRaises(ValueError):
             user.gender = 'x' #Não existe o valor x nas opções de campo válido. 
             user.save()#Essa opção retornaria um erro pois não foi implementada ainda. 
    #O banco de dados, mesmo com a implementação, está aceitando generos não catalogados.
    #Foi proposital para demonstrar que o modelo necessita de uma validação no método save.


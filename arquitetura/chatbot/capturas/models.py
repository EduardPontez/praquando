from django.db import models

# Create your models here.
class Captura(models.Model):

    code = models.CharField(max_Length = 15)
    #CharField - tipo de campo do SQLite através de classe Python

    code_user = models.CharField(max_Length = 15)
    #Código do usuário pois cada um deles terá sua própria página de capturas
    # Relacionar aplicativo de perguntas com usuários cadastrados
    
    active = models.IntegerField()
    """Se o usuário estiver ativo, recebe 1, caso contrário recebe 0, impossibilitando
        usuários inativos a acessarem recursos da aplicação.
        Este campo estará em todas as tabelas que tiverem interação com o usuário
    """

    name = models.CharField(max_Length = 100)
    age = models.IntegerField()
    sex = models.CharField(max_Length = 10)
    email = models.CharField(max_Length = 100)
    cellphone = models.CharField(max_Length = 15) #telefone celular
    phone = models.CharField(max_Length = 10) #telefone fixo
    cep = models.CharField(max_Length = 10) #cep - exemplo: 04538-133
    state = models.CharField(max_Length = 50) #estado
    city = models.CharField(max_Length = 100) #cidade
    neighborhood = models.CharField(max_Length = 100) #bairro
    address = models.CharField(max_Length = 200) #endereço
    number = models.CharField(max_Length = 5)
    cpf = models.CharField(max_Length = 15) #cpf - exemplo 542.458.414-43
    cnpj = models.CharField(max_Length = 15) #cnpj - exemplo: 76.255.668/0001-41
     
    #Serão capturados durante a interação com o usuário
    '''E-mail é a captura mais importante pois pode ser usado para entrar em contato com o 
       usuário e pedir as informações faltantes posteriormente
    '''

    def __str__(self):
        return self.code
    #definir campo que será exibido na tela administrativa para selecionar dados da tabela

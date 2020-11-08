from django.db import models

# Create your models here.
class Pergunta(models.Model):
    code = models.CharField(max_length = 15)
    code_user = models.CharField(max_length = 15)
    active = models.IntegerField()
    
    code_relation = models.CharField(max_length = 15)
    '''
    Campo irá relacionar uma resposta atual com uma pergunta 
    anterior para alterar o fluxo do ChatBot
    '''

    question = models.CharField(max_length = 500)
    
    answer = models.CharField(max_length = 500)
    #retorno do ChatNot
    
    def __str__(self):
        return self.question
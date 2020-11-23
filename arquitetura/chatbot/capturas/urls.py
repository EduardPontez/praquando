from django.urls import path, include
from .views import capturas

urlpatterns = [
	path('<int:code_user>/', capturas) #Definindo código do usuário como rota de acesso
	]
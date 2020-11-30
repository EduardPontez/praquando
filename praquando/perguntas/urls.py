from django.urls import path
from .views import perguntas, pergunta, novo, salvarNovo, edicao, salvarEdicao, delecao, salvarDelecao, chatbot, questao, api

# perguntas - consulta por todas as perguntas
# pergunta - consultas individualmente

# novo - carregar página para novo cadastro
#salvarNovo - executar rotina de cadastrar no banco (tipo POST)

# edicao - carregar página para edição
# SalvarEdicao - executar rotina para salvar no banco

# delecao - carregar página para deleção 
# salvarDelecao - executart deleção no banco

# chatbot - carregar a tela do chatbot
# questao - interação com o usuário
# api - carregar a tela de integração do chatbot a sites e sistemas de terceiros

urlpatterns = [

	path('<int:code_user>/', perguntas),
	path('pergunta/<int:id>/', pergunta),
	path('novo/<int:code_user>/', novo),
	path('salvarNovo/', salvarNovo),
	path('edicao/<int:id>/', edicao),
	path('salvarEdicao/', salvarEdicao),
	path('delecao/<int:id>/', delecao),
	path('salvarDelecao/', salvarDelecao),
	path('chatbot/<int:code_user>/', chatbot),
	path('questao/<int:code_user>/<int:code_before>/<str:question>/', questao),
	path('api/<int:code_user>/', api)

	#Paths sem parâmetros serão capturados via POST
	#Path é inteligente o sificiente no Django para diferenciar POST de GET
]
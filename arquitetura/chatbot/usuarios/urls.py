from django.urls import path
from .views import login, entrar, usuarios, usuario, novo, salvarNovo, edicao, salvarEdicao, delecao, salvarDelecao

#login - carregar a tela de login
#entrar - acionar as rotinas da tela de login
#usuarios - carregar a tela de usuários
#usuario - selecionar apenas um usuário

# novo - carregar página para novo cadastro
#salvarNovo - executar rotina de cadastrar no banco (tipo POST)

# edicao - carregar página para edição
# SalvarEdicao - executar rotina para salvar no banco

# delecao - carregar página para deleção 
# salvarDelecao - executart deleção no banco


urlpatterns = [

	path('login/', login),
	path('entrar/', entrar),
	path('', usuarios),
	path('usuario/<int:code>/', usuario),
	path('novo/', novo),
	path('salvarNovo/', perguntas),
	path('edicao/<int:id>/', edicao),
	path('salvarEdicao/', salvarEdicao),
	path('delecao/<int:id>/', delecao),
	path('salvarDelecao/', salvarDelecao),

	#Paths sem parâmetros serão capturados via POST
	#Path é inteligente o sificiente no Django para diferenciar POST de GET
]
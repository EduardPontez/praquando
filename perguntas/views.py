from django.shortcuts import render
from .models import Pergunta
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from unidecode import unidecode
from usuarios.models import Usuario

codeUser = 0

# Create your views here.
def perguntas(request, code_user):
	titulo = 'Cadastro de Perguntas e Respostas'
	pergunta = Pergunta.objects.filter(code_user = code_user)
	usuario = Usuario.objects.filter(code = code_user)
	
	if len(usuario) > 0:
		global codeUser
		codeUser = code_user
		return render(request, 'perguntas.html', 
					 {'titulo' : titulo, 'perguntas' : pergunta, 'code_user' : code_user})
	else:
		return render(request, 'redirecionar.html', {'code_user' : 0})



def pergunta(request, id):
	titulo = 'Cadastro de Perguntas e Respostas'
	base_url = request.scheme + "://" + request.get_host()
	pergunta = Pergunta.objects.get(id = id)

	global codeUser
	usuario = Usuario.objects.filter(code = codeUser)

	if len(usuario) > 0:
		
		return render(request, 'perguntas.html',
					 {'titulo' : titulo, 'perguntas' : [pergunta], 'code_user' : codeUser, 'url' : base_url})
	else:
		return render(request, 'redirecionar.html', {'code_user' : 0})

def novo(request, code_user):
	titulo = 'Inserção de Perguntas e Respostas'
	base_url = request.scheme + "://" + request.get_host()
	todas = Pergunta.objects.filter(code_user = code_user)
	usuario = Usuario.objects.filter(code = code_user)
	
	if len(usuario) > 0:

		return render(request, 'novoPerguntas.html', 
		        	 {'titulo' : titulo, 'code_user' : code_user, 'todas' : todas, 'url' : base_url})
	
	else:
		return render(request, 'redirecionar.html', {'code_user' : 0})


def getCODE():
	from datetime import datetime
	dataHora = datetime.now()
	code = str(dataHora.year)
	code += str(dataHora.month)
	code += str(dataHora.day)
	code += str(dataHora.hour)
	code += str(dataHora.minute)
	code += str(dataHora.second)
	code = str(int(round(int(code)/2, 0)))

	return code

@csrf_protect
def salvarNovo(request):
	code = getCODE()
	code_user = request.POST.get("code_user")
	active = 1
	code_relation = request.POST.get("code_relation")
	question = request.POST.get("question")
	answer = request.POST.get("answer")

	p = Pergunta(
		code = code,
		code_user = code_user,
		active = active,
		code_relation = code_relation,
		question = question,
		answer = answer
	)

	p.save()
	return render(request, 'redirecionar.html', {'code_user' : code_user})


def edicao(request, id):
	titulo = 'Edição de Perguntas e Respostas'
	global codeUser
	todas = Pergunta.objects.filter(code_user = codeUser)
	base_url = request.scheme + "://" + request.get_host()
	pergunta = Pergunta.objects.get(id = id)
	usuario = Usuario.objects.filter(code = codeUser)
	
	if len(usuario) > 0:
		return render(request, 'edicaoPerguntas.html', 
		         	 {'titulo' : titulo, 'perguntas' : pergunta, 'todas' : todas, 'code_user' : codeUser, 'url' : base_url})
	else:
		return render(request, 'redirecionar.html', {'code_user' : 0})

@csrf_protect
def salvarEdicao(request):
	id = int(request.POST.get("id"))
	code_user = request.POST.get("code_user")
	code_relation = request.POST.get("code_relation")
	question = request.POST.get("question")
	answer = request.POST.get("answer")

	Pergunta.objects.filter(id=id).update(

		code_user = code_user,
		code_relation = code_relation,
		question = question,
		answer = answer
	)

	return render(request, 'redirecionar.html', {'code_user' : code_user})


def delecao(request, id):
	titulo = 'Deleção de Perguntas e Respostas'
	global codeUser
	base_url = request.scheme + "://" + request.get_host()
	todas = Pergunta.objects.filter(code_user = codeUser)
	pergunta = Pergunta.objects.get(id = id)
	usuario = Usuario.objects.filter(code = codeUser)
	
	if len(usuario) > 0:
		return render(request, 'delecaoPerguntas.html', 
	         	 	 {'titulo' : titulo, 'perguntas' : pergunta, 'todas' : todas, 'code_user' : codeUser, 'url' : base_url})
	else:
		return render(request, 'redirecionar.html', {'code_user' : 0})


@csrf_protect
def salvarDelecao(request):
	id = int(request.POST.get("id"))
	code_user = request.POST.get("code_user")
	Pergunta.objects.filter(id = id).delete()

	return render(request, 'redirecionar.html', {'code_user' : code_user})


def chatbot(request, code_user):
	titulo = 'Chatbot'
	usuario = Usuario.objects.get(code = code_user)

	if usuario:
		exibicao = usuario.name
		exibicao = exibicao.split(' ', 1)[0]
		return render(request, 'chatbot.html', 
					 {'titulo' : titulo, 'code_user' : code_user, 'usuario' : exibicao})
	else:
		return render(request, 'redirecionar.html', {'code_user' : 0})

# nlp - processamento de linguagem natural
def questao(request, code_user, code_before, question):
	
	question = question.replace('%20', ' ')
	qTemp = question.lower()
	
	if code_before > 0:

		consulta = Pergunta.objects.filter(code_user = code_user, code_relation = code_before, active=1)
		
		if len(consulta) <= 0:
			consulta = Pergunta.objects.filter(code_user = code_user, active = 1)
		
	else:
		consulta = Pergunta.objects.filter(code_user = code_user, active = 1)

	lista = list()

	# controle de abreviações
	qTemp = qTemp.replace('vc', 'voce')
	qTemp = qTemp.replace('vcs', 'voces')
	qTemp = qTemp.replace('eh', 'e')
	qTemp = qTemp.replace('tb', 'tambem')
	qTemp = qTemp.replace('tbm', 'tambem')
	qTemp = qTemp.replace('oq', 'o que')
	qTemp = qTemp.replace('dq', 'de que')
	qTemp = qTemp.replace('td', 'tudo')
	qTemp = qTemp.replace('pq', 'por que')
	qTemp = qTemp.replace('qm', 'quem')
	qTemp = qTemp.replace('qd', 'quando')
	qTemp = qTemp.replace('p', 'para')
	qTemp = qTemp.replace('mto', 'muito')
	qTemp = qTemp.replace('fas', 'faz')

	# cria uma lista com query da consulta
	if len(consulta) <= 0:
		lista.append({
			'code_current' : 0,
			'code_user' : code_user,
			'code_before' : code_before,
			'question' : question,
			'input' : question,
			'output':'Desculpe, mas não sei informar.'

		})
	else:
		for x in consulta:
			lista.append({
				'code_current' : x.code,
				'code_user' : x.code_user,
				'code_before' : code_before,
				'question' : x.question,
				'input' : question,
				'output' : x.answer
			})
				
	# remove acentuação e espaços
	questao_recebida = unidecode(question)
	questao_recebida.replace('?', '')
	questao_recebida.replace('!', '')
	questao_recebida.replace('-', '')
	questao_recebida = questao_recebida.strip()

	# coloca em minúsculas
	questao_recebida = questao_recebida.lower()

	#elimina as três últimas letras de cada palavra com tokenização
	templ = questao_recebida.split(' ')
	temp2 = list()

	for x in templ:
		if len(x) > 3:
			temp2.append(x[0:len(x)-3])
		else:
			temp2.append(x)

	questao_recebida = ' '.join(temp2)

	# percorre a lista de registros encontrados
	iguais = 0
	code = ''

	for x in lista:
		# remove acentuação e espaços
		questao_encontrada = unidecode(x['question'])
		questao_encontrada.replace('?', '')
		questao_encontrada.replace('!', '')
		questao_encontrada.replace('-', '')
		questao_encontrada = questao_encontrada.strip()

		# coloca em minúsculas
		questao_encontrada = questao_encontrada.lower()

		#elimina as três últimas letras de cada palavra com tokenização
		temp3 = questao_encontrada.split(' ')

		temp4 = list()

		for y in temp3:
			if len(y) > 3:
				temp4.append(y[0:len(y)-3])
			else:
				temp4.append(y)

		questao_encontrada = ' '.join(temp4)

		#cria uma lista para a questão recebida e uma para a questão encontrada
		qrList = questao_recebida.split(' ')
		qeList = questao_encontrada.split(' ')
		
		#removendo último caractere do útimo elemento da lista de questão encontrada
		if len(qeList[-1]) > 3: 
			qeList[-1] = qeList[-1][:-1]
		
		#consta as palavras recebidas que coincidem com as palavras de cada questão encontrada
		qtd = 0

		for y in qrList:
			if y in qeList:
				qtd += 1

		if len(qrList) >= len(qeList):
		  percent = qtd*100//len(qrList)
		else:
		  percent = qtd*100//len(qeList)

		if percent >= iguais:
			iguais = percent
			code = x['code_current']

	if(iguais == 0):
		update = {}
		update = {'output':'Desculpe, mas não sei informar.'}
		lista = [{**d,**update} for d in lista]
		
	# deixa na lista somente a resposta correspondente
	correspondente = list()
	for x in lista:
		if code == x['code_current']:
			correspondente.append(x)
			break
	lista = correspondente

	return JsonResponse(lista, safe=False) 


def api(request, code_user):
	titulo = 'API de Integração'
	base_url = request.scheme + "://" + request.get_host()
	usuario = Usuario.objects.filter(code = code_user)
	
	if len(usuario) > 0:
		return render(request, 'api.html', {'titulo' : titulo, 'code_user' : code_user, 'url' : base_url})
	else: 
		return render(request, 'redirecionar.html', {'code_user' : 0})
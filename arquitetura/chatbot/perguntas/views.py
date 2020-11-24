from django.shortcuts import render
from .models import Pergunta
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from unidecode import unidecode
from capturas.models import Captura

codeUser = 0

# Create your views here.
def perguntas(request, code_user):
	titulo = 'Cadastro de Perguntas e Respostas'
	pergunta = Pergunta.objects.filter(code_user = code_user)
	global codeUser
	codeUser = code_user
	return render(request, 'perguntas.html', 
				 {'titulo' : titulo, 'perguntas' : pergunta, 'code_user' : code_user})


def pergunta(request, id):
	titulo = 'Cadastro de Perguntas e Respostas'
	pergunta = Pergunta.objects.get(id = id)
	global codeUser
	return render(request, 'perguntas.html',
				 {'titulo' : titulo, 'perguntas' : [pergunta], 'code_user' : codeUser})

def novo(request, code_user):
	titulo = 'Inserção de Perguntas e Respostas'
	todas = Pergunta.objects.filter(code_user = code_user)
	return render(request, 'novoPerguntas.html', 
		         {'titulo' : titulo, 'code_user' : code_user, 'todas' : todas})


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
	todas = Pergunta.objects.filter(code_user = code_user)
	pergunta = Pergunta.objects.get(id = id)
	return render(request, 'edicaoPerguntas.html', 
		         {'titulo' : titulo, 'perguntas' : pergunta, 'todas' : todas, 'code_user' : codeUser})


@csrf_protect
def salvarEdicao(request):
	id = int(request.POST.get("id"))
	code_user = request.POST.get("code_user")
	code_relation = request.POST.get("code_relation")
	question = request.POST.get("question")
	answer = request.POST.get("answer")

	Pergunta.objects.filter(id=id).update(
		code = code,
		code_user = code_user,
		active = active,
		code_relation = code_relation,
		question = question,
		answer = answer
	)

	return render(request, 'redirecionar.html', {'code_user' : code_user})


def delecao(request, id):
	titulo = 'Deleção de Perguntas e Respostas'
	global codeUser
	todas = Pergunta.objects.filter(code_user = code_user)
	pergunta = Pergunta.objects.get(id = id)
	return render(request, 'delecaoPerguntas.html', 
	         	 {'titulo' : titulo, 'perguntas' : pergunta, 'todas' : todas, 'code_user' : codeUser})

@csrf_protect
def salvarDelecao(request):
	id = int(request.POST.get("id"))
	code_user = request.POST.get("code_user")
	Pergunta.objects.filter(id = id).delete()

	return render(request, 'redirecionar.html', {'code_user' : code_user})


def chatbot(request, code_user):
	titulo = 'Chatbot'
	return render(request, 'chatbot.html', 
				 {'titulo' : titulo, 'code_user' : code_user})




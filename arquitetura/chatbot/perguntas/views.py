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

# nlp - processamento de linguagem natural
def question(request, code_user, code_before, question):
	question = question.replace('%20', ' ')
	qTemp = question.lower()
	if code_before > 0:
		consulta = Pergunta.objects.filter(code_user = code_user, code_relation = code_before, active=1)
		if len(consulta) <= 0:
			consulta - Pergunta.objects.filter(code_user = code_user, active = 1)
		else:
			consulta = Pergunta.objects.filter(code_user = code_user, active = 1)

		# capturas de informação
		# idade
		import re
		if 'anos' in qTemp:
			idade = qTemp[qTemp.index('anos')-8:qTemp.index(anos)]
			idade = int(re.sub('[^0-9]', '', idade))
		else:
			tokens = qTemp.split(' ')
			for token in tokens:
				parts = res.sub('[^0-9]', '', token)
				if len(parts) >= 1 and len(parts) <=3:
					idade = int(parts)

		# sexo
		sexo = ''
		_qTemp = qTemp.replace(',', '').replace('.', '').replace(';', '').replace('!', '')
		if ' m ' in _qTemp or 'masculino' in _qTemp:
			sexo = 'M'
		elif ' f ' in _qTemp or 'feminino' in _qTemp:
			sexo = 'F'

		# email
		#tokenização
		email = ''
		tokens = qTemp.split(' ')
		for token in tokens:
			if '@' in token and '.' in token:
				email = token.strip()
				if email[-1] == '.':
					email = email[0:-1]
				email = email.replace(',', '').replace(';', '').replace('!', '')

				# nome
				emailList = email.split('@')
				nome = emailList[0]

		# cpf
		cpf = ''
		tokens = qTemp.split(' ')
		for token in tokens:
			parts = re.sub('[^0-9]', '', token)
			if len(parts) == 11:
				from validate_docbr import CPF
				objCPF = CPF()
				if objCPF.validate(parts):
					cpf = parts.strip()

		# cnpj
		cnpj = ''
		tokens = qTemp.split(' ')
		for token in tokens:
			parts = re.sub('[^0-9]', '', token)
			if len(parts) == 11:
				from validate_docbr import CNPJ
				objCNPJ = CNPJ()
				if objCNPJ.validate(parts):
					cnpj = parts.strip()


		# telefone celular
		celular = ''
		tokens = qTemp.split('')

		for token in tokens:
			parts = re.sub('[^0-9]', '', token)
			if parts != cpf:
				if '9' in parts:
					if len(parts) == 13 or len(parts) == 11 or len(parts) == 9:
						celular = parts.strip()

		# localidade
		# cep
		cep = ''
		endereco = ''
		bairro = ''
		numero = ''
		estado = ''
		cidade = ''
		tokens = qTemp.split(' ')
		import buscacep
		for token in tokens:
			parts = re.sub('[^0-9]', '', token)
			if len(parts == 8):
				try:
					res = buscacep.busca_cep_correios(parts)
				except:
					res = False
				if res != False:
					cep = parts.strip()
					estado = res.localidade[res.localidade.index('/'):].replace('/', '').strip()
					cidade = res.localidade[:res.localidade.index('/')].strip()
					bairro = res.bairro.strip()
					endereco = res.logradouro.strip()
					numero = re.sub('[^0-9]', '', res.logradouro)
		

		# telefone fixo
		telefone = ''
		tokens = qTemp.split(' ')
		for token in tokens:
			parts = re.sub('[^0-9]', '', token)
			if parts != cep:
				if len(parts) == 12 or len(parts) == 10 or len(parts) == 8:
					telefone = parts.strip()

		# inserção de resultados da captura

		lista = list()
		if len(email) > 0 or len(celular) > 0 or len(telefone) > 0 or len(cep) > 0 or len(cpf) > 0 or len(cnpj) > 0:
			code = getCODE()
			global codeUser
			code_user = codeUser
			active = 1

			captura = Captura(
				code = code,
				code_user = code_user,
				active = active,
				name = nome.upper(),
				age = idade,
				sex = sexo.upper(),
				email = email,
				cellphone = celular,
				phone = telefone,
				cep = cep,
				state = estado.upper(),
				city = cidade.upper(),
				neighborhood = bairro.upper(),
				address = endereco.upper(),
				number = numero.upper(),
				cpf = cpf,
				cnpj = cnpj
			)

			captura.save()
			lista.append({
				'code_current' : 0,
				'code_user' : code_user,
				'code_before' : code_before,
				'question' : question,
				'input' : question,
				'output' : 'Ok, entendi'
				})
		else:
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

			# cria uma lista com query da consulta
			if len(consulta) <= 0:
				lista.append({
					'code_current' : 0,
					'code_user' : code_user,
					'code_before' : code_before,
					'question' : question,
					'input' : question,
					'output' : 'Desculpe, mas não sei informar.'
				})
			else:
				for x in consulta:
					lista.append({
						'code_current' : x.code,
						'code_user' : x.code_user,
						'code_before' : x.code_before,
						'question' : x.question,
						'input' : question,
						'output' : x.answer
					})

			# remove acentuação e espaços
			questao_recebida = unidecode(question)
			questao_recebida.replace('?', '')
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
				questao_recebida.replace('?', '')
				questao_encontrada.questao_encontrada.strip()

				# coloca em minúsculas
				questao_encontrada = questao_encontrada.lower()

				#elimina as três últimas letras de cada palavra com tokenização
				templ = questao_recebida.split(' ')
				temp2 = list()

				for y in templ:
					if len(y) > 3:
						temp2.append(x[0:len(y)-3])
					else:
						temp2.append(y)

				questao_encontrada = ' '.join(temp2)

				#cria uma lista para a questão recebida e uma para a questão encontrada
				qrList = questao_recebida.split(' ')
				qeList = questao_encontrada.split(' ')

				#consta as palavras recebidas que coincidem com as palavras de cada questão encontrada
				qtd = 0

				for y in qrList:
					if y in qeList:
						qtd += 1

				if qtd >= iguais:
					iguais = qtd
					code = x['code_current']

			# deixa na lista somente a resposta correspondente
			correspondente = List()
			for x in lista:
				if code == x['code_current']:
					correspondente.append(x)
					break
			lista = correspondente

		return JsonResponse(lista, safe=False) 
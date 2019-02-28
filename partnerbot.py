from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json 
import os
import requests
from webexteamssdk import WebexTeamsAPI



# CHAT BOT v3.0.0
# Integracao Cisco Operations Insights & Webex Teams & CMX
# (c) 2019 
# Flavio Correa
# Joao Peixoto
# Sergio Polizer
# Daniel Vicentini

#########################################################
## VAR FIXAS

# infobot
api = WebexTeamsAPI(access_token='YTg5YjMwODMtYjliMS00YjM3LTlmMjYtNzlhZWU1MDE0NDlhODIwYzMwODctZDVj_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f')

# Webhook
webhook_url="https://partnerbotbr.herokuapp.com"
webhook_name="partnerbotbr"
botmail="partnerbotbr@webex.bot"

#########################################################
## FUNCOES


def CriaWebhook(webhook_name,webhook_url):


	# Cria Webhook para receber msg via POST
    # Avisa Teams para gerar hooks para mensagems criadas somente

	# Webhook para msgs
    api.webhooks.create(webhook_name,webhook_url,"messages","created")
	# Webhook para nova sala criada - boas vindas
    api.webhooks.create(webhook_name+"-new",webhook_url,"rooms","created")
	
    return

def webexME():
	# detalhes sobre mim
	data = api.people.me()
	return data

def WebexRoomCreate(name):

	# Cria Sala Webex e retorna ID da sala, name aqui e' o nome da Sala
	api.rooms.create(name)

	# Encontra roomID da sala para devolver
	novasala = getwebexRoomID(name)

	return novasala

def WebexRoomDel(id):

	#Remove sala Webex,id aqui e' roomID 
	api.rooms.delete(id)

	return

def WebexIncUser(sala,mail):

	#Inclui usuario como membro da sala, criando sala caso nao exista
    # Descobri roomID da sala (sala e' o nome completo ou parte dela)
	salaaincluir=getwebexRoomID(sala)

	# Cria sala caso esta nao exista
	if salaaincluir == None:
		salaaincluir = WebexRoomCreate(sala)

	useraincluir=getwebexUserID(mail)

	# inclui usuario caso id encontrado
	if useraincluir !=None:
			#executa a operacao
			api.memberships.create(salaaincluir,useraincluir)

	return

def webexUser(mail):
	# pesquisa ID do usuário e retorna MSG
	usuario = api.people.list(email=mail)
	user=None

	for inter in usuario:
		user = inter.id

	if user !=None:
		resultado = "Usuario "+str(mail)+" ID e' "+user
	else:
		resultado = "Nenhum Usuario encontrado para "+str(mail)

	return resultado

def getwebexUserID(mail):
	# pesquisa ID do usuário; retorna vazio se nao encontrado
	usuario = api.people.list(email=mail)
	user=None

	for x in usuario:
		user = x.id

	if user !=None:
		resultado = user
	
	return resultado


def webexRoomsList():
	# lista salas que pertenco
	rooms=api.rooms.list()
	resultado = ""

	for room in rooms:
		resultado = resultado + "Sala " + str(room.title) + " ID: " + str(room.id)+ "\n"

	return resultado



def getwebexRoomID(sala):

	# Retorna ID da Sala; retorna vazio se nao encontrado
    # O parametro sala e' todo ou parte do nome da sala procurada
	# Salas que pertenco
	rooms=api.rooms.list()
	salawebex = None

	# for para encontrar ID da sala determinada

	for room in rooms:
		if sala in room.title:
	  		salawebex = room
	  		break

			
	# mandando uma mensagem para a Sala caso encontrada:s
	if salawebex != None:
		resultado = (str(salawebex.id))
	else:
		resultado = salawebex
		
	return resultado

def getwebexMsg(msgID):
	
    # msgID é o parametro resgatado do corpo do webhook
	# Retorna lista com o [0]texto da mensagem informada [1]ID da sala e [2]email da pessoa
	mensagem=api.messages.get(msgID)
				
	return mensagem.text,mensagem.roomId,mensagem.personEmail

def webexmsgRoom(sala,msg):

	# Manda msg para 1 sala especifica, procurando salas onde estou (usando partes do nome informado em sala)
	rooms=api.rooms.list()
	salawebex = None

	salawebex = getwebexRoomID(sala)
			
	# mandando uma mensagem para a Sala caso encontrada:
	if salawebex != None:
		api.messages.create(salawebex,None,None,msg)

	return

def webexmsgRoomviaID(sala,msg):

	# Manda msg para 1 sala especifica informada via sala=roomID, 
	api.messages.create(sala,None,None,msg)

	return

def webexmsgAll(msg):
	# mensagem em todas as salas que estou
	#
	rooms=api.rooms.list()

	for room in rooms:
		api.messages.create(room.id,None,None,msg)
	
	return



def webextalk(msg_id):

    # Camada de interação com o usuário conversando com o BOT

    # chama funcao para resgatar detalhes da mensagem (via id)
    dados = getwebexMsg(msg_id)
    # armazena o texto da msg enviada pelo usuario 
    # box e' o que o user escreveu
    box=dados[0]
    box.lower()
    # armazena o id sala usada para devolver para mesma
    idsala=dados[1]
    # armazena email de quem enviou - nao utilizado ainda
    usermail=dados[2]

    # Para o caso de nenhum pedido coberto aqui
    mais="Escreva 'mais' para saber suas opções"
    
    msg=""

    # Splita para encontrar detalhes dos parametros
    sp=box.split(" ")
    box=sp[0]
	

    # chamadas de acordo com os parametros
	
    if box == "mais" and len(sp)<2:
        msg="Descubra sobre nossas principais ferramentas para ajudá-lo. Escreva:\n"
        msg=msg+"mais sobre Cliente: conheça nosso programa semanal Quint@s Quinze\n"
        msg=msg+"mais sobre Demos: nossas ferramentas de demonstração\n"
        msg=msg+"mais sobre Projetos: nossa ferramenta para ajudar no desenvolvimento de projetos\n"
        msg=msg+"mais sobre Treinamento: nossas ferramentas e programação de capacitação\n"
        msg=msg+"mais sobre Suporte: Abertura de Chamados no Cisco TAC\n"
        msg=msg+"mais sobre Alertas: assine nossas newsletter de Produtos\n"


    if len(sp)>2:
        tema=sp[2]
        if tema!="" and "cliente" in tema:
            msg="Participe Regularmente de nossas atualizações de soluções para Cliente.\n"
            msg=msg+"Acesse nossa agenda: http://www.cisco.com/c/pt_br/about/events-schedule/quintas-quinze.html\n"
            msg=msg+"O Quint@s Quinze é transmitido on-line. Se inscreva e participe"	
        
        if tema!="" and "demo" in tema:
            msg="Conheça, aprenda e demonstre todas as soluções Cisco on-line\n"
            msg=msg+"Nossos produtos podem ser testados e acessados usando a nuvem da Cisco.\n"
            msg=msg+"Conheça http://dcloud.cisco.com\n"
            msg=msg+"Produtos Cisco Small Business http://www.cisco.com/go/emulators\n"
        
        if tema!="" and "projeto" in tema:
            msg="Precisa de ajuda para desenvolvimento de projetos? Nosso time virtual Partner Help Line é o canal para\n"
            msg=msg+"ajudá-lo no desenvolvimento do seu projeto, incluindo:\n"
            msg=msg+"-Dúvidas sobre produtos e funcionalidades\n"
            msg=msg+"-Construção da lista de materiais para compra\n"
            msg=msg+"-Apresentações remotas do portifólio Cisco para seus clientes\n"
            msg=msg+"\nComeçe por aqui:http://www.cisco.com/c/en/us/partners/support-help/presales-helpline.html\n"

        if tema!="" and "trein" in tema:
           msg="A Cisco disponibiliza para você Engenheirou ou Vendedor uma plataforma de treinamento on-line.\n"
           msg=msg+"No Partner Academy você encontra treinamentos EAD Cisco para todas as nossas soluções:\n"
           msg=msg+"https://salesconnect.cisco.com/#/program/PAGE-13518\n"

        if tema!="" and "suporte" in tema:
           msg="Desafios no uso dos produtos Cisco instalados? Contate nosso TAC\n"
           msg=msg+"Cisco Technical Assistance Center: http://www.cisco.com/c/pt_br/support/index.html\n"
        
        if tema!="" and "alert" in tema:
           msg="Nosso serviço de alertas avisa você diariamente sobre produtos entrando em Fim de Linha,\n"
           msg=msg+"Produtos com problemas de software conhecido e as últimas novidade a respeito de segurança\n"
           msg=msg+"dos produtos Cisco. Mantenha-se informado: http://www.cisco.com/cisco/support/notifications.html\n"

    msg=msg+mais        

    # apos montagem da resposta em msg, envia a respectiva sala teams:
    webexmsgRoomviaID(idsala,msg)

    return

#########################################################
## LOGICA COMECA AQUI

# inicia programa
# Site

# Valida existencia de webhook
webhookok=0
webhook=api.webhooks.list()
for b in webhook:
	 if b.name==webhook_name:
		 webhookok=1
# Webhook nao encontrado. Cria novos.
if webhookok==0:
	CriaWebhook(webhook_name,webhook_url)

# http server
class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    # POST valida se o que chega sem dados via o Webhook
    # do POST e' que se chama a rotina de respnder ao usuario

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n", str(self.path), str(self.headers), post_data.decode('utf-8'))
        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

        # Conteudo
        content=json.loads(post_data.decode('utf-8'))
		

		# resposta as perguntas
        if content['name']==webhook_name and content['data']['personEmail']!=botmail:
            # identifica id da mensagem
            msg_id=(content['data']['id'])
            # executa a logica conforme o pedido (interacao)
            webextalk(msg_id)

	
def run(server_class=HTTPServer, handler_class=S, port=int(os.getenv('PORT',8080))):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
        
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')



"""
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""


if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:	
        run()
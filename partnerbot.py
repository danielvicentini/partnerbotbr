from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json 
import os
import requests
from webexteamssdk import WebexTeamsAPI

#########################################################
## VAR FIXAS

# Ponha aqui os dados do seu robozinho
bottoken='YTg5YjMwODMtYjliMS00YjM3LTlmMjYtNzlhZWU1MDE0NDlhODIwYzMwODctZDVj_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f'
botmail="partnerbotbr@webex.bot"

api = WebexTeamsAPI(access_token=bottoken)

# Ponha aqui os dados do seu Webhook
# webhook_url o endereço publico onde está o app
webhook_url="https://partnerbotbr.herokuapp.com"
# webhook_name e' o nome do gatilho que o Webex Teams gera para seu aplicativo entender
webhook_name="partnerbotbr"

#########################################################
## FUNCOES WEBEX TEAMS

#########################################################
## Sessão webhook

def ValidaWebhook(webhook_name,webhook_url):

	# Valida existencia de webhook, na ausencia cria novo
    # Retorna sucesso ou erro na operacao

    resultado=""
    webhookok=0
    webhook=api.webhooks.list()
    for b in webhook:
        if b.name==webhook_name:
            webhookok=1
    
    # Cria novo caso nao encontrado
    if webhookok == 0:
        resultado=CriaWebhook(webhook_name,webhook_url)
        
    return resultado

def CriaWebhook(webhook_name,webhook_url):


	# Cria Webhook para receber msg via POST
	# Avisa Teams para gerar hooks para mensagems criadas somente
    # Retorna ok ou erro
    
	# Webhook para msgs
    try:
        api.webhooks.create(webhook_name,webhook_url,"messages","created")
        resultado="ok"
    except:
        resultado="erro"
        pass

	# Webhook para nova sala criada - boas vindas - ainda nao funcionando
    #api.webhooks.create(webhook_name+"-new",webhook_url,"rooms","created")
	
    return resultado

def CleanUpWebhook():

    # cleaning de webhooks
	# lista webhooks, e apaga os desativados
    # retorna resultado

    x = api.webhooks.list()
    msg=("lista de webhooks:\n")
    count = 0
    for b in x:
        msg=msg+("id: " + str(b.id)+"\n")
        msg=msg+("nome: "+str(b.name)+"\n")
        msg=msg+("status: "+str(b.status)+"\n")
        # Limpa webhooks desativados
        if (b.status)=='disabled':
            msg=msg+("apagando webhook "+str(b.name)+"...\n")
            try:
                api.webhooks.delete(b.id)
            except:
                print("erro")
                pass
        if (b.status)=="active":
            count = count + 1

    msg=msg+(str(count)+" webhooks ativos\n")
    
    return msg

def DeleteWebhook(webhook):    
        
    # apaga todos os webhooks com <nome> caso nome seja informado
    # retorna o resultado

    x = api.webhooks.list()
    msg=("lista de webhooks:\n")
    count = 0
    for b in x:
	    #Limpa webhooks desativados
        if (b.name)==nome:
            msg=msg+("apagando webhook... \n")
            try:
                api.webhooks.delete(b.id)
                count = count + 1
            except:
                print ("erro")
                pass
        
    msg=msg+(str(count)+" webhooks apagados\n")

    return msg



#########################################################
# Sessao sobre pessoas

def webexME():
	# detalhes sobre mim, retorna dados
	data = api.people.me()

	return data

def getwebexUserID(mail):
	
    # pesquisa ID do usuário e retorna; retorna vazio se nao encontrado
	
    try:
        usuario = api.people.list(email=mail)
        for x in usuario:
            user = x.id

    except:
        user="erro"
        pass
    
   
    return user


#########################################################
# Sessao sobre Salas

def WebexRoomCreate(name):

	# Cria Sala Webex,name aqui e' o nome da Sala, e retorna o ID da sala. Vazio se erro.

    try:
        api.rooms.create(name)
    except:
        pass

	# Encontra roomID da sala para devolver
    novasala = getwebexRoomID(name)

    return novasala

def WebexRoomDel(id):

    resultado=""
	#Remove sala Webex,id aqui e' roomID, retorna sucesso ou nao
    try:
        api.rooms.delete(id)
        resultado = "ok"
    except:
        resultado="erro"
        pass

    return resultado

def WebexIncUser(sala,mail):

    msg=""
	# Inclui usuario como membro da sala, criando sala caso nao exista
    # Descobre roomID da sala (sala e' o nome completo ou parte dela)
	# Retorna dados do sucesso ou nao da criacao da sala

    salaaincluir=getwebexRoomID(sala)

	# Cria sala caso esta nao exista
    if salaaincluir == None:
        try:
            salaaincluir = WebexRoomCreate(sala)
            msg=msg+"sala "+sala+" criada\n"
        except:
            msg="erro na criacao da sala\n"
            pass

    try:
        useraincluir=getwebexUserID(mail)
        msg=msg+"user "+mail+" encontrado\n"
    except:
        msg=msg+"erro para encontrar user\n"
        pass

	# inclui usuario caso id encontrado
    if useraincluir !=None:
			#executa a operacao
            try:
                api.memberships.create(salaaincluir,useraincluir)
                msg=msg+"user "+mail+" incluido na sala "+sala
            except:
                msg=msg+'erro na inclusao do usuario'
                pass

    return msg

def webexRoomsList():
	# lista salas que pertenco, retorna msg com a lista
 
    rooms=api.rooms.list()
    resultado = ""
    
    try:
	    for room in rooms:
		    resultado = resultado + "Sala " + str(room.title) + "\n"
    except:
        resultado="erro"

    return resultado


def getwebexRoomID(sala):

	# Retorna ID da Sala; retorna vazio se nao encontrado
   	# O parametro sala e' todo ou parte do nome da sala procurada
	
    # Salas que pertenco
    rooms=api.rooms.list()
    
    salawebex=None

	# for para encontrar ID da sala determinada

    try:
        for room in rooms:
            if sala in room.title:
                salawebex = room
                break
    except:
        pass
			
	# identifica ID da sala
    if salawebex != None:
        resultado = (str(salawebex.id))
    else:
        resultado = salawebex
		
    return resultado



#########################################################
# Sessao sobre envio de mensagens

def getwebexMsg(msgID):
	
	# msgID é o parametro resgatado do corpo do webhook
	# Retorna lista com o [0]texto da mensagem informada [1]ID da sala e [2]email da pessoa
	mensagem=api.messages.get(msgID)
				
	return mensagem.text,mensagem.roomId,mensagem.personEmail


def webexmsgRoom(sala,msg):

	# Manda msg para 1 sala especifica, procurando salas onde estou (usando partes do nome informado em sala).
    # Retorna sucesso ou erro

    rooms=api.rooms.list()
    salawebex = None

    #resgata ID da sala
    salawebex = getwebexRoomID(sala)
    
    # mandando uma mensagem para a Sala caso encontrada
    if salawebex != None:
        try:
            api.messages.create(salawebex,None,None,msg)
            resultado="ok"
        except:
            resultado="erro"
            pass
    return

def webexmsgRoomviaID(sala,msg):

	# Manda msg para 1 sala especifica informada via sala=roomID, nao retorna sucesso ou erro
    try:
        api.messages.create(sala,None,None,msg)
        msg="ok"
    except:
        msg="erro"
        pass

    return msg

#def webexmsgAll(msg):
	# mensagem em todas as salas que estou, nao e' mais recomandado esta funcao
	# pois manda mensagens indesejaveis para salas 1:1

	#rooms=api.rooms.list()

	#for room in rooms:
	#	api.messages.create(room.id,None,None,msg)
	
	#return
    
def getCiscoApiToken():
    
    #Chama Cisco.com para gerar token para consultas. Retorna Token

    url = "https://cloudsso.cisco.com/as/token.oauth2"

    # Dados criados de apiconsole.cisco.com

    payload = "client_id=7t9s28h7t5337pwknwdesssv&grant_type=client_credentials&client_secret=7xtCggEKxGAYKs4UTHYaKUsD"
    headers = {
    'content-type': "application/x-www-form-urlencoded",
    'Cache-Control': "no-cache",
    'Postman-Token': "f073e0db-6167-49c7-5e7a-54f4590331ff"
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    resposta=json.loads(response.text)
    token=resposta['access_token']

    return token

def CiscoApiHello (token):

    # chama Cisco API para testes
    url = "https://api.cisco.com/hello"

    headers = {
    'Authorization': "Bearer "+token,
    'Cache-Control': "no-cache",
    'Postman-Token': "9d6632a7-0d65-a22e-2274-3bac58526c7f"
    }

    response = requests.request("GET", url, headers=headers)

    return response.text

#########################################################
## FUNCOES de Logica

#########################################################
## Sessão analise de mensagems


def procurapam(parceiro):

    # Procura PAM do parceiro, retorna msg com dados ou resultado negativo caso nao encontrado

    msg = ""
    
    # Retorna erro se nome da pesquisa for muito pequeno
    if len(parceiro)<3:
        msg="Minimo 3 caracteres"
        return msg

    # Procura o PAM do parceiro
    # Base de dados
    filepath = "basePAM.txt"

    # loop de pesquisa  
    with open(filepath) as fp:  
        line = fp.readline()
        while line:
            texto=line.split(";")
            pname=texto[0]
                  
            # Caso encontrado cria resposta
            if parceiro in pname.lower():
                pcity=texto[1]
                ppam=texto[2]
                pmail=texto[3]
                pphone=texto[4]
    
                msg=msg+("Parceiro: "+pname+", PAM: "+ppam+"\nEmail: "+pmail+"@cisco.com\nTelefone: "+pphone+"\nCidade: "+pcity)
                    
            line = fp.readline()
                    
        # devolva negativa caso nada encontrado
        if msg=="":
            msg="Nenhum resultado encontrado.\n"

    return msg     
        
def autorizauser(usermail):

    # Esta funcao devolve true ou false para validar se usermail e' valido
    # (se pode pedir comando ou nao)

    # primeiro checa se email e da Cisco
    email=usermail.split("@")
        
    # caso positivo devolve true ou false
    if email[1]=="cisco.com":
        resultado = True
    else:
        resultado = False
   
    return resultado

def procurapartner(parceiro):

    # Procura Detalhes do parceiro, retorna msg com dados ou resultado negativo caso nao encontrado

    msg = ""
    
    # Retorna erro se nome da pesquisa for muito pequeno
    if len(parceiro)<3:
        msg="Minimo 3 caracteres"
        return msg

    # Procura o PAM do parceiro
    # Base de dados
    filepath = "techmap.txt"

    # loop de pesquisa  
    with open(filepath) as fp:  
        line = fp.readline()
        while line:
            texto=line.split(";")
            pname=texto[0]
                  
            # Caso encontrado cria resposta
            if parceiro in pname.lower():
                pcert=texto[1]
                sem_name=texto[2]
                sem_mail=texto[3]
                sem_phone=texto[4]
                fem_name=texto[5]
                fem_mail=texto[6]
                fem_phone=texto[7]
                ppam=procurapam(parceiro)
    
                msg=msg+("\nParceiro: "+pname+"\nCertificacão: "+pcert)
                msg=msg+("\nSEM: "+sem_name+"\nSEM Phone:"+sem_phone+"\nSEM email:"+sem_mail)
                msg=msg+("\nFEM: "+fem_name+"\nFEM Phone:"+fem_phone+"\nFEM email:"+fem_mail)
                msg=msg+("\nPAM:"+ppam)
                    
            line = fp.readline()
                    
        # devolva negativa caso nada encontrado
        if msg=="":
            msg="Nenhum resultado encontrado.\n"

    return msg   

def showtechmapping():

    # retorna lista de nome de parceiros do Tech Mapping

    msg = "\nLista de Parceiros Mapeados:\n"
    
    # Procura o PAM do parceiro
    # Base de dados
    filepath = "techmap.txt"

    # loop de pesquisa  
    with open(filepath) as fp:  
        line = fp.readline()
        while line:
            texto=line.split(";")
            pname=texto[0]
                  
            msg=msg+pname+"\n"

            line = fp.readline()
                    
    return msg   


def logica(comando,usermail):

    # faz a logica de entender o comando pedido e a devida resposta para o usuario
    # o parametro usermail e' utilizado para identificar o usuario que solicitou o comando
    # O usuario pode ser uzado como filtro para se executar ou negar o comando
    #
    # Retorna mensagem para ser enviada para console ou Webex teams
    
    #Separa o comando por espacos
    #Primeiro item e'o comando em si, os demais sao parametros deste comando
    #
    comando=comando.lower()
    sp=comando.split(" ")
    
    # comando na variavel box, lower deixa em minusculo para normalizar
    box=sp[0]
    
    # Para o caso de nenhum pedido coberto aqui
    mais="\nEscreva 'mais' para saber suas opções"
    
    msg=""
	
    # chamadas de acordo com os parametros

    # Funcoes somente para users Cisco

    if autorizauser(usermail)==True:
        # funcao busca o PAM
        if box == "pam" and len(sp)>1:
            parceiro=sp[1]
            msg=procurapam(parceiro)
        # funcao busca parceiro - procura pam inclusa
        if box == "parceiro" and len(sp)>1:
            parceiro=sp[1]
            msg=procurapartner(parceiro)
        if box == "techmap":
            msg=showtechmapping()
        


    # Funcoes para todos

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
            msg=msg+"O Quint@s Quinze é transmitido on-line. Se inscreva e participe\n"	
        
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

    return msg

#########################################################
## LOGICA COMECA AQUI

# inicia programa

# Testa existencia do Webhook. Caso negativo, cria
msg=ValidaWebhook(webhook_name,webhook_url)
# Imprime erro caso validacao do Webhook nao funcionou
if msg=="erro":
    print ("Erro de Webhook")


# para teste formato="c" de console, para produção usar "w" web
# ponha aqui a variavel para o formato
formato="w"


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
        # trata mensagem quando nao e' gerada pelo bot. Se nao e' bot, entao usuario
        try:     
            if content['name']==webhook_name and content['data']['personEmail']!=botmail:
	   	        # identifica id da mensagem
                msg_id=(content['data']['id'])
                # identifica dados da mensagem
                webextalk=getwebexMsg(msg_id)
                usermail=webextalk[2]
                mensagem=webextalk[0]
                sala=webextalk[1]

               # executa a logica
                msg=logica(mensagem,usermail)
           
               # Envia resposta na sala apropriada
                webexmsgRoomviaID(sala,msg)

        except:
               print("POST nao reconhecido")
               pass

def run(server_class=HTTPServer, handler_class=S, port=int(os.getenv('PORT',8080))):
        #Esta funcao roda efetivamente o servidor Web
        # PORT usa variavel PORT (tipico de servicos PaaS) ou porta 8080 caso nao definida (tipico para teste local http://localhost:8080)
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

if formato=='w':
    # Roda versao Producao Web
    run()

if formato=='c':
    # Roda versao console para testes e depuracao de erros

    box=""
    print("exit para sair. help para comandos de usuario. help+ para comandos avançados")

    # a definidcao do usermail (emai) e' importante para testar os filtros de usuario
    usermail=input("seu email>")
    
    # loop ate' 'exit'
    while box !="exit":
        box=input(">")

        # executa a logica
        msg=logica(box,usermail)
           
        # Imprime
        print(msg)


        if box=="eos":
            token=getCiscoApiToken()
            nova_resp=CiscoApiHello(token)
            print(nova_resp)
    
        #################################################################
        # FERRAMENTAS DE MANUTENCAO PARA CONSOLE
        # Utiliza para entender existencia de webhooks, salas e respectiva manutencao
     
        if box == "help+":
            msg="Comandos disponiveis:\nuserid: Identifica ID do usuario\nroomid: Identifica ID da sala\nusermail: troca usuario\nnovasala: Cria uma sala nova com usuario\nremovesala: Remove sala\nsalas: lista salas que pertenco\n"
            msg=msg+("webhook_create: cria webhook\nwebhook_del: apaga webhooks com este nome\nwebhook_clean: lista webhooks autuais, apagando os desativos\n")
            print (msg)

        #troca usuario para testar aplicacoes webexteams

        
        
        if box=="usermail":
                usermail=input("seu email>")

        # chamada funcao para encontrar id do user
        if box == "userid":
             email=input("Email do user:")
             msg = getwebexUserID(email)
             print (msg)

	    # chamada funcao para encontrar nome da sala
        if box == "roomid":
            sala=input("nome da sala? (todo ou partes):")
            msg = getwebexRoomID(sala)
            print (msg)

        # cleaning de webhooks
	    # lista webhooks, e apaga os desativados
        if box =="webhook_clean":
            msg=CleanUpWebhook()
            print(msg)

	    # apaga todos os webhooks com <nome> caso nome seja informado
        if box =="webhook_del":
            nome=input("nome do webhook:")
            msg=DeleteWebhook(nome)
            print(msg)

        # cria webhook
        if box =="webhook_create":
            nome=input("nome do webhook:")
            url=input("endereço http:")
            msg=CriaWebhook(nome,url)
            print(msg)

	    # chamada de funcao para Criar nova sala com user 
        if box == "novasala":
            email=input ("Qual email para incluir na sala?:")
            msg=getwebexUserID(email)

            if msg!="erro":
                novasala=input ('qual o nome da sala?:')
                msg=WebexIncUser(novasala,email)
                webexmsgRoom(novasala,"ola' "+str(email))
            else:
                msg="erro para identificar user"

            print(msg)

        # Remove Sala
        if box == "removesala":
            nome_sala=input('qual o nome da sala?:')
            msg=WebexRoomDel(getwebexRoomID(nome_sala))
            print(msg)

        # Lista salas
        if box =="salas":
            msg = webexRoomsList()
            print (msg)
            
        # FIM DAS FERRAMENTAS
        #################################################################


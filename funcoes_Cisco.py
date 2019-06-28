import json 

#########################################################
## FUNCOES API Suporte Cisco

#########################################################

def help():

    # Funcao ajuda deste bot
    msg="""
Forma de uso:  \n
Procurar Manager do Parceiro: manager partner ***nome do parceiro*** OU  \n
manager partner ***nome do manager***

Procurar PAM do parceiro: pam partner ***nome do parceiro***

Procurar SE do parceiro: se ***dna|dc|sec|collab*** partner ***nome do parceiro***

Detalhe do Parceiro: detail partner ***nome do parceiro***
"""
    
    return msg


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

def SupportAPIHello():

    # Testa API Hello
    token=getCiscoApiToken()
    nova_resp=CiscoApiHello(token)
    return nova_resp
        
    

#########################################################
## FUNCOES TECHMAPPING CISCO BRASIL

#########################################################

def procurase(parceiro,arquitetura,especialidade):

    # Procura SE do parceiro, retorna msg com dados ou resultado negativo caso nao encontrado

    # encerra se parceiro for nenhum (por enquanto)
    if parceiro=="":
        return

    # O 3o parametro desta funcao e' para entender especialidades do SE
    # caso tenha alguma, esta e' identificada, do contrario e' all (todas)
    hbox=especialidade.split(arquitetura)
    parametro=""
    
    if len(hbox)>1:
        parametro=hbox[1]
        especialidade=parametro.lstrip()
        especialidade=especialidade.rstrip()
    
    if especialidade=="":
        especialidade = "all"

    msg = ""
    count=0

    # Base de dados de acordo com a arquitetura definida

    if "sec" in arquitetura:
        filepath = "BASE_SECURITY.txt"
    if "dna" in arquitetura or "en" in arquitetura:
        filepath = "BASE_EN.txt"
    if "collab" in arquitetura:
        filepath = "BASE_COLLAB.txt"
    if "dc" in arquitetura or "data" in arquitetura:
        filepath = "BASE_DC.txt"

    # procura pessoa em parceiro especifico
    # No futuro incluir pesquisa em todos os parceiros caso parceiro = all (todos)

    if parceiro != "all":

        # loop de pesquisa e criacao da resposta 
        with open(filepath) as fp:  
            line = fp.readline()
            while line:
                texto=line.split(";")
                pname=texto[0]
                    
                # Caso encontrado o parceiro, investiga cada SE e competencias
                if parceiro in pname.lower():
                    if count == 0:
                        msg=("**Partner:**"+pname+"  \n")

                    sename=texto[1]
                    setel=texto[2]
                    semail=texto[3]
                    secomp=texto[4]
                                              
                    #identifica competencias
                    compet=""
                    for x in secomp.split(','):
                        if x !="":
                            compet = compet + "'" + x + "'"

                    # Seleciona se vai para impressao caso encontrado        

                    # Se nenhuma competencia declarada, entao vale todas
                    if especialidade == "all":
                        
                            msg=msg+("  \n**SE:** "+sename+": "+semail+" "+setel+"  \n")
                            if compet != "":
                                msg=msg+("**Competencies:**"+compet+"  \n")
                            count=count+1
                    
                    # Se competencia declarada, entao somente aquele SE que a possui
                    if especialidade != "all":
                        if compet != "" and especialidade in compet.lower():
                            msg=msg+("  \n**SE:** "+sename+": "+semail+" "+setel+"  \n")
                            msg=msg+("**Competencies:**"+compet+"  \n")
                            count=count+1

                  

                line = fp.readline()
                        
            # devolva negativa caso nada encontrado
            if count==0:
                msg="Nenhum resultado encontrado.  \n"

        return msg     


def procurapam(parceiro):

    # Procura PAM do parceiro, retorna msg com dados ou resultado negativo caso nao encontrado

    if parceiro=="":
        return


    msg = ""
    count=0

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
    
                msg=msg+("**PAM do Parceiro:** "+pname+": "+ppam+" "+pmail+"@cisco.com "+pphone+" "+pcity+"  \n\n")
                count=count+1
                    
            line = fp.readline()
                    
        # devolva negativa caso nada encontrado
        if count==0:
            msg="PAM: Nenhum resultado encontrado.  "

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

def procuramanager(parceiro):

    # Procura Detalhes do parceiro, retorna msg com dados ou resultado negativo caso nao encontrado

    if parceiro=="":
        return

    msg=""
    count = 0

    
    # Procura os Managers do parceiro
    # Base de dados
    filepath = "SEM.txt"

    # loop de pesquisa  
    with open(filepath) as fp:  
        line = fp.readline()
        while line:
            texto=line.split(";")
            pname=texto[0]
                
            # Caso encontrado cria resposta
            if parceiro in pname.lower():
                pcity=texto[1]
                pregion=texto[2]
                sem_title=texto[3]
                sem_name=texto[4]
                sem_mail=texto[5]
                sem_phone=texto[6]
                
                msg=msg+("**Manager:**"+sem_name+" **Title:**"+sem_title+" "+sem_phone+" "+sem_mail+"  \n")
                msg=msg+("**Region:**"+pregion+" **City:**"+pcity+"  \n\n")
                count = count + 1
                
            line = fp.readline()

    # tentativa de encontrar um SEM especifico caso a rotina acima nao retorne nada

    if count==0:    

        # loop de pesquisa  
        with open(filepath) as fp:  
            line = fp.readline()
            while line:
                texto=line.split(";")
                manager=texto[4]
                    
                # Caso encontrado cria resposta
                if parceiro in manager.lower():
                    pname=texto[0]
                    pcity=texto[1]
                    pregion=texto[2]
                    sem_title=texto[3]
                    sem_name=texto[4]
                    sem_mail=texto[5]
                    sem_phone=texto[6]
                    
                    msg=msg+("**Manager:**"+sem_name+" **Partner:**"+pname+" **Title:**"+sem_title+" "+sem_phone+" "+sem_mail+"  \n")
                    msg=msg+("**Region:**"+pregion+" "+pcity+"  \n\n")
                    count = count + 1
                    
                line = fp.readline()



        # devolva negativa caso nada encontrado
        if count==0:
            msg="Manager: Nenhum resultado encontrado.  \n"

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

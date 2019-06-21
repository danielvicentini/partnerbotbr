# -*- coding: utf-8 -*-
import json 

#########################################################
## FUNCOES API Suporte Cisco

#########################################################

def help():

    # ajuda
    msg="""
Uso:
Procurar Manager do Parceiro: manager partner ***nome do parceiro*** OU
manager partner ***nome do manager***
---
Procurar PAM do parceiro: pam partner ***nome do parceiro***
---
Procurar SE do parceiro: se ***dn|en|dna|sec|collab*** partner ***nome do parceiro***
---
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

    if parceiro=="":
        return

    msg = ""
    count=0

    # Procura o PAM do parceiro
    # Base de dados

    if "sec" in arquitetura:
        filepath = "base_SECURITY.txt"
    if "dna" in arquitetura or "en" in arquitetura:
        filepath = "base_EN.txt"
    if "collab" in arquitetura:
        filepath = "base_COLLAB.txt"
    if "dc" in arquitetura or "data" in arquitetura:
        filepath = "base_DC.txt"

    # loop de pesquisa  
    with open(filepath) as fp:  
        line = fp.readline()
        while line:
            texto=line.split(";")
            pname=texto[0]
                  
            # Caso encontrado cria resposta
            if parceiro in pname.lower():
                if count == 0:
                    msg=("**Partner:**"+pname)

                sename=texto[1]
                setel=texto[2]
                semail=texto[3]
                secomp=texto[4]
    
                msg=msg+("\n**SE:** "+sename+": "+semail+" "+setel)
                
                #identifica competencias
                compet=""
                for x in secomp.split(','):
                    if x !="":
                        compet = compet + "'" + x + "'"
                # imprime competencias somente se tiver pelo menos 1 declarada
                if compet !="" and especialidade=="all":
                    msg=msg+("\n**Competencies:**"+compet+"\n")

                count=count+1
                msg=msg+"\n---\n"

            line = fp.readline()
                    
        # devolva negativa caso nada encontrado
        if count==0:
            msg="Nenhum resultado encontrado.\n"

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
    
                msg=msg+("\n**PAM do Parceiro:** "+pname+": "+ppam+" "+pmail+"@cisco.com "+pphone+" "+pcity+"\n")
                count=count+1
                    
            line = fp.readline()
                    
        # devolva negativa caso nada encontrado
        if count==0:
            msg="\nPAM: Nenhum resultado encontrado.\n"

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
                
                msg=msg+("\nManager:"+sem_name+" Title:"+sem_title+" "+sem_phone+" "+sem_mail)
                msg=msg+("\nRegion:"+pregion+" City:"+pcity+"\n---\n")
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
                    
                    msg=msg+("**Manager:**"+sem_name+" **Partner:**"+pname+" **Title:**"+sem_title+" "+sem_phone+" "+sem_mail)
                    msg=msg+("\n**Region:**"+pregion+" "+pcity+"\n---\n")
                    count = count + 1
                    
                line = fp.readline()



        # devolva negativa caso nada encontrado
        if count==0:
            msg="Manager: Nenhum resultado encontrado.\n"

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

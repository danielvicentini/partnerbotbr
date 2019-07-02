from funcoes_Cisco import *
from funcoes_Mais import *

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
    
    # identifica e trata comandos relacionados a parceiros - palavra chave partner
    # logo a primeira parte do comando e' o que queremos procurar e
    # a segunda e' o nome do parceiro
    # logo comando = o comando completo, box = funcao esperada e parceiro = nome do parceiro
    sp=comando.split("partner")
    # comando na variavel box
    box=sp[0]

    # ajusta variavel com o nome do parceiro eliminando espacos
    if len(sp)>1:
        parceiro=sp[1].lstrip()
        # remove espacos no final, caso existam
        parceiro=parceiro.rstrip()

    
    msg=""
	
    # chamadas de acordo com os parametros

    # Funcoes somente para users Cisco

    if autorizauser(usermail)==True:
        # funcoes relacionadas a parceiro
        if "partner" in comando:
    
            # chama os managers do parceiro
            #if "manager" in box:
            #    msg=procuramanager(parceiro)

            if "manager" in box:
                msg=smartmanager(parceiro)

            # pam do parceiro
            #if "pam" in box:
            #    msg=procurapam(parceiro)
            if "pam" in box:
                msg=smartpam(parceiro)
    
            #if "se" in box or "systems engineer" in box:
            #    if "sec" in box:
            #        msg=procurase(parceiro,"sec",box)
            #    elif "dc" in box:
            #        msg=procurase(parceiro,"dc",box)
            #    elif "dna" in box:
            #        msg=procurase(parceiro,"dna",box)
            #    elif "col" in box:
            #        msg=procurase(parceiro,"collab",box)
            #    else:
            #        msg="use: se ***dc|dna|sec|collab*** partner ***partner name***"

            if "se" in box:
                if "sec" in box:
                    msg=smartse(parceiro,"sec",box)
                elif "dc" in box:
                    msg=smartse(parceiro,"dc",box)
                elif "dna" in box:
                    msg=smartse(parceiro,"dna",box)
                elif "col" in box:
                    msg=smartse(parceiro,"collab",box)
                else:
                    msg="use: se ***dc|dna|sec|collab*** partner ***partner name***"


            # detalhe completo do parceiro
            #if "detail" in box and parceiro != "":
            #    msg=procurapam(parceiro)
            #    msg=msg+procuramanager(parceiro)

            if "detail" in box and parceiro != "":
                msg=smartpam(parceiro)
                msg=msg+smartmanager(parceiro)

    
    if "help" in comando:
        msg=help()

    # Funcoes para todos

    

    if msg=="" or msg==None:
        msg="Use 'help' for help :-)"

    return msg

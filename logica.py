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

    # Para o caso de nenhum pedido coberto aqui
    mais="\nEscreva 'mais' para saber suas opções"
    
    msg=""
	
    # chamadas de acordo com os parametros

    # Funcoes somente para users Cisco

    if autorizauser(usermail)==True:
        # funcoes relacionadas a parceiro
        if "partner" in comando:
            # chama os managers do parceiro
            if "manager" in box:
                msg=procuramanager(parceiro)
            # pam do parceiro
            if "pam" in box:
                msg=procurapam(parceiro)
            if "se" in box or "systems engineer" in box:
                if "sec" in box:
                    msg=procurase(parceiro,"sec","all")
                if "dc" in box:
                    msg=procurase(parceiro,"dc","all")
                if "en" in box or "dna" in box:
                    msg=procurase(parceiro,"dna","all")
                if "col" in box:
                    msg=procurase(parceiro,"collab","all")

            # detalhe completo do parceiro
            if "detalhe" in box:
                msg=procurapam(parceiro)
                msg=msg+procuramanager(parceiro)
        
    
    if box=="eos":
       msg=SupportAPIHello()

    
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
        msg=maissobre(tema)
        
    return msg

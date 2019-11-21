from funcoes_Cisco import ajuda, smartlist, smartmanager, smartmeraki, smartpam, smartse, autorizauser, smartps, smartdap, smartsolution, smartagenda, smartestoque, smartaccess, smartcontact
from prime import testa_prime,prime_produto,prime_servico
from webexteams import getwebexRoomID, webexmsgRoomviaID

def logica(comando,usermail):

    # faz a logica de entender o comando pedido e a devida resposta para o usuario
    # o parametro usermail e' utilizado para identificar o usuario que solicitou o comando
    # O usuario pode ser uzado como filtro para se executar ou negar o comando
    #
    # Retorna mensagem para ser enviada para console ou Webex teams
    
    #Separa o comando por espacos
    #Primeiro item e'o comando em si, os demais sao parametros deste comando
    #tudo minusculo
    
    
    # 21.10.19
    # Novidade: Filtro de saia '|'
    # filtra no final a saida caso este simbolo seja usando
    
    filtro=""
    
    if '|' in comando:
        # divide a string em duas: antes e depois do simbolo |
        # O parametro 0 e' a parte da esquerda que e' o comando a ser tratado
        # O parametro 1 e' a parte da direita que representa o simbolo
        cmd=comando.split("|")
        filtro = cmd[1].strip()
        comando=cmd[0]    
    
    comando=comando.lower()
    
    # identifica e trata comandos relacionados a parceiros - palavra chave partner
    # logo a primeira parte do comando e' o que queremos procurar e
    # a segunda e' o nome do parceiro
    # logo comando = o comando completo, box = funcao esperada e parceiro = nome do parceiro
    sp=comando.split("partner")
    # comando ou a primeira palavra na variavel box
    box=sp[0]

    # ajusta a segunda variavel com o nome do parceiro eliminando espacos a esquerda e direita
    if len(sp)>1:
        parceiro=sp[1].strip()
        # remove espacos no final, caso existam
        #parceiro=parceiro.rstrip()

    
    # 21.11.19
    # variavel arquivo para o caso do bot devolver arquivos anexados
    
    arquivo=""
    msg=""
	
    # chamadas de acordo com os parametros

    # Funcoes somente para users Cisco

    if autorizauser(usermail)==True:
        # funcoes relacionadas a parceiro
        if "partner" in comando:
    
            if "manager" in box:
                msg=smartmanager(parceiro)

            # pam do parceiro
            if "pam" in box:
                msg=smartpam(parceiro)
    
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

            # procura SE certificado Meraki
            if "meraki" in box:
                msg=smartmeraki(parceiro)

            
            # procura SE de PS
            if "seps" in box:
                msg=smartps(parceiro)
            
            # procura dados DAP do parceiro
            if "dap" in box:
                msg=smartdap(parceiro)

            # procura parceiro por solucao - J. Sardinha - 23.7.19
            if "solution" in box:
                msg=smartsolution(parceiro)

            # procura agenda para parceiros - 26.7.19
            if "agenda" in box:
                # a variavel parceiro aqui na verdade leva o quarter procurado exemplo: q1
                msg=smartagenda(parceiro)

            if "detail" in box and parceiro != "":
                msg=smartpam(parceiro)
                msg=msg+smartmanager(parceiro)
                msg=msg+smartse(parceiro,"dna",box)
                msg=msg+smartse(parceiro,"collab",box)
                msg=msg+smartse(parceiro,"dc",box)
                msg=msg+smartse(parceiro,"sec",box)
                
            # nova funcao smart - 05.11.19

            if "newsearch" in box:
                parametros=comando.split(" ")
                msg=smartaccess(parametros[1],parametros)           
        
        
        # procura Contato do time de canais
        if "contato" in comando:
            
            # Transforma comando em parametros
            parametros=comando.split()
            # testa se tem o minimo de parametros
            if len(parametros)==2:
                contato=parametros[1]
                msg=smartcontact(contato)

        # lista_xls
        if "lista" in comando:        
          # Transforma comando em parametros
            parametros=comando.split()
            # testa se tem o minimo de parametros
            if len(parametros)==2:
                planilha=parametros[1]
                arquivo=smartlist(planilha)

                if arquivo !="erro":
                    msg = "Planilha "+arquivo+ " criada"
                elif arquivo == "erro":
                    msg = "Erro na criacao da planilha"

        # função prime - 16-7-2019
        # versao alpha

        if "desconto prime" in comando:

            correto="**Uso Correto:** desconto prime ***produto*** ou ***servico*** ***valor_prime*** ***valor_diferenca***.  \n**Exemplo:** desconto prime servico 65 30  \n"
            
            # Transforma comando em parametros
            parametros=comando.split()
            # testa se tem o minimo de parametros
            if len(parametros)==5:
                tipo=parametros[2]
                prime=int(parametros[3])
                diferenca=int(parametros[4])

                # primeiro testa se intervalo de prime e diferenca sao razoaveis
                if testa_prime(prime,diferenca)=="ok":
                    if "prod" in tipo:
                        # executa calculo prime para produto
                        msg=prime_produto(prime,diferenca)
                    elif "serv" in tipo or "svc" in tipo:
                        # executa calculo prime para servico
                        msg=prime_servico(prime,diferenca)
                    else:
                        # do contrario mensagem de erro com a sintaxe correta
                        msg=correto
                else:
                    # erro pois intervalos de prime e diferenca incorretos
                    msg="Intervalos de prime e/ou diferenca incorretos."
            else:
                # mensagem de erro pois nao tem o minimo de parametros
                msg=correto

    if "estoque" in comando:
        # Busca PID em estoque - segundo parametro deve ser PID
        # Transforma comando em parametros
        parametros=comando.split(" ")
        if len(parametros)>1: msg=smartestoque(parametros[1].upper())

    if "help" in comando:
        msg=ajuda()

    # Funcoes para todos

    
    if msg=="" or msg==None:
        msg="Use 'help' for help :-)"

    # 26-7-19
    # tenta logar tudo na sala "log do partnerbot"
    try:
        log="user:"+usermail+" comando:"+comando
        webexmsgRoomviaID(getwebexRoomID("log do partnerbot"),log,"")
    except:
        pass

    # 21.10.19 filtra a saida caso filtro tenha sido pedido
    if filtro != "":
        linhas=msg.split("\n")
        nova_msg=""
        for b in range(len(linhas)):
            if filtro.lower() in linhas[b].lower():
                nova_msg=nova_msg+linhas[b]+"\n"
        # altera msg somente com o filtro
        msg=nova_msg        

    return msg,arquivo
    #return msg

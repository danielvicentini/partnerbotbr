# Funcoes de texto - informacionais

def maissobre(tema):

    msg=""

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

    return msg


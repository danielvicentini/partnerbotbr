
# prime julho 2019
# margens padrao
margem_1tier=20    
margem_2tier=20
margem_dist=5

# racional de diferenciais na margem
dif_iss=3
dif_st=8
dif_extra_prime=0
dif_margem=(margem_dist+margem_2tier)-margem_1tier
dif_total=dif_margem+dif_st

# desconto percentual extra para o prime
produto_importado_1tier=dif_extra_prime-dif_margem
produto_importado_fatDiretoDist=dif_extra_prime+dif_margem
produto_importado_revenda_comST=dif_total+dif_extra_prime
produto_importado_revenda_semST=dif_extra_prime+dif_margem

produto_nacional_1tier=dif_extra_prime-dif_margem
produto_nacional_fatDiretoDist=dif_extra_prime+dif_margem
produto_nacional_revenda_comST=dif_total+dif_extra_prime
produto_nacional_revenda_semST=dif_extra_prime+dif_margem

servico_1tier=dif_extra_prime-dif_iss-dif_margem
servico_fatDiretoDist=dif_extra_prime+dif_iss+dif_margem
servico_revenda_comST=dif_extra_prime+dif_iss+dif_margem
servico_revenda_semST=dif_extra_prime+dif_iss+dif_margem




def variaveis():

    msg=("margem 1tier="+str(margem_1tier)+"%\n")
    msg=msg+("margem Dist="+str(margem_dist)+"%\n")
    msg=msg+("margem 2Tier="+str(margem_2tier)+"%\n")
    msg=msg+("Dif ISS:"+str(dif_iss)+"% Dif ST:"+str(dif_st)+"% Dif Extra Prime:"+str(dif_extra_prime)+"% Dif Margem:"+str(dif_margem)+"% Dif Total:"+str(dif_total)+"%\n")

    msg=msg+("Produto Importado 1tier:"+str(produto_importado_1tier)+"%\n")
    msg=msg+("Produto Importado Faturamento Direto:"+str(produto_importado_fatDiretoDist)+"%\n")
    msg=msg+("Produto Importado Revenda com ST:"+str(produto_importado_revenda_comST)+"%\n")
    msg=msg+("Produto Importado Revenda sem ST:"+str(produto_importado_revenda_semST)+"%\n")

    msg=msg+("Produto Nacional 1tier:"+str(produto_nacional_1tier)+"%\n")
    msg=msg+("Produto Nacional Faturamento Direto:"+str(produto_nacional_fatDiretoDist)+"%\n")
    msg=msg+("Produto Nacional Revenda com ST:"+str(produto_nacional_revenda_comST)+"%\n")
    msg=msg+("Produto Nacional Revenda sem ST:"+str(produto_nacional_revenda_semST)+"%\n")

    msg=msg+("Servico 1tier:"+str(servico_1tier)+"%\n")
    msg=msg+("Servico Direto:"+str(servico_fatDiretoDist)+"%\n")
    msg=msg+("Servico Revenda com ST:"+str(servico_revenda_comST)+"%\n")
    msg=msg+("Servico Revenda sem ST:"+str(servico_revenda_semST)+"%\n")


    return msg


### funcoes calculo de nao-prime


def calc_1tier(prime,diferenca):

    # Prime parceiro 1 Tier

    # desconto para parceiro 1 tier
    tier1=(100-prime)*(100+diferenca)
    tier1=round((100-(tier1/100)),2)
    
    # desconto para parceiro com faturamento direto no Dist
    direto=(100-prime)*(100+diferenca-produto_importado_fatDiretoDist)
    direto=round((100-(direto/100)),2)

    # desconto para revenda com ST
    tier2comst=(100-prime)*(100+diferenca-produto_nacional_revenda_comST)
    tier2comst=round((100-(tier2comst/100)),2)
    
    # desconto para revenda sem ST
    tier2semst=(100-prime)*(100+diferenca-produto_nacional_revenda_semST)
    tier2semst=round((100-(tier2semst/100)),2)
    
    msg=formata_resp(tier1,direto,tier2comst,tier2semst)


    return msg

def calc_faturaDist(prime,diferenca):

    # Prime e' do 2Tier que Fatura direto via Dist

    # desconto para parceiro 1 tier
    tier1=(100-prime)*(100+diferenca+produto_importado_fatDiretoDist)
    tier1=round((100-(tier1/100)),2)
    
    # desconto para parceiro com faturamento direto no Dist
    direto=(100-prime)*(100+diferenca)
    direto=round((100-(direto/100)),2)

    # desconto para revenda com ST
    tier2comst=(100-prime)*(100+diferenca-(produto_importado_revenda_comST-produto_importado_fatDiretoDist))
    tier2comst=round((100-(tier2comst/100)),2)
    
    # desconto para revenda sem ST
    tier2semst=(100-prime)*(100+diferenca)
    tier2semst=round((100-(tier2semst/100)),2)
    
    msg=formata_resp(tier1,direto,tier2comst,tier2semst)
    
    return msg


def calc_revComST(prime,diferenca):

    # Prime e' do 2tier com ST

    # desconto para parceiro 1 tier
    tier1=(100-prime)*(100+diferenca+produto_importado_revenda_comST)
    tier1=round((100-(tier1/100)),2)
    
    # desconto para parceiro com faturamento direto no Dist
    direto=(100-prime)*(100+diferenca+(produto_importado_revenda_comST-produto_importado_fatDiretoDist))
    direto=round((100-(direto/100)),2)

    # desconto para revenda com ST
    tier2comst=(100-prime)*(100+diferenca)
    tier2comst=round((100-(tier2comst/100)),2)
    
    # desconto para revenda sem ST
    tier2semst=(100-prime)*(100+diferenca+(produto_importado_revenda_comST-produto_importado_fatDiretoDist))
    tier2semst=round((100-(tier2semst/100)),2)

    
    msg=formata_resp(tier1,direto,tier2comst,tier2semst)



    return msg

def calc_revSemST(prime,diferenca):

    # Prime e' do parceiro revenda 2Tier sem ST
    #     
    # desconto para parceiro 1 tier
    tier1=(100-prime)*(100+diferenca+produto_importado_revenda_semST)
    tier1=round((100-(tier1/100)),2)
    
    # desconto para parceiro com faturamento direto no Dist
    direto=(100-prime)*(100+diferenca)
    direto=round((100-(direto/100)),2)

    # desconto para revenda com ST
    tier2comst=(100-prime)*(100+diferenca+(produto_importado_revenda_comST-produto_importado_revenda_semST))
    tier2comst=round((100-(tier2comst/100)),2)
    
    # desconto para revenda sem ST
    tier2semst=(100-prime)*(100+diferenca)
    tier2semst=round((100-(tier2semst/100)),2)

    msg=formata_resp(tier1,direto,tier2comst,tier2semst)

    return msg

def calc_srv1tier(prime,diferenca):

    # Prime e' do 1tier

    # desconto para parceiro 1 tier
    tier1=(100-prime)*(100+diferenca)
    tier1=round((100-(tier1/100)),2)
    
    # desconto para parceiro com faturamento direto no Dist
    direto=(100-prime)*(100+diferenca-servico_fatDiretoDist)
    direto=round((100-(direto/100)),2)

    # desconto para revenda com ST
    tier2comst=(100-prime)*(100+diferenca-servico_revenda_comST)
    tier2comst=round((100-(tier2comst/100)),2)
    
    # desconto para revenda sem ST
    tier2semst=(100-prime)*(100+diferenca-servico_revenda_semST)
    tier2semst=round((100-(tier2semst/100)),2)
 
    msg=formata_resp(tier1,direto,tier2comst,tier2semst)
    return msg


def calc_srv2tier(prime,diferenca):

    # Prime e' do 2Tier faturando Direto via Dist ou revenda com ST ou revando sem ST

    # desconto para parceiro 1 tier
    tier1=(100-prime)*(100+diferenca-servico_fatDiretoDist)
    tier1=round((100-(tier1/100)),2)
    
    # desconto para parceiro com faturamento direto no Dist
    direto=(100-prime)*(100+diferenca)
    direto=round((100-(direto/100)),2)

    tier2comst=direto
    tier2semst=direto
    
    msg=formata_resp(tier1,direto,tier2comst,tier2semst)
    return msg



def formata_resp(a,b,c,d):

    msg=""
    msg=msg+"**1Tier:**"+str(a)+" "
    msg=msg+"**Dist fatura direto:**"+str(b)+" "
    msg=msg+"**Tier2 com ST:**"+str(c)+" "
    msg=msg+"**Tier2 sem ST:**"+str(d)+"  \n"

    return msg


def prime_produto(prime,diferenca):

    msg="\nProduto: desconto prime:"+str(prime)+"%  \n"
    msg=msg+"Caso parceiro prime é 1tier, descontos para demais concorrentes:  \n"
    msg=msg+calc_1tier(prime,diferenca)    
    msg=msg+"\n\nCaso parceiro prime é 2tier:  \n"
    msg=msg+"Se parceiro prime é 2tier e fatura direto, descontos para demais concorrentes:  \n"
    msg=msg+calc_faturaDist(prime,diferenca)
    msg=msg+"\nSe parceiro prime é 2tier e revende com ST, descontos para demais concorrentes:  \n"
    msg=msg+calc_revComST(prime,diferenca)
    msg=msg+"\nSe parceiro prime é 2tier e revende sem ST, descontos para demais concorrentes:  \n"
    msg=msg+calc_revSemST(prime,diferenca)

    return msg


def prime_servico(prime,diferenca):

    msg="\nServicos. Prime de "+str(prime)+"%  \n"
    msg=msg+"Caso parceiro prime é 1tier, descontos para demais concorrentes:  \n"
    msg=msg+calc_srv1tier(prime,diferenca)    
    msg=msg+"\n\nCaso parceiro prime é 2tier, descontos para demais concorrentes:  \n"
    msg=msg+calc_srv2tier(prime,diferenca)
    
    return msg

def testa_prime(prime,diferenca):

    msg=""
    # testa se parametros de prime e diferenca estão dentro da equacao
    teste="ok"

    if prime<5 or prime>90:
        teste="Erro"
    if diferenca<5 or diferenca>50:
        teste="erro" 
        return msg

    return teste

# inicio

#msg=""

#prime=80
#diferenca=30

#z=testa_prime(prime,diferenca)

#if z=="ok":
#    msg=prime_produto(prime,diferenca)
#    print (msg)
#    msg=prime_servico(prime,diferenca)
#else:
#    msg="Parametros fora do padrao"

#print (msg)

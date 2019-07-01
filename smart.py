import os
import requests
import json

smartsheet_token=os.environ['SMART_TOKEN']


url = "https://api.smartsheet.com/2.0/sheets/2210243842205572"

payload = ""
headers = {
#    'Authorization': "Bearer m4dkqyyu65z7f0uow3i6vbks8l",
    'Authorization': "Bearer "+ smartsheet_token,
    'Content-Type': "application/json",
    'cache-control': "no-cache",
    'Postman-Token': "50a08645-32c6-4b43-9dcd-fb4db45c942e"
    }

response = requests.request("GET", url, data=payload, headers=headers)

json_res = json.loads(response.text)

# quantas linhas tem a planilha
linhas = json_res['totalRowCount']

#leva conteudo da planilha para sheet
sheet=json_res['rows']


# loop para imprimir o conteúdo da linha

count=2
while (count<linhas):

    # pega 1 linha
    linha=json_res['rows'][count]

    # zero variaveis
    parceiro=""
    col2=""
    col3=""
    col4=""
    col5=""
    col6=""
    col7=""

    # tenta pegar valores. Tenta pois se a celula estiver vazia, dará erro de conteúdo, por isto o 'try'
    try:
        parceiro=linha['cells'][0]['value']
        col2=linha['cells'][1]['value']
        col3=linha['cells'][2]['value']
        col4=linha['cells'][3]['value']
        col5=linha['cells'][4]['value']
        col6=linha['cells'][5]['value']
        col7=linha['cells'][6]['value']
    except:
        pass

    
    #monta a linha e imprime
    print (str(parceiro)+' '+str(col2)+" "+str(col3)+" "+str(col4)+" "+str(col5)+" "+str(col6)+" "+str(col7))
    count=count+1
    


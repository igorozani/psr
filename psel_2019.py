import requests
import json
from datetime import datetime
import re

# requisição GET para a), b), e c)
r = requests.get('https://us-central1-psel-clt-ti-junho-2019.cloudfunctions.net/psel_2019_get')

# requisição GET para d)
r2 = requests.get('https://us-central1-psel-clt-ti-junho-2019.cloudfunctions.net/psel_2019_get_error')

# transforma o JSON em objeto
# a), b), c)
data = json.loads(r.text)
# d)
data2 = json.loads(r2.text)

# variável para armazenar a somatória de likes
soma = 0

# criação do objeto que será a resposta.json
resposta = {'full name': "Igor José Lima Rozani",
            'email:': 'igorozani@gmail.com',
            'code_link': '',
            'response_a': [],
            'response_b': [],
            'response_c': soma,
            'response_d': []}

# a)
# verifica se tem promoção no titulo e insere na lista de dict da chave response_a
for element in data['posts']:
    if re.search('promocao', element['title'], re.IGNORECASE):
        resposta["response_a"].append({'product_id': element['product_id'], 'price_field': element['price']})

# ordena a lista por preço e depois ID
def myFunc(e):
    return e['price_field']
resposta['response_a'].sort(key=myFunc)

# retira produtos da lista com IDs repetidos
i = 0
j = i + 1
while (j != len(resposta['response_a'])):
    if resposta['response_a'][i]['product_id'] == resposta['response_a'][j]['product_id']:
        del resposta['response_a'][j]
    else:
        i = j
        j += 1

# b)
for element in data['posts']:
    if (element['media'] == 'instagram_cpc' and element['likes'] > 700):
       resposta['response_b'].append({'post_id': element['post_id'], 'price_field': element['price']})

# c)
# convertendo strings para date, para fazer verificações de datas
maio1='01/05/2019'
maio1=datetime.strptime(maio1,'%d/%m/%Y').date()
maio31='31/05/2019'
maio31=datetime.strptime(maio31,'%d/%m/%Y').date()

for element in data['posts']:
    str_date = element['date']
    date = datetime.strptime(str_date, '%d/%m/%Y').date()
    # utiliza as datas calculadas acima para saber se esta no mes de maio e se é uma mídia paga
    if (maio1<date<maio31 and (element['media'] == 'instagram_cpc' or element['media'] == 'facebook_cpc' or element['media'] == 'google_cpc')):
       soma += element['likes']
       resposta['response_c'] = soma


# d)
# verifica se existe um ID de produto com mais de um valor de preço e insere na lista response_d
i = 0
j = i + 1
while (i != len(data2['posts'])):
    while (j != len(data2['posts'])):
        if data2['posts'][i]['product_id'] == data2['posts'][j]['product_id']:
            if data2['posts'][i]['price'] != data2['posts'][j]['price']:
                resposta['response_d'].append({'product_id': data2['posts'][i]['product_id']})
        j += 1
    i+=1
    j=i+1

# ordena a lista por IDs de produtos
def myFunc(e):
    return e['product_id']
resposta['response_d'].sort(key=myFunc)

# retira produtos da lista com IDs repetidos
i = 0
j = i + 1
while (j != len(resposta['response_d'])):
    if resposta['response_d'][i]['product_id'] == resposta['response_d'][j]['product_id']:
        del resposta['response_d'][j]
    else:
        i = j
        j += 1

resposta = json.dumps(resposta, indent=3)

arquivo_json = open('resposta.json', 'w')
arquivo_json.write(resposta)
arquivo_json.close()

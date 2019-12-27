import os

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

# variável para armazenar a somatória de likes em b)
soma = 0

# criação do objeto que será a resposta.json
resposta = {'full name': "Igor José Lima Rozani",
            'email:': 'igorozani@gmail.com',
            'code_link': 'https://github.com/igorozani/psel2019-raccoon',
            'response_a': [],
            'response_b': [],
            'response_c': soma,
            'response_d': []}

# a)
# percorre a lista de posts
for element in data['posts']:
    # verifica se tem promoção no titulo de cada elemento
    if re.search('promocao', element['title'], re.IGNORECASE):
        # caso seja verdade, insere o elemento com os campos 'product_id' e 'price_field' na lista response_a
        resposta['response_a'].append({'product_id': element['product_id'], 'price_field': element['price']})

# ordena a lista por preço e depois por ID
resposta['response_a'] = sorted(resposta['response_a'],key=lambda k: (k['price_field'],k['product_id']))

# retira produtos da lista com IDs repetidos
# inicializa os indíces
i = 0
j = i + 1
# percorre a lista a partir do segundo elemento
while (j != len(resposta['response_a'])):
    # verifica se elementos adjacentes possuem mesmo ID
    if resposta['response_a'][i]['product_id'] == resposta['response_a'][j]['product_id']:
        # caso seja verdade, remove o elemento da lista
        del resposta['response_a'][j]
    else:
        # caso contrário, incrementa os indíces
        i = j
        j += 1
# OBS: note que o código da retirada acima só funciona pois a lista está ordenada

# b)
# percorre a lista de posts
for element in data['posts']:
    # verifica se a postagem possui mais de 700 likes e é da mídia instagram_cpc
    if (element['media'] == 'instagram_cpc' and element['likes'] > 700):
       # caso seja verdade, adiciona o elemento com os campos 'post_id' e 'price_field' na lista response_b
       resposta['response_b'].append({'post_id': element['post_id'], 'price_field': element['price']})

# ordena a lista por preço e depois por ID
resposta['response_b'] = sorted(resposta['response_b'],key=lambda k: (k['price_field'],k['post_id']))

# c)
# convertendo strings para date, para fazer verificações de datas
maio1='01/05/2019'
maio1=datetime.strptime(maio1,'%d/%m/%Y').date()
maio31='31/05/2019'
maio31=datetime.strptime(maio31,'%d/%m/%Y').date()

# percorre a lista de postagens
for element in data['posts']:
    # em cada elemento da lista, converte a string que representa a data para um obj datetime.date
    str_date = element['date']
    date = datetime.strptime(str_date, '%d/%m/%Y').date()
    # utiliza as datas calculadas acima para verificar se o elemento esta no mês de maio
    # ou seja, a data do elemento está entre 01/05/2019 e 31/05/2019
    # e se é uma mídia paga ou seja, a mídia ou é instagram_cpc, ou facebook_cpc, ou google_cpc
    if (maio1<date<maio31 and (element['media'] == 'instagram_cpc' or element['media'] == 'facebook_cpc' or element['media'] == 'google_cpc')):
       # caso seja verdade, incrementa 1 no contador de likes
       soma += element['likes']
       # copia o valor para response_c
       resposta['response_c'] = soma


# d)
# verifica se existe um ID de produto com mais de um valor de preço e insere na lista response_d
# inicializa os indíces
i = 0
j = i + 1
# percorre as postagens
while (i != len(data2['posts'])):
    while (j != len(data2['posts'])):
        # verifica se os elementos apontados pelos indíces i e j possuem o mesmo ID
        if data2['posts'][i]['product_id'] == data2['posts'][j]['product_id']:
            # caso seja verdade, verifica se os preços são diferentes
            if data2['posts'][i]['price'] != data2['posts'][j]['price']:
                # caso seja verdade, adiciona o elemento com o campos 'product_id' na lista response_d
                resposta['response_d'].append({'product_id': data2['posts'][i]['product_id']})
        # incrementa j para comparar todos os elementos com o que está apontado por i
        j += 1
    # atualiza os índices para repetir o processo para o próximo elemento da lista
    i+=1
    j=i+1

# ordena a lista por IDs de produtos
def myFunc(e):
    return e['product_id']
resposta['response_d'].sort(key=myFunc)

# retira produtos da lista com IDs repetidos
# inicializa os indíces
i = 0
j = i + 1
# percorre a lista a partir do segundo elemento
while (j != len(resposta['response_d'])):
    # verifica se elementos adjacentes possuem mesmo ID
    if resposta['response_d'][i]['product_id'] == resposta['response_d'][j]['product_id']:
        # caso seja verdade, remove o elemento da lista
        del resposta['response_d'][j]
    else:
        # caso contrário, incrementa os indíces
        i = j
        j += 1
# OBS: novamemente repare que o código da retirada acima só funciona pois a lista está ordenada

resposta = json.dumps(resposta, indent=4)

arquivo_json = open('resposta.json', 'w')
arquivo_json.write(resposta)
arquivo_json.close()

os.system( "curl -H \"Content-Type: application/json\" --data @resposta.json https://us-central1-psel-clt-ti-junho-2019.cloudfunctions.net/psel_2019_post")


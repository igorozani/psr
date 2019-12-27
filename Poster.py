import json
import requests
import os

# classe responsável por montar resposta.json e fazer a requisição POST
class Poster():

    @staticmethod
    def post(resposta):
        # recebe o objeto resposta e transforma em json
        resposta = json.dumps(resposta, indent=4)

        # cria e escreve o arquivo resposta.json
        arquivo_json = open('resposta.json', 'w')
        arquivo_json.write(resposta)
        arquivo_json.close()

        # faz a requisição HTTP POST
        os.system("curl -H \"Content-Type: application/json\" --data @resposta.json https://us-central1-psel-clt-ti-junho-2019.cloudfunctions.net/psel_2019_post")

        return
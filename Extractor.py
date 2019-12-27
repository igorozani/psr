import json
import requests


class Extractor():

    # retorna a resposta da requisição get na api RaccoonExtractor
    @staticmethod
    def get(rota):
        # requisição GET
        r = requests.get(rota)
        # transforma o JSON em objeto
        data = json.loads(r.text)
        return data
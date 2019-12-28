# ps-raccoon

Código feito para o processo seletivo raccoon, feito por Igor José Lima Rozani.

O código foi dividido em 3 classes para diminuir a responsabilidade da classe principal (psel_2019.py),
distribuindo as tarefas para suas respectivas classes.

A classe Extractor.py faz a requisição GET utilizando a rota passada como argumento. De modo análogo a classe Poster
faz a requisição POST.

A classe psel_2019.py contém as respostas a), b), c) e d) e chamadas dos métodos pertencentes à Extractor e Poster, 
para obter/enviar os dados json.

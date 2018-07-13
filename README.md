# WebProxyCache

Nesse trabalho, o objetivo é criar um proxy Web cache que ofereça seus serviços em duas portas TCP (Transmission Control Protocol) diferentes: uma para comunicação HTTP (54321) e outra para monitoramento básico (54322).

Na porta TCP 54321, o proxy Web deverá aceitar conexões a partir das quais serão enviadas requisições HTTP e suas respostas correspondentes.

Na porta TCP 54322, o proxy Web deverá apresentar informações básicas de seu uso.

Por exemplo: há quanto tempo o servidor está no ar; um ranking dos sites mais visitados; ranking dos maiores objetos armazenados; ranking dos objetos mais requisitados, etc.

## Instalação

Requisitos:
- Python 3.6
- Virtualenv
- Pip

Instalação:

```
$ cd WebProxyCache 
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

Para executar:
``$ python main.py``

Gerando a documentação:
```
$ cd docs
$ make html
```
Abra o `html/index.hml` em seu navegador para acessar a documentação gerada.

Para mais informações acesse a [documentação](https://leuzera.github.com/WebProxyCache) disponivel no Github.

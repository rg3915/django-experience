# Django Experience #20 - Consumido Marvel Comics API

<a href="">
    <img src="../img/youtube.png">
</a>

A api da Marvel está em https://developer.marvel.com/docs

Leia também https://developer.marvel.com/documentation/authorization


## Autorização

Gere um apikey no site da Marvel.

```
publicKey: 1234
privateKey: abcd
ts: 1
```


A partir da documentaçãoi em https://developer.marvel.com/documentation/authorization

Em Authentication for Server-Side Applications temos que vamos precisar de um

**ts** é timestamp e um **hash**

`md5(ts+privateKey+publicKey)`

Você precisará gerar um outro token em md5.

A partir do site https://www.md5hashgenerator.com/ faça a concatenação de

`md5(ts+privateKey+publicKey)`

Ex: `1abcd1234`

Resultado: `ffd275c5130566a2916217b101f26150`

```
ts=1
apikey=1234
hash=ffd275c5130566a2916217b101f26150
```

Exemplo de endpoint:

http://gateway.marvel.com/v1/public/characters?ts=1&apikey=1234&hash=ffd275c5130566a2916217b101f26150


Veja os demais endpoints em https://developer.marvel.com/docs


## Hash md5


```python
import hashlib

def compute_md5_hash(my_string):
    '''
    Converte string em md5 hash.
    https://stackoverflow.com/a/13259879/802542
    '''
    m = hashlib.md5()
    m.update(my_string.encode('utf-8'))
    return m.hexdigest()


publicKey = 1234
privateKey = 'abcd'
ts = 1

assert compute_md5_hash('1abcd1234') == 'ffd275c5130566a2916217b101f26150'
```

## Requests

Vamos usar o [Requests](https://docs.python-requests.org/en/latest/) para consumir a API.


## O serviço

```python
# service.py
# service.py
import hashlib

import requests
from decouple import config
from rich import print
from rich.console import Console
from rich.table import Table

console = Console()


def compute_md5_hash(my_string):
    '''
    Converte string em md5 hash.
    https://stackoverflow.com/a/13259879/802542
    '''
    m = hashlib.md5()
    m.update(my_string.encode('utf-8'))
    return m.hexdigest()


def make_authorization():
    '''
    Gera os tokens de autorização.
    '''
    publicKey = config('PUBLIC_KEY')
    privateKey = config('PRIVATE_KEY')
    ts = 1
    md5_hash = compute_md5_hash(f'{ts}{privateKey}{publicKey}')
    query_params = f'?ts={ts}&apikey={publicKey}&hash={md5_hash}'
    return query_params


def main(url):
    url += make_authorization()
    with requests.Session() as session:
        response = session.get(url)
        print(response)
        characters = response.json()['data']['results']

        table = Table(title='Marvel characters')
        headers = (
            'id',
            'name',
            'description',
        )

        for header in headers:
            table.add_column(header)

        for character in characters:
            values = str(character['id']), str(character['name']), str(character['description'])  # noqa E501
            table.add_row(*values)

        console.print(table)


if __name__ == '__main__':
    endpoint = 'http://gateway.marvel.com/v1/public/characters'
    main(endpoint)
```

```
python service.py
```


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

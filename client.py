# client.py
import timeit

import requests

base_url = 'http://localhost:8000/api/v1'

url_video = f'{base_url}/videos/'
url_movie = f'{base_url}/movies/?format=json'
url_movie_readonly = f'{base_url}/movies/movies_readonly/?format=json'
url_movie_regular_readonly = f'{base_url}/movies/movies_regular_readonly/?format=json'


def get_result(url):
    start_time = timeit.default_timer()
    r = requests.get(url)
    print('status_code:', r.status_code)
    end_time = timeit.default_timer()
    print('time:', round(end_time - start_time, 3))
    print()


if __name__ == '__main__':
    get_result(url_video)
    get_result(url_movie)
    get_result(url_movie_readonly)
    get_result(url_movie_regular_readonly)

# django-experience

Tutorial Django Experience 2022

## Este projeto foi feito com:

* [Python 3.9.8](https://www.python.org/)
* [Django 4.0.2](https://www.djangoproject.com/)
* [Django Rest Framework 3.12.4](https://www.django-rest-framework.org/)
* [Bootstrap 4.0](https://getbootstrap.com/)
* [htmx 1.6.1](https://htmx.org/)

## Como rodar o projeto?

* Clone esse repositório.
* Crie um virtualenv com Python 3.
* Ative o virtualenv.
* Instale as dependências.
* Rode as migrações.

```
git clone https://github.com/rg3915/django-experience.git
cd django-experience
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python contrib/env_gen.py
python manage.py migrate
python manage.py createsuperuser --username="admin" --email=""
```

## Passo a passo

Veja a pasta de [passo-a-passo](https://github.com/rg3915/django-experience/tree/main/passo-a-passo).


## Features da aplicação

* Renderização de templates na app `todo`.
* API REST feita com Django puro na app `video`.
* Django REST framework nas apps `example`, `movie` e `school`.

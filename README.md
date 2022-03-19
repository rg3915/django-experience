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
* Django REST framework nas apps `example`, `hotel`, `movie` e `school`.
* [Salvando dados extra](https://github.com/rg3915/django-experience/blob/main/passo-a-passo/08_drf_salvando_dados_extra.md) com [perform_create](https://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/#associating-snippets-with-users)
* [Reescrevendo o Admin do User](https://github.com/rg3915/django-experience/blob/main/passo-a-passo/10_reescrevendo_admin_user.md)
* [Editando mensagens de erro no DRF](https://github.com/rg3915/django-experience/blob/main/passo-a-passo/12_drf_editando_mensagens_erro.md)
* **Dica:** [Adicionando Grupos e Permissões](https://github.com/rg3915/django-experience/blob/main/passo-a-passo/14_grupos_permissoes.md)
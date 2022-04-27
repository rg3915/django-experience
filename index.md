# Django Experience

Tutorial Django Experience 2022

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

## Features da aplicação

* Renderização de templates na app `todo`.
* API REST feita com Django puro na app `video`.
* Django REST framework nas apps `example`, `hotel`, `movie` e `school`.
* [Salvando dados extra](https://github.com/rg3915/django-experience/blob/main/passo-a-passo/08_drf_salvando_dados_extra.md) com [perform_create](https://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/#associating-snippets-with-users)
* **Dica:** [Reescrevendo o Admin do User](https://github.com/rg3915/django-experience/blob/main/passo-a-passo/10_reescrevendo_admin_user.md)
* [Editando mensagens de erro no DRF](https://github.com/rg3915/django-experience/blob/main/passo-a-passo/12_drf_editando_mensagens_erro.md)
* **Dica:** [Adicionando Grupos e Permissões](https://github.com/rg3915/django-experience/blob/main/passo-a-passo/14_grupos_permissoes.md)


## Passo a passo

* [#01 - Como criar um projeto Django completo + API REST + Render Template](passo-a-passo/01_django_full_template_como_criar_um_projeto_django_completo_api_rest_render_template.md)
* [#02 - Criando API com Django SEM DRF - parte 2](passo-a-passo/02_criando_api_com_django_sem_drf_parte2.md)
* [#03 - DRF: Entendendo Rotas](passo-a-passo/03_drf_entendendo_rotas.md)
* [#04 - DRF: Entendendo Serializers](passo-a-passo/04_drf_entendendo_serializers.md)
* [#05 - DRF: Serializers mais rápido](passo-a-passo/05_drf_serializers_mais_rapido.md)
* [#06 - DRF: Entendendo Viewsets](passo-a-passo/06_drf_entendendo_viewsets.md)
* [#07 - DRF: APIView e o problema do get_extra_actions](passo-a-passo/07_drf_apiview_get_extra_actions.md)
* [#08 - DRF: Salvando dados extra](passo-a-passo/08_drf_salvando_dados_extra.md)
* [#09 - DRF: Entendendo Autenticação](passo-a-passo/09_drf_entendendo_autenticacao.md)
* [#10 - Dica: Reescrevendo o Admin do User](passo-a-passo/10_reescrevendo_admin_user.md)
* [#11 - DRF: Entendendo Permissões](passo-a-passo/11_drf_entendendo_permissoes.md)
* [#12 - Dica: Editando as mensagens de erro](passo-a-passo/12_drf_editando_mensagens_erro.md)
* [#13 - DRF: Fix Permissão](passo-a-passo/13_drf_fix_permissao.md)
* [#14 - DRF: Grupos e Permissões](passo-a-passo/14_grupos_permissoes.md)
* [#15 - DRF: Entendendo Validações](passo-a-passo/15_drf_entendendo_validacoes.md)
* [Entendendo o Django REST framework](passo-a-passo/16_entendendo_drf.md)
* [#17 - Novo comando](passo-a-passo/17_novo_comando.md)
* [#18 - Como rodar o projeto Django Experience no Windows 10 com PowerShell](https://youtu.be/clDiMuITKCs)
* [#19 - Dica: O problema do readonly e validação no Django](passo-a-passo/19_readonly_validation.md)

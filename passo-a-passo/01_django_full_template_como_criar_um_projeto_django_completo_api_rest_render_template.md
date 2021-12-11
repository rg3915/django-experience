# Django Experience #03 - Como criar um projeto Django completo + API REST + Render Template

## contrib e gitignore

```
mkdir contrib
touch contrib/env_gen.py
touch .gitignore
```

## A receita do bolo

```
cat << EOF > requirements.txt
Django==4.0
dr-scaffold==2.1.*
djangorestframework==3.12.*
django-seed==0.3.*
python-decouple==3.5
django-extensions==3.1.*
psycopg2-binary==2.9.*
drf-yasg==1.20.*
pytz
EOF
```

## Criando virtualenv e instalando tudo

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```


## Settings

```
django-admin startproject backend .
echo "SECRET_KEY=my-super-secret-key" > .env
```

Edite `settings.py`


```python
# settings.py
from decouple import config

SECRET_KEY = config('SECRET_KEY')

INSTALLED_APPS = [
    ...
    # 3rd apps
    'drf_yasg',
    'rest_framework',
    'dr_scaffold',
    'django_extensions',
    'django_seed',
    # my apps
]

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR.joinpath('staticfiles')
```

## Criando a app principal

```
cd backend
python ../manage.py startapp core
cd ..
```

> Adicione `backend.core` em `INSTALLED_APPS`.

Edite `backend/core/apps.py`.

`name = 'backend.core'`


## Criando os arquivos básicos

```
touch backend/core/urls.py

mkdir -p backend/core/templates/includes
mkdir -p backend/core/static/{css,img,js}

touch backend/core/static/css/style.css
touch backend/core/static/js/main.js
touch backend/core/templates/{base,index}.html
touch backend/core/templates/includes/{nav,pagination}.html

python manage.py create_template_tags core -n url_replace
```

> Mostrar as pastas.


## Criando mais uma app

```
cd backend
python ../manage.py startapp todo
cd ..
```

> Adicione `backend.todo` em `INSTALLED_APPS`.

Edite `backend/todo/apps.py`.

`name = 'backend.todo'`


```
mkdir backend/todo/api
mkdir -p backend/todo/templates/todo

touch backend/todo/api/serializers.py
touch backend/todo/api/viewsets.py

touch backend/todo/{forms,views,urls}.py
touch backend/todo/templates/todo/todo_{list,detail,form,confirm_delete}.html
```

Editar `backend/urls.py`

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('backend.core.urls', namespace='core')),
    path('', include('backend.todo.urls', namespace='todo')),
    path('admin/', admin.site.urls),
]

```


Editar `backend/core/urls.py`

```python
from django.urls import path

from .views import index

app_name = 'core'

urlpatterns = [
    path('', index, name='index'),
]

```

Editar `backend/todo/urls.py`

```python
from django.urls import include, path
from rest_framework import routers

from backend.todo import views as v
from backend.todo.api.viewsets import TodoViewSet

app_name = 'todo'

router = routers.DefaultRouter()

router.register(r'todos', TodoViewSet)

todo_urlpatterns = [
    path('', v.TodoListView.as_view(), name='todo_list'),
    path('<int:pk>/', v.TodoDetailView.as_view(), name='todo_detail'),
    path('create/', v.TodoCreateView.as_view(), name='todo_create'),
    path('<int:pk>/update/', v.TodoUpdateView.as_view(), name='todo_update'),
    path('<int:pk>/delete/', v.TodoDeleteView.as_view(), name='todo_delete'),
]

urlpatterns = [
    path('todo/', include(todo_urlpatterns)),
    path('api/v1/', include(router.urls)),
]

```

## Editando todos os arquivos

```
git clone https://github.com/rg3915/django-full-template.git /tmp/django-full-template
cp /tmp/django-full-template/.gitignore .
cp /tmp/django-full-template/contrib/env_gen.py contrib/

cp /tmp/django-full-template/backend/urls.py backend/
cp /tmp/django-full-template/backend/core/views.py backend/core/
cp /tmp/django-full-template/backend/core/static/css/style.css backend/core/static/css/
cp -R /tmp/django-full-template/backend/core/templates/ backend/core/
cp /tmp/django-full-template/backend/core/templatetags/url_replace.py backend/core/templatetags/

cp /tmp/django-full-template/backend/todo/{admin,forms,models,views}.py backend/todo/
cp /tmp/django-full-template/backend/todo/api/{serializers,viewsets}.py backend/todo/api/
cp -R /tmp/django-full-template/backend/todo/templates/todo/ backend/todo/templates/
```

Depois que editar tudo, faça

## Rodando as migrações

```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser --username="admin" --email=""
```

## Gerando alguns dados randomicamente

```
pip install psycopg2-binary
python manage.py seed todo --number=50
```

```
pip freeze | grep psycopg2-binary >> requirements.txt
```

## urls

Rode o comando para ver as urls

```
python manage.py show_urls
```

```
/
/api/v1/
/api/v1/todos/
/api/v1/todos/<pk>/
/redoc/
/swagger/
/todo/
/todo/<int:pk>/
/todo/<int:pk>/delete/
/todo/<int:pk>/update/
/todo/create/
```

## Estrutura das pastas

```
.
├── backend
│   ├── asgi.py
│   ├── core
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── __init__.py
│   │   ├── migrations
│   │   │   ├── __init__.py
│   │   │   └── __pycache__
│   │   ├── models.py
│   │   ├── __pycache__
│   │   ├── static
│   │   │   ├── css
│   │   │   │   └── style.css
│   │   │   ├── img
│   │   │   └── js
│   │   │       └── main.js
│   │   ├── templates
│   │   │   ├── base.html
│   │   │   ├── includes
│   │   │   │   ├── nav.html
│   │   │   │   └── pagination.html
│   │   │   └── index.html
│   │   ├── templatetags
│   │   │   ├── __init__.py
│   │   │   ├── __pycache__
│   │   │   └── url_replace.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── __init__.py
│   ├── __pycache__
│   ├── settings.py
│   ├── todo
│   │   ├── admin.py
│   │   ├── api
│   │   │   ├── __pycache__
│   │   │   ├── serializers.py
│   │   │   └── viewsets.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── __init__.py
│   │   ├── migrations
│   │   │   ├── 0001_initial.py
│   │   │   ├── __init__.py
│   │   │   └── __pycache__
│   │   ├── models.py
│   │   ├── __pycache__
│   │   ├── templates
│   │   │   └── todo
│   │   │       ├── todo_confirm_delete.html
│   │   │       ├── todo_detail.html
│   │   │       ├── todo_form.html
│   │   │       └── todo_list.html
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── urls.py
│   └── wsgi.py
├── contrib
│   └── env_gen.py
├── db.sqlite3
├── manage.py
├── README.md
└── requirements.txt
```
# Проект methods

Автор: Михалкин Дмитрий

Задача: Написать 2 метода API и описать их.

На данной странице можно увидеть структуру проекта:
///dirtree
methods:
    - apps:
        - __init__.py
        - admin.py
        - apps.py
        - models.py
        - serializers.py
        - tests.py
        - urls.py
        - views.py
        - migrations:
            - 0001_initial.py
            - __init__.py
    - methods:
        - __init__.py
        - asgi.py
        - settings.py
        - urls.py
        - wsgi.py
///
### Исходный код:
#### Файл settings проекта methods

``` py title='settings.py'
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'apps',
    'django_extensions',
    'rest_framework',
    'markdown',
]
```

#### Файл urls проекта methods
Модуль URL-конфигураций проекта.

Этот модуль определяет базовые URL-паттерны для веб-приложения.
Включает URL-адреса из приложения APPS.
Все URL-адреса, связанные с APPS, будут начинаться с '/apps/'.

``` py title='urls.py'
from django.urls import path, include
urlpatterns = [
    path('apps/', include('apps.urls')),
]
```

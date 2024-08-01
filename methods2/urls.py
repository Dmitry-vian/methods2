"""
Модуль URL-конфигураций проекта.

Этот модуль определяет базовые URL-паттерны для веб-приложения.
"""

from django.urls import path, include

"""
Включает URL-адреса из приложения APPS.
Все URL-адреса, связанные с APPS, будут начинаться с '/apps/'.
"""

urlpatterns = [
    path('apps/', include('apps.urls')),  # Включает URL-адреса из модуля
]

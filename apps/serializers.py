from rest_framework import serializers
from .models import CommandsResult


class CommandsResultSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Ifconfig.

    Преобразует объекты модели CommandResult в формат, пригодный для передачи в виде JSON.
    Используется для представления данных о сетевых интерфейсах.

    Поля:
        - name (str): Имя сетевого интерфейса.
        - output (str): Вывод команды ifconfig или ipconfig.
    """
    class Meta:
        model = CommandsResult
        fields = ['command', 'name', 'output']


from django.db import models


class CommandsResult(models.Model):
    """
    Модель для хранения информации о результатах выполнения команды ifconfig.

    Атрибуты:
        command (CharField): Название команды.
        name (CharField): Имя сетевого интерфейса или созданного файла.
        output (TextField): Текстовый вывод команды.
    """
    command = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    output = models.TextField()


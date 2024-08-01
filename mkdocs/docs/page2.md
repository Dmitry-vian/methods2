# Приложение apps

На этой странице мы можем рассмотреть приложение apps

### Исходный код

#### Файл apps приложения
Класс конфигурации для приложения 'apps'. Устанавливает поле автоинкремента и имя приложения.

``` py title='apps.py'
from django.apps import AppConfig


class AppsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps'
```

#### Файл models приложения
    Модель для хранения информации о результатах выполнения команды ifconfig и touchfile.

    Атрибуты:
        command (CharField): Название команды.
        name (CharField): Имя сетевого интерфейса или созданного файла.
        output (TextField): Текстовый вывод команды.

``` py title='models.py'
from django.db import models


class CommandsResult(models.Model):
    command = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    output = models.TextField()
```

#### Файл serializers приложения
    Сериализатор для модели Ifconfig.

    Преобразует объекты модели CommandResult в формат, пригодный для передачи в виде JSON.
    Используется для представления данных о сетевых интерфейсах.

    Поля:
        - command (str): Название команды.
        - name (str): Имя сетевого интерфейса.
        - output (str): Вывод команды ifconfig или ipconfig.

``` py title='serializers.py'
class CommandsResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommandsResult
        fields = ['command', 'name', 'output']
```

#### Файл urls приложения
    Создает экземпляр маршрутизатора для автоматической генерации URL-адресов для представлений (ViewSet).
    DefaultRouter используется для создания стандартных URL-паттернов для REST API.
    
    Устанавливает имя приложения для пространства имен URL. 
    Используется для создания уникальных имен URL и предотвращения конфликтов.
    
    Регистрирует ViewSet `SystemCommands` в маршрутизаторе с базовым именем 'ifconfig-apps'.
    Это создает URL-паттерны для стандартных действий CRUD 
    (создание, чтение, обновление, удаление) для объектов `Ifconfig`.
    
    Регистрирует ViewSet `SystemCommands` в маршрутизаторе с базовым именем 'touchfile-apps'.
    Это создает URL-паттерны для стандартных действий CRUD для объектов `Touchfile`.
    
    Сохраняет список сгенерированных URL-паттернов в переменной `urlpatterns`.
    Эти URL-паттерны будут использоваться в файле URL-конфигураций проекта.

``` py title='urls.py'
from rest_framework.routers import DefaultRouter

from apps.views import SystemCommands


router = DefaultRouter()
app_name = 'apps'
router.register(r'systemcommands', SystemCommands, basename='ifconfig-apps')
router.register(r'systemcommands', SystemCommands, basename='touchfile-apps')
urlpatterns = router.urls
```

#### Файл views приложения
    Позволяет выполнять системные команды через HTTP запросы и сохранять результаты в базе данных.
    
    В данном случае здесь представлены команды ifconfig и touchfile.
    - ifconfig позволяет получить нам информацию о сетевых интерфейсах.

    - touchfile позволяет создать новый файл.

``` py title='views.py'
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from .models import CommandsResult
from .serializers import CommandsResultSerializer
import subprocess
import platform


def execute_command(command):
    """
    Выполняет указанную системную команду и возвращает ее вывод.

    Args:
        command (str): Команда для выполнения.

    Returns:
        str: Вывод команды или сообщение об ошибке в случае неудачи.

    Raises:
        subprocess.CalledProcessError: Если при выполнении команды возникла ошибка.

    Notes:
        Использует кодировку cp866 для декодирования вывода команды.
        Для выполнения команды используется модуль subprocess.
    """
    try:
        # Используем subprocess.run для более удобного интерфейса
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True, encoding='cp866')
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Ошибка выполнения команды: {e}"
```

Использование(В моём случае я запускаю команду на локальном сервере):

curl -X POST -H "Content-Type: application/json" -d "{\"command\": \"ifconfig\"}" http://127.0.0.1:8000/apps/systemcommands/ifconfig/

Выполняет команду `ifconfig` или `ipconfig` (в зависимости от ОС) и возвращает результат.

curl -X POST -H "Content-Type: application/json" -d "{\"filename\": \"Hello.json\"}" http://127.0.0.1:8000/apps/systemcommands/touchfile/

Создает файл с указанным именем и возвращает результат.

``` py title='views.py'
class SystemCommands(viewsets.ViewSet):
    """
    ViewSet для выполнения системных команд.

    Позволяет выполнять различные системные команды, такие как `ifconfig` (для получения информации о сетевых интерфейсах) и `touchfile` (для создания файлов).
    Результаты выполнения команд сохраняются в базе данных.

    **Модель данных:**
    Использует модель `CommandsResult` для хранения информации о выполненных командах.
    """
    queryset = CommandsResult.objects.all()
    serializer_class = CommandsResultSerializer

    @action(detail=False, methods=['post'], url_path='ifconfig')
    def command_ifconfig(self, request):
        """
        Создает новую запись о результате выполнения команды.

        Args:
            request: Запрос HTTP.

        Returns:
            Response: HTTP-ответ с сериализованными данными созданной записи.

        Raises:
            ValidationError: Если в запросе отсутствует обязательное поле `command`.
        """
        command = request.data.get('command')
        if command != 'ifconfig':
            return Response({'error': 'Неверная команда'}, status=status.HTTP_400_BAD_REQUEST)

        # Определяем команду в зависимости от ОС
        system_command = 'ipconfig' if platform.system() == 'Windows' else 'ifconfig'

        output = execute_command(system_command)
        ifconfig_instance = CommandsResult.objects.create(name=command, output=output)
        serializer = CommandsResultSerializer(ifconfig_instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path='touchfile')
    def command_touchfile(self, request):
        """
        Создает новый файл и сохраняет информацию о создании в базе данных.

        Args:
            request: HTTP запрос, содержащий данные о создаваемом файле.

        Returns:
            Response: HTTP ответ с информацией о результате операции.

        Raises:
            Exception: В случае возникновения ошибок при создании файла.
        """
        filename = request.data.get('filename')
        if not filename:
            return Response({'error': 'Имя файла не указано'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with open(filename, 'w') as f:
                pass  # Файл будет создан при открытии
            touchfile_instance = CommandsResult.objects.create(name='touchfile', output=f"Файл {filename} создан")
            serializer = CommandsResultSerializer(touchfile_instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': f'Ошибка создания файла: {e}'}, status=status.HTTP_400_BAD_REQUEST)
```
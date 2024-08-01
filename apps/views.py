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



class SystemCommands(viewsets.ViewSet):
    """
    ViewSet для выполнения системных команд.

    Позволяет выполнять различные системные команды, такие как `ifconfig` (для получения информации о сетевых интерфейсах) и `touchfile` (для создания файлов).
    Результаты выполнения команд сохраняются в базе данных.

    **Использование:** (В моём случае я запускаю команду на локальном сервере)
    * **POST localhost/apps/systemcommands/ifconfig/:** Выполняет команду `ifconfig` или `ipconfig` (в зависимости от ОС) и возвращает результат.
    * **POST localhost/apps/systemcommands/touchfile/:** Создает файл с указанным именем и возвращает результат.

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

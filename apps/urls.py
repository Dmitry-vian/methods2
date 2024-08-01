from rest_framework.routers import DefaultRouter

from apps.views import SystemCommands



router = DefaultRouter()
app_name = 'apps'
router.register(r'systemcommands', SystemCommands, basename='ifconfig-apps')
router.register(r'systemcommands', SystemCommands, basename='touchfile-apps')
urlpatterns = router.urls
"""
Создает экземпляр маршрутизатора для автоматической генерации URL-адресов для представлений (ViewSet).
DefaultRouter используется для создания стандартных URL-паттернов для REST API.

Устанавливает имя приложения для пространства имен URL. 
Используется для создания уникальных имен URL и предотвращения конфликтов.

Регистрирует ViewSet `SystemCommands` в маршрутизаторе с базовым именем 'ifconfig-apps'.
Это создает URL-паттерны для стандартных действий CRUD (создание, чтение, обновление, удаление) для объектов `Ifconfig`.

Регистрирует ViewSet `SystemCommands` в маршрутизаторе с базовым именем 'touchfile-apps'.
Это создает URL-паттерны для стандартных действий CRUD для объектов `Touchfile`.

Сохраняет список сгенерированных URL-паттернов в переменной `urlpatterns`.
Эти URL-паттерны будут использоваться в файле URL-конфигураций проекта.
"""
# TESTING


Создать файлы конфигурации

```
<WORKDIR>/
  config.json
  studios/
    studio_name1.json
    studio_name2.json
```

Пример кофигурации

_config.json_
```json
{
  "__REQUIRED FIELDS__": "",
  "configs_repository_url": "git@github.com:username/repository.git",
  "__OPTIONAL FIELDS__": "",
  "studio_config_files_dir": "~/studios",
  
}
```

Создать конфиг файл для каждого сервера

```json
{
  "server_url": "https://ayon.domain.com:5000",
  "token": "*********"
}
```
Определить переменную для рабочей папки в shell или в коде

```shell
# linux
export AYON_TOOLS_WORKDIR="<WORKDIR>"
# windows
set AYON_TOOLS_WORKDIR="<WORKDIR>"
```

```python
import os
os.environ['AYON_TOOLS_WORKDIR'] = '<WORKDIR>'
```
По умолчанию будет использоваться путь `~/.ayon_tools`

Теперь можно запускать основной скрипт


### Переменные
- AYON_TOOLS_WORKDIR
- AYON_SERVER_URL
- AYON_API_KEY


# Roadmap

## Этап 1

### Взаимодействие с Ayon API

GET
- авторизация
- список пресетов анотомии
- данные конкретного пресета анотомии
- анотомия проекта
- список бандлов
- состав бандла
- студийные настройки всех аддонов бандла 
- проектные настройки аддонов бандла 
- студийные и проектные настройки одного аддона указаного бандла
- список депенденси пакетов
- атрибуты

SET
- обновление пресета анотомии
- создание пресета анотомии
- обновление анотомии проекта
- создание бандла
- обновление студийных настроек бандла
- обновление проектных настреок бандла
- заливка файлов депенденси пакета
- обновление свойств атрибуты
- создание атрибута

## Этап 2

### Структура приложения

Базовые классы и функции:

```
ayon_tools/
    api/
        auth.py
        addons.py
        bundles.py
        anatomy.py
        attributes.py
        packages.py
        projects.py
    utils/
        addon_tools.py          # builder and other tools
        anatomy_tools.py    
        check_tool.py           # apply chekers, diff toll
        shortcuts.py            # shortcut tools
        setup_logging.py
        addon_base_class.py
        git_tools.py            # manage git repo
    config.py
    cli.py
    __init__.py
    __main__.py
```

Структура файлов кофига:

```
generic/                        # or studio_name
    info.json                   # studio info (name, host, port)
    default/                    # for all projects of current studio
        settings/               # full json version of all settings
            anotomy.json
            addons/
                <addon_name>/
                    addon.py
                    info.json
                    default_settings.json
                    settins.yaml
                    checkers.py
    
        # shortcuts:
        addons/
            <addon_name>.yaml
        anatomy.yaml
        applications.yaml
        tasks.yaml
        families.yaml
        tamplates.yaml
    <project_name>/
        settings/
            ...
        addons/
            ...
        anatomy.yaml
        ...
```

Конфиги храянятся в git репозитории с такой структурой веток:

```
main                    # дефолтный конфиг из которого создаются новые ветки если не требуется наследование от какаой-то студии
studio/<studio_name1>   # ветка для отдельного клиента
studio/<studio_name2>   # ветка для отдельного клиента
...
```

Общие переменные и параметры конфига

- AYON_TOOLS_GIT_REPO       репозиторий с конфигами всех клиентов
- AYON_TOOLS_WORKDIR        диреткория куда клонируется репозиторий и происходит вся работа
- AYON_TOOLS_CONFIG_DIR     папка с конфигами клиентов   


По пути `AYON_TOOLS_CONFIG_DIR` располагаются файлы с ключами доступа клиентов

```
config_dir/
    <studio_name1>.yaml
    <studio_name2>.yaml
    ...
```

> Имя файла должно соответстовать имени студии из репозитория

Пример файла

```yaml
API_KEY=12345677890
```

### Авторизация

Авторизация теперь должна быть не общей а локальной под клиента.


### Инициализация приложения

Работа приложения должна проходить в 4 этапа

1. Вызывая команду в терминале мы парсим аргументы и передаём в основную функцию.

Обязательные аргументы:

- имя студии
- действие

Дополнительные рагументы

- имя проекта
- любые другие аргументы

2. Приложение получает контекст указанной студии (или нескольких). Это некоторое общее исходное состояние для любых
последующих действий.

- если репозитория нет
  - клонировать репозиторий
- если репозиторий есть
   - проверить что репозиторий не имеет незакомиченых изменений (если не включен DEV режим)
   - скачать обновления репозитория

3. Инициализация и выполнение команды

- исходя из задачи нужно создать инстансы соответствуюей студии или студий
  - переключиться на ветку студии 
  - загрузить все конфиги в текущий контекст (именно загрузку делать по запросу)
  - сделать проверки валидности конфигов
- выполнить команду


## Этап 3

### Реализация логики приложения

После инициализации приложения можно выполнять определённые команды

- обновление настроек аддонов для студии и для проекта
- создание нового проекта с указанными настройками
- проверка соответствия настроек локальных и на сервере (требуется после выполнения команды)

## Этап 4

### Реализация CLI
# AYON TOOLS

Инструменты для управление сервером AYON на базе репозитория конфигов.

- Все конфиги хранятся в одном репозитории
- Каждый сервер имеет свою git-ветку
- Для управления серверами требуются ключи для каждого сервера

## Настройка 

Для начала следует определиться с рабочей директорией. Там будут храниться все конфиги и скаченые файлы.

По умолчанию это путь `~/.ayon_tools`. Изменить его можно с помощью переменной `AYON_TOOLS_WORKDIR`
или флага команды `-w --workdir`.

### Необходимые файлы конфигурации в `workdir`

#### Основной конфиг файл

`<WORKDIR>/config.json`

Это основной конфиг приложения. Допустимые значения в этом файле (* - обязательное поле):

- `configs_repository_url*` - Адрес для клонирования репозитория с конфигурационными файлами серверов.
- `ayon_backend_repository_url` - Адрес для клонирования репозитория `ayon-backend`. В данный момент он общий для всех.
  По умолчанию используется адрес `https://github.com/ynput/ayon-backend`. 
- `studio_config_files_dir` - Диреткория с файлами настроек серверов. По умолчанию используется путь `<WORKDIR>/studios`
- `private_key_path`  и `public_key_path` - путь к ключам для клонирования репозиториев. По умолчанию используются стандартные пути в `~/.ssh`

#### Настройки серверов

`<WORKDIR>/studios`

Это директори с настройками серверов. Имя файла соответствует имени сервера с которым работаем, а так же имени ветки
в репоизтории конфигов.

Пример:

```
studios/
  studio_name1.json
  studio_name2.json
```

Пример содержимого такого файла:

```json
{
  "server_url": "http://localhost:5001",
  "token": "veryinsecurapikey",
  "label": "My Studio"
}
```

## Запуск

Перед запуском убедитесь что виртуальное окружение настроено

```shell
poetry install
```

Теперь можно запускать команду.

```shell
poetry run python -m ayon_tools --help
```

```shell
poetry run python -m ayon_tools apply --help
```

## Команды

### APPLY

Клманда `apply` должна как минимум получить один аргумент с именем сервера.

```shell
poetry run python -m ayon_tools apply myserver
```

Прежде чем запускать команду `apply` убедитесь что в git-репозитории конфигов серверов есть одноимённая ветка со всеми
необходимыми конфигами. 

Команда `apply` применяет все настройки, указанные в репозтории, на указанный сервер.

### DUMP

TODO

### RESTORE

TODO

### CHECK

TODO

### INFO

TODO

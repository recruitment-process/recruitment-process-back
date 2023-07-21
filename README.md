### recruitment-process-back

# Бэкенд CRM для HR

### О проекте:

### Оглавление:
- [Бэкенд CRM для HR](#бэкенд-crm-для-hr)
    - [О проекте:](#о-проекте)
    - [Оглавление:](#оглавление)
  - [Запуск приложения](#запуск-приложения)
      - [Клонируйте реппозиторий](#клонируйте-реппозиторий)
      - [Перейдите в папку с проектом recruitment-process-back, установите и запустите виртуальное окружение.](#перейдите-в-папку-с-проектом-recruitment-process-back-установите-и-запустите-виртуальное-окружение)
      - [Установите зависимости:](#установите-зависимости)
      - [Запустите приложение на локальном сервере](#запустите-приложение-на-локальном-сервере)
    - [Установка pre-commit hooks](#установка-pre-commit-hooks)
      - [Установка pre-commit](#установка-pre-commit)
      - [Установка hooks](#установка-hooks)
    - [Работа с commitizen](#работа-с-commitizen)
    - [Используемые технологии:](#используемые-технологии)

## Запуск приложения
#### Клонируйте реппозиторий

```sh
git clone git@github.com:recruitment-process/recruitment-process-back.git
```

#### Перейдите в папку с проектом recruitment-process-back, установите и запустите виртуальное окружение.

```sh
cd recruitment-process-back
```

```sh
python -m venv venv
```

* Если у вас Linux/MacOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/Scripts/activate
    ```
#### Установите зависимости:

```sh
pip install -r requirements.txt
```

#### Запустите приложение на локальном сервере
Перейдите в папку crm_backend
```sh
cd crm_backend
```
* Если у вас windows
    ```sh
    python manage.py runserver
    ```
* Если у вас Linux/MacOS
    ```sh
    python3 manage.py runserver
    ```

### Установка pre-commit hooks

Для того, чтобы при каждом коммите выполнялись pre-commit проверки, необходимо:
- Установить pre-commit
- Установить pre-commit hooks

#### Установка pre-commit
Модуль pre-commit уже добавлен в requirements и должен установиться автоматически с виртуальным окружением.

Проверить установлен ли pre-commit можно командой (при активированном виртуальном окружении):
```sh
pre-commit --version
>> pre-commit 3.2.0
```

Если этого не произошло, то необходимо установить pre-commit:
```sh
pip install pre-commit
```

#### Установка hooks
Установка хуков:
```sh
pre-commit install --all
```
Установка хука для commitizen
```sh
pre-commit install --hook-type commit-msg
```
В дальнейшем, при выполнении команды git commit будут выполняться проверки, перечисленные в файле .pre-commit-config.yaml.

Если не видно, какая именно ошибка мешает выполнить commit, можно запустить хуки вручную командой:
```sh
pre-commit run --all-files
```

### Работа с commitizen
Чтобы сгенерировать установленный git-commit, запустите в вашем терминале
```sh
cz commit
```
или сочетание клавиш
```sh
cz c
```

### Используемые технологии:
- Python 3.10
- Django 4.1
- Django Rest Framework 3.14.0

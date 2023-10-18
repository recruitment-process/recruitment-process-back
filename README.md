### recruitment-process-back

![recruitment-process](https://github.com/recruitment-process/recruitment-process-back/actions/workflows/commit-tests.yml/badge.svg) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


# Бэкенд CRM для HR

### О проекте:

### Оглавление:
- [Бэкенд CRM для HR](#бэкенд-crm-для-hr)
    - [О проекте:](#о-проекте)
    - [Оглавление:](#оглавление)
  - [Запуск приложения](#запуск-приложения)
      - [Запуск приложения на локальном сервере](#запуск-приложения-на-локальном-сервере)
      - [Запуск тестов:](#запуск-тестов)
      - [Документация API доступна по адресам:](#документация-api-доступна-по-адресам)
      - [Админка доступна по адресу:](#админка-доступна-по-адресу)
    - [Установка pre-commit hooks](#установка-pre-commit-hooks)
      - [Установка pre-commit](#установка-pre-commit)
      - [Установка hooks](#установка-hooks)
    - [Работа с commitizen](#работа-с-commitizen)
  - [Используемые технологии](#используемые-технологии)
  - [Авторы](#авторы)

## Запуск приложения
**Клонирование реппозитория**

```sh
git clone git@github.com:recruitment-process/recruitment-process-back.git
```

Перейдите в папку с проектом recruitment-process-back, установите и запустите виртуальное окружение.

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
**Установка зависимостей**

  ```sh
  pip install -r requirements.txt
  ```
**Применяем миграции:**

  ```sh
  python manage.py migrate
  ```
**Создаем суперпользователя:**

  ```
  python manage.py createsuperuser
  ```
#### Запуск приложения на локальном сервере
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
#### Запуск тестов:
```sh
python manage.py test
```

#### Документация API доступна по адресам:
```sh
http://127.0.0.1:8000/api/schema/swagger-ui/
```
```sh
http://127.0.0.1:8000/api/schema/redoc/
```

#### Админка доступна по адресу:

```sh
http://127.0.0.1:8000/admin/
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
>> pre-commit 3.3.3
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

## Используемые технологии
- Python 3.10
- Django 4.1
- Django Rest Framework 3.14.0

## Авторы
- [Балахонова Марина](https://github.com/margoloko)
- [Таргонский Михаил](https://github.com/mishatar)
- [Попов Егор](https://github.com/DOSuzer)
- [Ильин Иван](https://github.com/ivan-hedgehog)

# Установка сервера в venv

1. В папке выполняем команду `python -m venv --clear venv`.
2. В PowerShell Windows 11 нужно выполнить в этой же папке команду `Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope Process`. Смысл её в том, что мы разрешаем в области видимости этого процесса консоли выполнять любые командлеты PowerShell. Это понадобится для запуска виртуального окружения.
3. Выполняем команду `.\venv\Scripts\Activate.ps1`. В промпте (приглашении) консоли должна появится надпись `(venv) PS`. Теперь мы находимся в виртуальном окружении. Если мы выполним команду `pip freeze`, то вывод должен быть пустым, то есть не установлено ни одного модуля.
4. Устанавливаем нужное. Последовательно выполняем следующие команды: `pip install fastapi "uvicorn[standard]" SQLAlchemy alembic psycopg2-binary`. Можно снова проверить с помощью pip freeze, которая должна показать список установленных модулей.
5. Устанавливаем PostgreSQL. Создаём в нём пользователя. Для этого пользователя создаём БД. В linux это выглядит примерно так: 
```sh
sudo su - postgres
createuser --interactive --pwprompt
createdb -O created_user db_name
```
Если непонятно, что здесь происходит, то читаем о PostgreSQL. Далее выполняем команду `cp ./env.template .env`, после чего вводим данные от созданного пользователя в PostgreSQL и название базы. Выполняем команду `cp ./alembic.ini.template alembic.ini` и тоже правим пусть к БД. Выполняем команду `alembic upgrade 536366596e20`.
6. Запускаем локальный сервер с помощью команды `uvicorn main:app --reload`.

## Обновления от 29.03.2024

- Добавлено немного фронтенда. Подключены через CDN [TailwindCSS](https://tailwindcss.com/) и [AlpineJS](https://alpinejs.dev/start-here). Некоторые решения по вёрстке можно найти на [flowbite.com](https://flowbite.com/docs/getting-started/introduction/). Какой-то концепции нет, будем считать это отправной точкой.
- Добавлен run.bat, работать он будет, если виртуальное окружение создать в папке `venv`.

## Обновления от 01.04.2024

- Прикрутил PostgreSQL и alembic, теперь можно использовать БД.

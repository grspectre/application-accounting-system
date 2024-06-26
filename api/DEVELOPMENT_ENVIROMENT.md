# Настраиваем среду разработки на сервере

## Примерная последовательность действий

```bash
cd development
mkdir pir01
git clone https://github.com/grspectre/application-accounting-system.git
cd application-accounting-system/api/
cp gunicorn_start.template gunicorn_start
nano gunicorn_start
chmod u+x gunicorn_start
sudo cp ./sysconfigs/nginx_virtual_host /etc/nginx/sites-available/pir01
sudo nano /etc/nginx/sites-available/pir01
sudo cp ./sysconfigs/supervisor.conf /etc/supervisor/conf.d/pir01.conf
sudo nano /etc/supervisor/conf.d/pir01.conf
python3 -m venv venv --clear
source venv/bin/activate
pip install SQLAlchemy fastapi gunicorn "uvicorn[standard] alembic requests psycopg2-binary"
cd /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/pir01
```

Особое внимание следует обратить на пути ко всяческим файлами и unix-сокету (а то по сути оно работать будет, но почему-то вывод методов бекенда не будет изменяться. А ты оказывается получаешь данные с другого инстанса для разработки. Так что нужно быть внимательным.)

Обязательно нужно изменить наименование upstream в виртуальном хосте nginx.

## Подключаем базу данных.

Предполагается, что мы находимся в каталоге `./api`. БД с номерами `pir_01 - pir_04` уже созданы, доступы:

```
user: accounting
pwd: accounting
```

```
source venv/bin/activate
pip install alembic psycopg2-binary # если в venv/bin/ не появился файл alembic - копируем его с прода
cp alembic.ini.template alembic.ini # правим путь к базе
cp env.template .env # правим наименование БД
alembic upgrade 536366596e20 # мигрируем БД
```

## Workflow тестирования

1. Заливаем изменения в github в свою ветку
2. На сервере делаем git pull в своей ветке
3. Выполняем команду `sudo supervisorctl restart pir01` где `pir01` - идентификатор тестового инстанса.

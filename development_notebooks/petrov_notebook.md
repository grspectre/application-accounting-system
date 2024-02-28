# Дневник разработчика Николай Евгеньевич Петров (nepetrov7)

## 2024-02-17 - 2024-03-01, Спринт 1

### 2024-02-19

Провели собрание, все шло со скрипом. Большинство из команды не имеет опыта в it, поэтому в обсуждении мало принимали участие, надеюсь в будущем это изменится.

создали репозиторий, добавили участников.

проголосовали за язык программирования, лидирующим оказался python.

договорились что база будет в postgresql.

Решили что ПО будет монолитом, потому как он достаточно прост, нам не нужны сложности с микросервисами, да и проект мы не собираемся развивать в дальнейшем, он снимается с поддержки в июне 2024 =))

### 2024-02-25

взял на себя таску с проработкой структуры базы данных

Сущности в базе данных для Системы учета заявок для сервисного центра техники:

1. Таблица "employee": (сотрудники)
  - employee_id (идентификатор сотрудника)
  - name (ФИО)
  - roles (роли пользователя: admin, manager)
  - email
  - phone (телефон)
  - password
  - context (json) - дополнительная информация о пользователе в формате JSON
  - is_active (флаг активности пользователя)


2. Таблица "customers": (клиенты)
  - customer_id (идентификатор клиента)
  - name (ФИО)
  - email
  - phone (телефон)
  - password
  - context (json) - дополнительная информация о пользователе в формате JSON
  - is_active (bool) (флаг активности пользователя)
  - is_company (bool) (флаг отвечающий за показатель физическое лицо или юридическое)

3. Таблица "orders": (Заявки)
  - id (идентификатор заявки)
  - customer_id (ссылка на клиента)
  - employee_id (идентификатор сотрудника)
  - order_type (например, телефонная консультация, выезд на ремонт)
  - status (например, новая, в обработке, завершена)
  - creation_date (дата создания заявки)
  - update_date (дата изменения заявки)

отправил на ревью коллегам.
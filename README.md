# Уведомления пользователей на Flask

Данный микросервис разработан на Flask и предоставляет RestAPI для создания, отображения и отправки уведомлений пользователям. Он использует MongoDB для хранения данных уведомлений и SMTP-сервер для отправки уведомлений по электронной почте.

## Описание функциональности

Микросервис предоставляет следующие функции:

- Создание нового уведомления: Метод `POST /create` позволяет создавать новые уведомления для пользователей. Уведомление может быть привязано к конкретному пользователю, иметь целевой идентификатор (например, идентификатор сущности, к которой относится уведомление) и содержать произвольные данные.
- Отображение списка уведомлений: Метод `GET /list` позволяет получать список уведомлений пользователя. Список включает информацию о количестве уведомлений, количестве непрочитанных уведомлений и самих уведомлениях. Можно указать параметры `skip` и `limit`, чтобы получить определенное количество уведомлений.
- Отметка уведомления как прочитанного: Метод `POST /read` позволяет отметить уведомление как прочитанное для пользователя.

## Установка и запуск

1. Установите Docker и Docker Compose на вашем компьютере.
2. Создайте файлы `app.py`, `Dockerfile`, `docker-compose.yml` и `requirements.txt`.
3. Скопируйте соответствующий код из репозитория и вставьте его в каждый файл.
4. Укажите необходимые переменные окружения в файле `docker-compose.yml`.
5. Выполните команду `docker-compose up` для запуска микросервиса.

## Переменные окружения

В файле `docker-compose.yml` можно настроить следующие переменные окружения:

- `PORT`: Порт, на котором будет работать приложение Flask.
- `EMAIL`: Тестовый адрес электронной почты, используемый для отправки уведомлений.
- `DB_URI`: Строка подключения к MongoDB.
- `SMTP_HOST`: Хост SMTP-сервера.
- `SMTP_PORT`: Порт SMTP-сервера.
- `SMTP_LOGIN`: Логин пользователя SMTP-сервера.
- `SMTP_PASSWORD`: Пароль пользователя SMTP-сервера.
- `SMTP_EMAIL`: Адрес электронной почты, от которого будут отправляться уведомления.
- `SMTP_NAME`: Имя, которое будет отображаться у получателя уведомлений.

## API Endpoints

### Создание нового уведомления

URL: `POST /create`

Тело запроса:
```json
{
    "user_id": "638f394d4b7243fc0399ea67",
    "target_id": "0399ea67638f394d4b7243fc",
    "key": "new_message",
    "data": {
        "some_field": "some_value"
    }
}
```
### Отметка уведомления как прочитанного

URL: `POST /read`

Тело запроса:
```json
{
    "notification_id": "638f394d4b7243fc0399ea67"
}
```
## Список уведомлений

### Получение списка уведомлений

URL: `GET /list`

Параметры запроса:
- `user_id` (обязательный) - идентификатор пользователя, для которого запрашивается список уведомлений.

Пример запроса:
URL: `GET /list?user_id=12345`

Пример ответа:
```json
{
    "notifications": [
        {
            "id": "638f394d4b7243fc0399ea67",
            "title": "Новое уведомление",
            "message": "Привет! У тебя есть новое уведомление.",
            "timestamp": "2021-09-22T10:30:00Z",
            "read": false
        },
        {
            "id": "987654abcdef",
            "title": "Важное уведомление",
            "message": "Не забудь выполнить задачу до конца дня.",
            "timestamp": "2021-09-23T16:45:00Z",
            "read": true
        }
    ]
}
```
### Зависимости
В файле requirements.txt перечислены зависимости, которые необходимо установить для работы микросервиса. Выполните команду pip install -r requirements.txt, чтобы установить все требуемые зависимости.
Chat

Добро пожаловать в тестовое задание.

| Описание            | Команда<br>                                                                        |
| ------------------- | ---------------------------------------------------------------------------------- |
| Запустить контейнер | docker-compose build --no-cache<br>docker-compose up --build <br>                  |
| Завершить контейнер | docker-compose down --volumes                                                      |
|                     |                                                                                    |
| Создать миграцию    | docker-compose exec web alembic revision --autogenerate -m "Initial migration"<br> |
| Применить миграцию  | docker-compose exec web alembic upgrade head                                       |







This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.
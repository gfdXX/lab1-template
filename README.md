# Лабораторная работа #1

![GitHub Classroom Workflow](../../workflows/GitHub%20Classroom%20Workflow/badge.svg?branch=master)

## Continuous Integration & Continuous Delivery

### Формулировка

В рамках первой лабораторной работы требуется написать простейшее веб приложение, предоставляющее пользователю набор
операций над сущностью Person. Для этого приложения автоматизировать процесс сборки, тестирования и релиза на Render.com.

Приложение должно реализовать API:

* `GET /api/v1/persons/{personId}` – информация о человеке;
* `GET /api/v1/persons` – информация по всем людям;
* `POST /api/v1/persons` – создание новой записи о человеке;
* `PATCH /api/v1/persons/{personId}` – обновление существующей записи о человеке;
* `DELETE /api/v1/persons/{personId}` – удаление записи о человеке.

[Описание API](person-service.yaml) в формате OpenAPI.

### Требования

* Исходный проект хранится на Github. Для сборки использовать
  _только_ [Github Actions](https://docs.github.com/en/actions).
* Запросы / ответы должны быть в формате JSON.
* Если запись по id не найдена, то возвращать HTTP статус 404 Not Found.
* При создании новой записи о человека (метод POST /person) возвращать HTTP статус 201 Created с пустым телом и
  Header `Location: /api/v1/persons/{personId}`, где `personId` – id созданной записи.
* Приложение должно содержать 4-5 unit-тестов на реализованные операции.
* Приложение должно быть завернуто в Docker.
* Деплой на Render.com реализовать средствами GitHub Actions, для деплоя использовать docker. Для деплоя _нельзя_
  использовать Heroku CLI или webhooks.
* В [build.yml](build.yml) дописать шаги на сборку, прогон unit-тестов и деплой на Render.com.
* Приложение должно использовать БД для хранения записей.
* В [[inst][heroku] Lab1.postman_environment.json](postman/%5Binst%5D%5Bheroku%5D%20Lab1.postman_environment.json)
  заменить значение `baseUrl` на адрес развернутого сервиса на Render.com.

### Пояснения

* [Пример](https://github.com/Romanow/person-service) приложения на Kotlin / Spring.
* Для локальной разработки можно использовать Postgres в docker, для этого нужно запустить `docker compose up -d`,
  поднимется контейнер с Postgres 13, будет создана БД `persons` и пользователь `program:test`.
* После успешного деплоя на Render.com, через newman запускаются интеграционные тесты. Интеграционные тесты можно проверить
  локально, для этого нужно импортировать в Postman
  коллекцию [lab1.postman_collection.json](postman/%5Binst%5D%20Lab1.postman_collection.json)]) и
  environment [[local] lab1.postman_environment.json](postman/%5Binst%5D%5Blocal%5D%20Lab1.postman_environment.json).
* Для поиска нужного инструмента для сборки используется [Github Marketplace](https://github.com/marketplace).
* Пояснение как работает [Render.com](https://render.com/docs).
* Для подключения БД на Render.com заходите через Dashboard в раздел Databases и создаете новую PostgreSQL базу данных.
  Для получения адреса, пользователя и пароля переходите в саму БД и выбираете раздел `Info` -> `Connection Details`.

### Прием задания

1. При получении задания у вас создается fork этого репозитория для вашего пользователя.
2. После того как все тесты успешно завершатся, в Github Classroom на Dashboard будет отмечен успешный прогон тестов.
3. Для деплоя на Render.com необходимо создать аккаунт и настроить GitHub Actions secrets:
   - `RENDER_SERVICE_ID` - ID сервиса на Render.com
   - `RENDER_API_KEY` - API ключ для Render.com

### Развертывание на Render.com

1. Создайте аккаунт на [Render.com](https://render.com)
2. Создайте новую PostgreSQL базу данных в разделе "Databases"
3. Создайте новый Web Service, выбрав "Deploy from GitHub Repository"
4. Укажите ваш репозиторий и настройте:
   - Build Command: `docker build -t person-service .`
   - Start Command: `docker run -p 10000:8000 person-service`
   - Environment Variables: `DATABASE_URL` (из настроек базы данных)
5. Получите Service ID из URL вашего сервиса
6. Создайте API ключ в настройках аккаунта
7. Добавьте secrets в GitHub:
   - `RENDER_SERVICE_ID`
   - `RENDER_API_KEY`
8. Обновите `baseUrl` в Postman environment файле на URL вашего сервиса 

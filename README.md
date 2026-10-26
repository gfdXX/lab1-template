# РСОИ, ЛР1: CI/CD для REST-сервиса Person

![Python](https://img.shields.io/badge/Python-FastAPI-009688?logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-SQLModel-4169E1?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-compose-2496ED?logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-CI%2FCD-2088FF?logo=githubactions&logoColor=white)

Лабораторная работа №1 по курсу «Распределённые системы обработки информации», МГТУ им. Н.Э. Баумана (осень 2025).
Условие задания (с поправкой на Render вместо Heroku) — в [ASSIGNMENT.md](ASSIGNMENT.md).

## Что сделано

- REST-сервис на **FastAPI + SQLModel + PostgreSQL** ([`src/person/main.py`](src/person/main.py)) с CRUD над сущностью Person: `GET/POST /api/v1/persons`, `GET/PATCH/DELETE /api/v1/persons/{id}` по спецификации [person-service.yaml](person-service.yaml);
- [`Dockerfile`](Dockerfile) и [`docker-compose.yml`](docker-compose.yml) (сервис + PostgreSQL), отдельный [`docker-compose.tests.yml`](docker-compose.tests.yml) для тестов;
- вместо Heroku сервис разворачивается на Render по описанию [`render.yaml`](render.yaml);
- [GitHub Actions](.github/workflows/classroom.yml): сборка Docker-образов, unit-тесты на `pytest` ([`main_test.py`](src/person/main_test.py)) и интеграционные тесты Postman (Newman) против развёрнутого на Render сервиса.

## Запуск локально

```bash
git clone https://github.com/gfdXX/lab1-template.git
cd lab1-template
docker compose up --build        # сервис на http://localhost:8000, Swagger — /docs
```

## Автор

Салженикин Даниил, МГТУ им. Н.Э. Баумана.

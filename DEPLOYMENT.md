# Инструкция по деплою на Render.com

## Предварительные требования

1. ✅ Аккаунт на [Render.com](https://render.com)
2. ✅ GitHub репозиторий с кодом
3. ✅ Настроенные GitHub Secrets

## Пошаговая инструкция

### 1. Создание Web Service на Render.com

1. Войдите в [Render Dashboard](https://dashboard.render.com)
2. Нажмите "New +" → "Web Service"
3. Выберите "Build and deploy from a Git repository"
4. Подключите ваш GitHub репозиторий
5. Настройте сервис:
   - **Name**: `person-service`
   - **Environment**: `Docker`
   - **Dockerfile Path**: `./Dockerfile`
   - **Port**: `8000`

### 2. Создание PostgreSQL базы данных

1. Нажмите "New +" → "PostgreSQL"
2. Настройте базу:
   - **Name**: `person-db`
   - **Database**: `persons`
   - **User**: `program`
   - **Plan**: Free
3. Скопируйте **External Database URL**

### 3. Настройка переменных окружения

В настройках Web Service добавьте:
- **Key**: `DATABASE_URL`
- **Value**: строка подключения к БД

### 4. Получение Service ID и API ключа

#### Service ID:
- URL сервиса: `https://dashboard.render.com/web/srv-XXXXXXXXXX`
- Service ID = `srv-XXXXXXXXXX`

#### API ключ:
1. Account Settings → API Keys
2. Create API Key
3. Скопируйте ключ

### 5. Настройка GitHub Secrets

В GitHub репозитории:
1. Settings → Secrets and variables → Actions
2. Добавьте secrets:
   - `RENDER_SERVICE_ID` = Service ID
   - `RENDER_API_KEY` = API ключ

### 6. Тестирование деплоя

1. Сделайте commit и push в ветку `main`
2. Проверьте GitHub Actions:
   - Перейдите в Actions tab
   - Убедитесь, что workflow выполнился успешно
3. Проверьте Render.com:
   - Сервис должен автоматически обновиться
   - Проверьте логи деплоя

### 7. Обновление Postman Environment

Замените в файле `postman/[inst][heroku] Lab1.postman_environment.json`:
```json
{
  "key": "baseUrl",
  "value": "https://your-actual-service-name.onrender.com"
}
```

## Проверка работоспособности

После успешного деплоя проверьте:

1. **API документация**: `https://your-service.onrender.com/docs`
2. **Создание записи**:
   ```bash
   curl -X POST "https://your-service.onrender.com/api/v1/persons" \
        -H "Content-Type: application/json" \
        -d '{"name": "Test User", "age": 25, "city": "Moscow"}'
   ```
3. **Получение записей**:
   ```bash
   curl "https://your-service.onrender.com/api/v1/persons"
   ```

## Troubleshooting

### Проблемы с деплоем:
- Проверьте логи в Render Dashboard
- Убедитесь, что GitHub Secrets настроены правильно
- Проверьте, что DATABASE_URL корректный

### Проблемы с базой данных:
- Убедитесь, что база данных создана и запущена
- Проверьте строку подключения
- Убедитесь, что переменная DATABASE_URL установлена

### Проблемы с GitHub Actions:
- Проверьте, что workflow файл находится в `.github/workflows/`
- Убедитесь, что secrets добавлены в репозиторий
- Проверьте логи выполнения workflow

# Cyber forum

---
### Загрузка
```shell
git clone https://github.com/ayanaakhh/cyber-forum.git
```
```shell
cd cyber-forum
```

### Настройка зависимостей

Cкопировать содержимое `.env.example` в файл `.env` и указать зависмости

```
cp example.env .env
```

### Скачивание необходимых библиотек и пакетов

```shell
pip install -r requirements.txt
```

### Миграции

```shell
python manage.py makemigrations && python manage.py migrate
```
### Создание супер-пользователя
```shell
python manage.py createsuperuser
```

### Запуск

```shell
python manage.py runserver
```

### Парсеры

```shell
python manage.py parse_news
python manage.py parse_posts
```


---

Stack: `Django`, `Bootstrap5`, `Jinja2`

# Scanity

## Описание
Приложение для анализа снимков КТ ОГК на основе искусственного интеллекта для автоматической классификации патологий.

<img alt="dashboard_screenshot" src="https://github.com/user-attachments/assets/54ff2e01-d8b1-4bee-a943-00a0ae766c12" />

Снимки экрана: https://github.com/


## Основные возможности
Приложение предоставляет удобный интерфейс для анализа снимков КТ в форматах .dcm, .png, .jpeg. Возможна массовая загрузка снимков через архивы .zip.

## Системные требования для запуска
* Оперативная память: от 4 ГБ (8 ГБ рекомендовано)
* Ядра ЦП: 2 (4 рекомендовано)
* Место на диске: от 20 ГБ

## Quick start
1. ```git clone https://github.com/gnegDev/scanity.git```
2. ```cd scanity```
3. ```docker compose up```
4. Приложение будет доступно на https://localhost:5000/
<br/><br/>

## Структура проекта
* scanityInterface/: веб-приложение Flask на Python, предоставляющее веб-интерфейс
* scanityCore/: веб-сервис Spring Boot на
Java, исполняющий обработку данных и управляющий БД PostgreSQL и S3 (хранилище файлов) MinIO
* scanityModel/: модель ИИ на Python, выполняющая основной анализ снимков КТ

## Руководство по развертыванию
https://github.com/

## Руководство пользователя
https://github.com/

###### Mazut Production

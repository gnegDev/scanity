# Scanity | Сканити

## Описание
Приложение для анализа снимков КТ ОГК на основе искусственного интеллекта для автоматической классификации патологий.

<img alt="dashboard_page" src="https://github.com/user-attachments/assets/9a31aca4-f3ca-4d6f-9149-d2ae960ecb01" />

[Снимки экрана](https://github.com/gnegDev/scanity/wiki/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BA%D0%B8-%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0)


## Основные возможности
Приложение предоставляет удобный интерфейс для анализа и классификации с помощью ИИ снимков КТ в форматах .dcm, .png, .jpeg. Возможна массовая загрузка снимков через архивы .zip. Имеется возможность скачивания отчёта о выполненном анализе.

## Системные требования для запуска
* Оперативная память: от 4 ГБ (8 ГБ рекомендовано)
* Ядра ЦП: от 2 (4 рекомендовано)
* Место на диске: от 20 ГБ
* Docker
* Git

## Quick start
1. ```git clone https://github.com/gnegDev/scanity.git```
2. ```cd scanity```
3. ```docker compose up --build```
4. Приложение будет доступно на http://localhost:5000/
<br/><br/>

## Структура проекта
* ```scanityInterface/```: веб-приложение Flask на Python, предоставляющее веб-интерфейс
* ```scanityCore/```: веб-сервис Spring Boot на
Java, исполняющий обработку данных и управляющий БД PostgreSQL и S3 (хранилище файлов) MinIO
* ```scanityModel/```: модель ИИ на Python, использующая PyTorch и выполняющая основной анализ снимков КТ
  + https://drive.google.com/file/d/11iFTB_e6G4XAOlbZCS0rTVKr3RFkiohf/view?usp=sharing: архив с тренером модели и тренировочными данными

## Руководство по развертыванию
[Руководство по развертыванию](https://github.com/gnegDev/scanity/wiki/%D0%A0%D1%83%D0%BA%D0%BE%D0%B2%D0%BE%D0%B4%D1%81%D1%82%D0%B2%D0%BE-%D0%BF%D0%BE-%D1%80%D0%B0%D0%B7%D0%B2%D0%B5%D1%80%D1%82%D1%8B%D0%B2%D0%B0%D0%BD%D0%B8%D1%8E)

## Руководство пользователя
[Руководство пользователя](https://github.com/gnegDev/scanity/wiki/%D0%A0%D1%83%D0%BA%D0%BE%D0%B2%D0%BE%D0%B4%D1%81%D1%82%D0%B2%D0%BE-%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D1%82%D0%B5%D0%BB%D1%8F)

###### Mazut Production 2025

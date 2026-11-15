# ci-cd-lab-7

Лабораторная работа №7: простой CI/CD пайплайн на GitHub Actions.

При каждом пуше в репозиторий GitHub автоматически запускает тесты
из лабораторной №6 (Selenium + pytest, форма поиска Яндекса).

## Структура

```
ci-cd-lab-7/
├── .github/workflows/tests.yml      # пайплайн CI/CD
├── pages/yandex_form_page.py        # Page Object
├── tests/test_yandex_form.py        # тесты формы поиска
├── tests/test_smoke.py              # проверка, что браузер запускается
├── conftest.py                      # фикстуры pytest
├── pytest.ini
└── requirements.txt
```

## Что делает пайплайн

1. Клонирует репозиторий.
2. Устанавливает Python 3.12 (Google Chrome на раннере уже есть).
3. Устанавливает зависимости из `requirements.txt`.
4. Запускает `pytest tests/ -v -n 2 --alluredir=allure-results`
   (параллельно в 2 процесса, Chrome без окна).
5. Сохраняет `allure-results` как артефакт.

Файл пайплайна лежит в `.github/workflows/`: это формат GitHub Actions,
аналог `.gitlab-ci.yml` из методички.

## Локальный запуск

```
pip install -r requirements.txt
pytest tests/ -v
pytest tests/ -v -n 2 --alluredir=allure-results
allure serve allure-results
```

## Про капчу

Яндекс иногда показывает проверку «Вы не робот?» вместо страницы.
В этом случае тест помечается как SKIPPED с причиной в логе: это защита
сайта, а не ошибка в коде.

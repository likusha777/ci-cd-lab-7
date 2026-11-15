import allure


@allure.suite("Проверка окружения")
@allure.title("Браузер запускается и открывает страницу")
def test_browser_starts(browser):
    """Не зависит от внешних сайтов: показывает, что Chrome и Selenium
    в пайплайне установлены и работают."""
    browser.get("data:text/html,<title>CI smoke</title><h1>ok</h1>")
    assert browser.title == "CI smoke"

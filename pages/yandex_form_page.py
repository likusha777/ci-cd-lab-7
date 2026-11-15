import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class YandexFormPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

        # Локаторы элементов формы
        self.SEARCH_INPUT = (By.ID, "text")
        self.SUGGEST_LIST = (By.CSS_SELECTOR, ".mini-suggest__popup-content")
        self.SEARCH_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
        self.SEARCH_RESULTS = (By.CSS_SELECTOR, "#search-result .serp-item")
        self.FIRST_RESULT_LINK = (By.CSS_SELECTOR, "#search-result .serp-item a")

    def is_captcha_shown(self):
        """Показал ли Яндекс проверку «Вы не робот?» вместо страницы"""
        return "captcha" in self.driver.current_url.lower()

    def _wait_until(self, condition):
        """Явное ожидание. Если вместо страницы открылась капча, тест
        пропускается (SKIPPED): это защита сайта, а не ошибка в тесте."""
        try:
            return self.wait.until(condition)
        except TimeoutException:
            if self.is_captcha_shown():
                pytest.skip("Яндекс показал капчу: проверка невозможна")
            raise

    def open_page(self, url):
        """Открыть указанный URL"""
        self.driver.get(url)

    def enter_search_text(self, text):
        """Ввести текст в поисковую строку"""
        search_input = self._wait_until(
            EC.element_to_be_clickable(self.SEARCH_INPUT)
        )
        search_input.clear()
        search_input.send_keys(text)
        return self

    def wait_for_suggest(self):
        """Дождаться появления списка подсказок"""
        self._wait_until(
            EC.visibility_of_element_located(self.SUGGEST_LIST)
        )
        return self

    def click_search_button(self):
        """Нажать кнопку поиска"""
        search_button = self._wait_until(
            EC.element_to_be_clickable(self.SEARCH_BUTTON)
        )
        search_button.click()
        return self

    def wait_for_search_results(self):
        """Дождаться появления результатов поиска"""
        self._wait_until(
            EC.visibility_of_element_located(self.SEARCH_RESULTS)
        )
        return self

    def get_first_result_text(self):
        """Получить текст первого результата поиска"""
        first_result = self._wait_until(
            EC.visibility_of_element_located(self.FIRST_RESULT_LINK)
        )
        return first_result.text

    def perform_search(self, search_text):
        """Выполнить полный цикл поиска"""
        (self.enter_search_text(search_text)
            .wait_for_suggest()
            .click_search_button()
            .wait_for_search_results())
        return self

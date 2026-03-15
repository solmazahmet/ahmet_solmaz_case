from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from pages.base_page import BasePage
from config.config import TIMEOUT


class OpenPositionsPage(BasePage):

    JOB_CARDS = (By.CSS_SELECTOR, ".posting")
    JOB_TITLE = (By.CSS_SELECTOR, ".posting-title h5")
    JOB_LOCATION = (By.CSS_SELECTOR, ".sort-by-location")
    JOB_LINK = (By.CSS_SELECTOR, "a.posting-title")
    GROUP_HEADER = (By.CSS_SELECTOR, ".postings-group .posting-category-title")
    APPLY_BUTTON = (By.CSS_SELECTOR, "a.postings-btn")

    FILTER_BUTTONS = (By.CSS_SELECTOR, ".filter-button")

    def filter_by_location(self, location):
        buttons = self.find_all(self.FILTER_BUTTONS)
        # second filter button is LOCATION
        loc_btn = buttons[1]
        loc_btn.click()
        option = (By.XPATH, f"//div[contains(@class, 'filter-popup')]//a[contains(text(), '{location}')]")
        self.click(option)
        WebDriverWait(self.driver, TIMEOUT).until(
            EC.presence_of_element_located(self.JOB_CARDS)
        )

    def wait_for_jobs_to_load(self):
        self.find(self.JOB_CARDS)

    def get_job_list(self):
        try:
            return self.find_all(self.JOB_CARDS)
        except TimeoutException:
            return []

    def get_job_positions(self):
        cards = self.get_job_list()
        result = []
        for card in cards:
            try:
                title = card.find_element(*self.JOB_TITLE)
                result.append(title.text.strip())
            except NoSuchElementException:
                continue
        return result

    def get_job_departments(self):
        try:
            headers = self.driver.find_elements(*self.GROUP_HEADER)
            return [h.text.strip() for h in headers if h.text.strip()]
        except NoSuchElementException:
            return []

    def get_job_locations(self):
        cards = self.get_job_list()
        result = []
        for card in cards:
            try:
                loc = card.find_element(*self.JOB_LOCATION)
                result.append(loc.text.strip())
            except NoSuchElementException:
                continue
        return result

    def click_view_role(self, index=0):
        cards = self.get_job_list()
        if cards and index < len(cards):
            link = cards[index].find_element(*self.JOB_LINK)
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", link
            )
            self.driver.execute_script("arguments[0].click();", link)

    def is_job_list_present(self):
        return len(self.get_job_list()) > 0

    def get_job_count(self):
        return len(self.get_job_list())

    def is_apply_button_present(self):
        return self.is_displayed(self.APPLY_BUTTON)

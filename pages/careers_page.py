from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from pages.base_page import BasePage
from config.config import CAREERS_URL, LEVER_QA_URL, TIMEOUT


class CareersPage(BasePage):

    DEPT_LINKS = (By.CSS_SELECTOR, "a.insiderone-icon-cards-grid-item-btn")
    SEE_ALL_TEAMS = (By.CSS_SELECTOR, "a.see-more")
    QA_CARD = (
        By.XPATH,
        "//div[contains(@class, 'insiderone-icon-cards-grid-item')]"
        "//h3[contains(text(), 'Quality Assurance')]",
    )
    QA_JOBS_LINK = (
        By.XPATH,
        "//h3[contains(text(), 'Quality Assurance')]"
        "/ancestor::div[contains(@class, 'insiderone-icon-cards-grid-item')]"
        "//a[contains(@class, 'insiderone-icon-cards-grid-item-btn')]",
    )

    def open_careers_page(self):
        self.open(CAREERS_URL)
        self.accept_cookies()

    def click_see_all_qa_jobs(self):
        self.scroll_to_element(self.SEE_ALL_TEAMS)
        self.js_click(self.SEE_ALL_TEAMS)
        WebDriverWait(self.driver, TIMEOUT).until(
            EC.visibility_of_element_located(self.QA_CARD)
        )
        # position data is loaded async from Lever API; wait for QA link href
        try:
            WebDriverWait(self.driver, TIMEOUT).until(
                lambda d: "lever.co" in (
                    d.find_element(*self.QA_JOBS_LINK).get_attribute("href") or ""
                )
            )
            self.scroll_to_element(self.QA_JOBS_LINK)
            self.js_click(self.QA_JOBS_LINK)
        except TimeoutException:
            # Lever API didn't respond in time, navigate directly
            self.open(LEVER_QA_URL)

    def is_qa_department_visible(self):
        return self.is_displayed(self.QA_CARD)

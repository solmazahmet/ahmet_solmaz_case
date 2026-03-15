from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from config.config import BASE_URL


class HomePage(BasePage):

    NAVBAR = (By.CSS_SELECTOR, "header#navigation")
    HERO_SECTION = (By.CSS_SELECTOR, "section.homepage-hero")
    CUSTOMER_LOGOS = (By.CSS_SELECTOR, ".homepage-hero-logo-reel")
    FOOTER = (By.CSS_SELECTOR, "footer#footer")

    def open_home_page(self):
        self.open(BASE_URL)
        self.accept_cookies()

    def is_home_page_loaded(self):
        return all([
            self.is_navbar_displayed(),
            self.is_hero_section_displayed(),
            self.is_partners_section_displayed(),
            self.is_footer_displayed()
        ])

    def is_navbar_displayed(self):
        return self.is_displayed(self.NAVBAR)

    def is_hero_section_displayed(self):
        return self.is_displayed(self.HERO_SECTION)

    def is_partners_section_displayed(self):
        return self.is_displayed(self.CUSTOMER_LOGOS)

    def is_footer_displayed(self):
        return self.is_displayed(self.FOOTER)

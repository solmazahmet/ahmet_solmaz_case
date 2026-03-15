import pytest

from pages.home_page import HomePage
from pages.careers_page import CareersPage
from pages.open_positions_page import OpenPositionsPage


@pytest.mark.ui
class TestInsiderCareers:

    def _setup_careers_and_filter(self, driver):
        """Navigate to careers, open QA jobs, filter by Istanbul + QA."""
        careers = CareersPage(driver)
        careers.open_careers_page()
        careers.click_see_all_qa_jobs()

        positions = OpenPositionsPage(driver)
        positions.wait_for_jobs_to_load()
        positions.filter_by_location("Istanbul")
        return positions

    def test_home_page_is_loaded(self, driver):
        """Visit insiderone.com and verify main page sections are visible."""
        home = HomePage(driver)
        home.open_home_page()

        assert home.is_navbar_displayed(), "Navbar should be visible"
        assert home.is_hero_section_displayed(), "Hero section should be visible"
        assert home.is_partners_section_displayed(), "Partners logo reel should be visible"
        assert home.is_footer_displayed(), "Footer should be visible"

    def test_careers_qa_page_and_filter_jobs(self, driver):
        """Navigate to Careers > QA, filter by Istanbul + QA, check job list."""
        positions = self._setup_careers_and_filter(driver)
        assert positions.is_job_list_present(), "Job list should be visible after filtering"

    def test_job_details_contain_correct_info(self, driver):
        """Each job's Position, Department, and Location should match filters."""
        positions = self._setup_careers_and_filter(driver)

        job_positions = positions.get_job_positions()
        job_departments = positions.get_job_departments()
        job_locations = positions.get_job_locations()

        assert len(job_positions) > 0, "At least one QA job should be listed"

        for pos in job_positions:
            assert "QA" in pos or "Quality Assurance" in pos, \
                f"Position '{pos}' should contain 'Quality Assurance'"

        for dept in job_departments:
            assert "Quality Assurance" in dept.title(), \
                f"Department '{dept}' should contain 'Quality Assurance'"

        for loc in job_locations:
            assert "istanbul" in loc.lower(), \
                f"Location '{loc}' should contain 'Istanbul, Turkey'"

    def test_view_role_redirects_to_lever(self, driver):
        """Click View Role and verify redirect to Lever application page."""
        positions = self._setup_careers_and_filter(driver)
        positions.click_view_role()

        current_url = positions.get_current_url()
        assert "jobs.lever.co" in current_url, \
            f"Should be on Lever page, got '{current_url}'"
        assert positions.is_apply_button_present(), \
            "Apply button should be visible on application page"

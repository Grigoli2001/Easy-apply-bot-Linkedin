# job_search.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time


class JobSearch:
    def __init__(self, browser):
        self.driver = browser.driver
        self.easy_apply_listings = []

    def wait(self, seconds):
        print(f"Waiting for {seconds} seconds...")
        time.sleep(seconds)

    def search_for_jobs(self, description, location="France"):
        try:
            description_input_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "input[id^='jobs-search-box-keyword']")
                )
            )
            description_input_element.clear()
            description_input_element.send_keys(description)

            location_input_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "input[id^='jobs-search-box-location']")
                )
            )
            location_input_element.clear()
            location_input_element.send_keys(location)
        except Exception as e:
            print(f"Error while searching: {e}")

        self.wait(3)
        location_input_element.send_keys(Keys.ENTER)
        print(f"Searched for: {description}")
        self.wait(2)

    def filter_easy_apply(self):
        try:
            easy_apply_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "button[aria-label='Easy Apply filter.']")
                )
            )
            easy_apply_button.click()
            print("Filtered to show only 'Easy Apply' jobs.")
            self.wait(2)
        except Exception as e:
            print(f"Error while filtering: {e}")

    def get_job_listings(self):
        job_listings = []
        try:
            job_listings = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "li.jobs-search-results__list-item")
                )
            )
            print(f"Found {len(job_listings)} job listings.")
        except Exception as e:
            print(f"Error while getting job listings: {e}")

        for job_listing in job_listings:
            if self.is_easy_apply(job_listing):
                self.easy_apply_listings.append(job_listing)

        print(f"Found {len(self.easy_apply_listings)} job listings with 'Easy Apply' option.")
        return self.easy_apply_listings

    def is_easy_apply(self, job_listing):
        try:
            apply_method = job_listing.find_element(
                By.CSS_SELECTOR, "li.job-card-container__apply-method"
            )
            return True if apply_method else False
        except:
            return False

    def click_all_easy_apply(self):
        for job_listing in self.easy_apply_listings:
            try:
                job_listing.click()
                print("Clicked on 'Easy Apply' job listing.")
                self.wait(5)
            except Exception as e:
                print(f"Error while clicking: {e}")

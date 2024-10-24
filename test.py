from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time


class LinkedIn:
    def __init__(self, user_data_dir=None, profile_dir="Default"):
        self.easy_apply_listings = []
        chrome_options = Options()

        if user_data_dir:
            chrome_options.add_argument(f"user-data-dir={user_data_dir}")
            chrome_options.add_argument(f"profile-directory={profile_dir}")

        chrome_options.add_argument(
            "--remote-debugging-port=9222"
        )  # To prevent conflicts
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--enable-unsafe-webgl")
        chrome_options.add_argument("--disable-webgl")
        chrome_options.add_argument("--disable-webrtc")
        chrome_options.add_experimental_option("detach", True)

        caps = DesiredCapabilities.CHROME
        caps["goog:loggingPrefs"] = {"browser": "SEVERE"}

        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service, options=chrome_options)

    def wait(self, seconds):
        print(f"Waiting for {seconds} seconds...")
        time.sleep(seconds)

    def open_new_tab(self, url):
        """Open a new tab and navigate to the specified URL."""
        try:
            self.driver.execute_script("window.open('');")

            window_handles = self.driver.window_handles

            self.driver.switch_to.window(window_handles[-1])

            self.driver.get(url)
            print(f"Opened new tab and navigated to: {url}")

        except Exception as e:
            print(f"Error while opening new tab: {e}")

    def open_page(self, url):
        """Open a webpage by URL."""
        self.driver.get(url)
        print(f"Opened page: {url}")
        self.wait(3)
        self.accept_cookies()

    def accept_cookies(self):
        try:
            self.driver.find_element(By.ID, "L2AGLb").click()
            print("Accepted cookies.")
        except:
            print("No cookies popup found.")

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
        # submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[class^='jobs-search-box__submit-button']")
        # submit_button.click()
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
            print(job_listings)
        except Exception as e:
            print(f"Error while getting job listings: {e}")
        for job_listing in job_listings:
            if self.is_easy_apply(job_listing):
                self.easy_apply_listings.append(job_listing)
        print(
            f"Found {len(self.easy_apply_listings)} job listings with 'Easy Apply' option."
        )
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

    def quit(self):
        self.driver.quit()
        print("Browser closed.")


browser = LinkedIn("C:\\Users\\gega\\AppData\\Local\\Google\\Chrome\\User Data")


browser.open_new_tab("https://www.linkedin.com/jobs/")
browser.search_for_jobs("Python", "France")
browser.filter_easy_apply()

job_listings = browser.get_job_listings()

browser.click_all_easy_apply()



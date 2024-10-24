# browser.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class Browser:
    def __init__(self, user_data_dir=None, profile_dir="Default"):
        chrome_options = Options()

        if user_data_dir:
            chrome_options.add_argument(f"user-data-dir={user_data_dir}")
            chrome_options.add_argument(f"profile-directory={profile_dir}")

        chrome_options.add_argument("--remote-debugging-port=9222")
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

    def open_new_tab(self, url):
        try:
            self.driver.execute_script("window.open('');")
            window_handles = self.driver.window_handles
            self.driver.switch_to.window(window_handles[-1])
            self.driver.get(url)
            print(f"Opened new tab and navigated to: {url}")
        except Exception as e:
            print(f"Error while opening new tab: {e}")

    def quit(self):
        self.driver.quit()
        print("Browser closed.")

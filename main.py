# main.py
from linkedin_bot.browser import Browser
from linkedin_bot.job_search import JobSearch

def main():
    browser = Browser("C:\\Users\\gega\\AppData\\Local\\Google\\Chrome\\User Data")

    job_search = JobSearch(browser)

    browser.open_new_tab("https://www.linkedin.com/jobs/")
    job_search.search_for_jobs("Python", "France")

    job_search.filter_easy_apply()

    job_search.get_job_listings()

    job_search.click_all_easy_apply()

    # browser.quit()

if __name__ == "__main__":
    main()

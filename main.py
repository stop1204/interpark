import logging
import os
import traceback
from tkinter import *

from selenium import webdriver as driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# import cloudscraper
# scraper = cloudscraper.create_scraper()
# response = scraper.get('https://www.globalinterpark.com/en/login')
# print(response.text)


chrome_options = driver.ChromeOptions()
chrome_options.add_argument("--disable-notifications")
chrome_options_path = os.path.join(os.getcwd(), "chrome_profile")
chrome_options.add_argument(f"user-data-dir={chrome_options_path}")
chrome_options.add_argument("--disable-gpu")


# these is for bypassing the bot detection of the website
# chrome_options.headless = True
# chrome_options.add_argument("start-maximized")
# # //use_subprocess=False
# chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
# chrome_options.add_argument("--disable-blink-features=AutomationControlled")
# chrome_options.add_argument("--disable-extensions")


class BrowserSimulator:
    def __init__(self, root):
        print("Browser Simulator")
        self.root = root
        self.root.title("Browser Simulator")
        self.driver = driver.Chrome(options=chrome_options)
        self.driver.get('https://www.globalinterpark.com/en/login')
        self.create_ui()
        self.login_facebook()
        self.navigate_to_url_concert()

    def create_ui(self):
        self.frame = Frame(self.root)
        self.frame.grid(row=0, column=0, padx=10, pady=10)

        # URL Input
        self.label_url = Label(self.frame, text="URL to Visit")
        self.label_url.grid(row=0, column=0)
        self.url_entry = Entry(self.frame, width=50)
        self.url_entry.insert(0, 'https://www.globalinterpark.com/en/login')
        self.url_entry.grid(row=0, column=1, columnspan=3, pady=5)

        self.visit_button = Button(self.frame, text="Visit URL", command=self.visit_url)
        self.visit_button.grid(row=0, column=4, padx=10)

        # XPath Input
        self.label_xpath = Label(self.frame, text="XPath of Element")
        self.label_xpath.grid(row=1, column=0)
        self.xpath_entry = Entry(self.frame, width=50)
        self.xpath_entry.insert(0, '//*[@id="someElement"]')
        self.xpath_entry.grid(row=1, column=1, columnspan=3, pady=5)

        self.click_button = Button(self.frame, text="Click Element", command=self.click_element)
        self.click_button.grid(row=1, column=4, padx=10)

        # take screen shoot
        self.take_screen = Button(self.frame, text="Take Screen", command=self.take_screen)
        self.take_screen.grid(row=2, column=4, padx=10)

        # click login facebook button
        # XPath Input
        self.label_xpath = Label(self.frame, text="XPath of Facebook Login Button")
        self.label_xpath.grid(row=3, column=0)
        self.xpath_entry = Entry(self.frame, width=50)
        self.xpath_entry.insert(0, '/html/body/div/main/div[3]/div/div[2]/a[1]/img')
        self.xpath_entry.grid(row=3, column=1, columnspan=3, pady=5)

        self.click_button = Button(self.frame, text="Click Facebook Login", command=self.login_facebook)
        self.click_button.grid(row=3, column=4, padx=10)

        # Add additional input box for the URL to navigate after login
        self.label_new_url = Label(self.frame, text="URL to Navigate After Login")
        self.label_new_url.grid(row=4, column=0)
        self.concert_url_entry = Entry(self.frame, width=50)
        self.concert_url_entry.insert(0, 'https://www.globalinterpark.com/en/product/24008203')
        self.concert_url_entry.grid(row=4, column=1, columnspan=3, pady=5)
        self.navigate_button = Button(self.frame, text="Navigate to concert page", command=self.navigate_to_url_concert)
        self.navigate_button.grid(row=4, column=4, padx=10)

    def navigate_to_url_concert(self):
        try:
            new_url = self.concert_url_entry.get()
            # wait url drive to load
            WebDriverWait(self.driver, 10).until(
                EC.url_contains("https://www.globalinterpark.com/en")
            )

            self.driver.get(new_url)
        except Exception as e:
            logging.error(f"Error navigating to URL: {e}")
            logging.error(traceback.format_exc())
            print(f"Error navigating to URL: {e}")

    def login_facebook(self):
        try:
            xpath = self.xpath_entry.get()
            # Wait for the Facebook login button to be present and then click it
            fb_login_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            fb_login_button.click()
        except Exception as e:
            logging.error(f"Error clicking element: {e}")
            logging.error(traceback.format_exc())
            print(f"Error clicking element: {e}")

    def take_screen(self):
        self.driver.save_screenshot("screen.png")

    def visit_url(self):
        try:
            url = self.url_entry.get()
            self.driver.get(url)
        except Exception as e:
            logging.error(f"Error visiting URL: {e}")
            logging.error(traceback.format_exc())
            print(f"Error visiting URL: {e}")

    def click_element(self):
        try:
            xpath = self.xpath_entry.get()
            element = self.driver.find_element(By.XPATH, xpath)
            element.click()
        except Exception as e:
            logging.error(f"Error clicking element: {e}")
            logging.error(traceback.format_exc())
            print(f"Error clicking element: {e}")


if __name__ == "__main__":
    root = Tk()
    app = BrowserSimulator(root)
    root.mainloop()

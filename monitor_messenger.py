#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
from options import email, passwd, profile_link, total_time, freq


class ActivityCheckBot:

    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_argument('headless')
        chrome_options.add_experimental_option("prefs", prefs)

        self.driver = webdriver.Chrome(chrome_options=chrome_options)

    def login(self):
        self.driver.get(profile_link)

        email_box = self.driver.find_element_by_xpath('//*[@id="email"]')
        email_box.send_keys(email)
        passwd_box = self.driver.find_element_by_xpath('//*[@id="pass"]')
        passwd_box.send_keys(passwd)

        login_btn = self.driver.find_element_by_xpath('//*[@id="loginbutton"]')
        login_btn.click()

    def uncheck_message_box(self):
        """
        Purpose of this function is to move cursor to other place than the entry box for message.
        """
        try:
            empty_space = WebDriverWait(self.driver, 5).until(ec.presence_of_element_located((By.CLASS_NAME, '_6ynn')))
            empty_space.click()

        except TimeoutException:
            print("There is something wrong, I cannot access status.")

    def check_activity(self):
        """
        Proper function that checks acivity in loop, with given frequency and for given time.
        """
        loops = total_time/freq
        loop = 0

        while loop <= loops:
            try:
                status = WebDriverWait(self.driver, 5).until(ec.presence_of_element_located((By.CLASS_NAME, '_2v6o')))
            except TimeoutException:
                print("There is something wrong, I cannot access status.")

            current_time = time.strftime("%H:%M:%S", time.localtime())

            status_file = open("status_file.txt", "a+")
            if 'Messenger' in status.text:
                status_file.write("Active;" + current_time + "\n")
            else:
                status_file.write("Inactive;" + current_time + "\n")
            status_file.close()

            loop += 1
            time.sleep(freq)

    def exit_bot(self):
        self.driver.stop_client()
        self.driver.close()


bot = ActivityCheckBot()
bot.login()
bot.uncheck_message_box()
bot.check_activity()
bot.exit_bot()

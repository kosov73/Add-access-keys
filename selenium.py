# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import UnexpectedAlertPresentException
import unittest, time, re, argparse

login= input('Enter your login:')
password = input('Enter your password:')
fd = open('key1.txt')

class web(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://bb.test-pro.online/login?next=/plugins/servlet/ssh/projects/DEN/repos/test/keys"
        self.verificationErrors = []
        self.accept_next_alert = True



    def test_web(self):
        driver = self.driver
        driver.get("https://bb.test-pro.online/login?next=/plugins/servlet/ssh/projects/DEN/repos/test/keys")
        driver.find_element_by_id("j_username").click()
        driver.find_element_by_id("j_username").clear()
        driver.find_element_by_id("j_username").send_keys(login)
        driver.find_element_by_id("content").click()
        driver.find_element_by_id("j_password").click()
        driver.find_element_by_id("j_password").send_keys(password)
        driver.find_element_by_id("submit").click()
        for i in fd:
            r = (''.join(re.findall(r'"ssh([^<>]+)"', i)))
            if len(r) == 0:
                continue
            p = ("ssh"+r)
            driver.find_element_by_id("add-key-button").click()
            driver.find_element_by_id("text").send_keys(p)
            driver.find_element_by_id("submit").click()
            try:
               driver.find_element_by_xpath("//section[@id='content']/div/div/section/form/div")
               driver.find_element_by_id("cancel").click()
            except:
               pass

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True

    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()

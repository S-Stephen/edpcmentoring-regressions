# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
import os

class TestPreferences(unittest.TestCase):
    def setUp(self):
        username = os.environ["SAUCE_USERNAME"]
        access_key = os.environ["SAUCE_ACCESS_KEY"]
        desired_cap = {
            'platform': "Mac OS X 10.9",
            'browserName': "chrome",
            'version': "31",
        }
        hub_url = "%s:%s@localhost:4445" % (username, access_key)
        self.driver = webdriver.Remote(desired_capabilities=desired_cap, command_executor="http://%s/wd/hub" % hub_url)
        self.driver.implicitly_wait(30)
        self.base_url = "https://demo.raven.cam.ac.uk/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_preferences(self):
        driver = self.driver
        driver.get("http://cupcmentoring.herokuapp.com")
        driver.find_element_by_id("userid").clear()
        driver.find_element_by_id("userid").send_keys("test0001")
        driver.find_element_by_id("pwd").clear()
        driver.find_element_by_id("pwd").send_keys("test")
        driver.find_element_by_name("submit").click()
        driver.find_element_by_link_text("Change these preferences").click()
        # ERROR: Caught exception [ERROR: Unsupported command [selectWindow | null | ]]
        self.assertEqual("off", driver.find_element_by_id("id_is_seeking_mentor").get_attribute("value"))
        driver.find_element_by_id("id_is_seeking_mentor").click()
        try: self.assertEqual("on", driver.find_element_by_id("id_is_seeking_mentor").get_attribute("value"))
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_id("submit-id-submit").click()
        driver.find_element_by_link_text("Change these preferences").click()
        driver.find_element_by_id("id_is_seeking_mentor").click()
        driver.find_element_by_id("submit-id-submit").click()
        # ERROR: Caught exception [ERROR: Unsupported command [selectWindow | null | ]]
        driver.find_element_by_link_text("Log out").click()
        driver.get("https://demo.raven.cam.ac.uk/auth/logout.html")
    
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

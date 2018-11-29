"""
This program demonstrates data-driven automation of
security and performance testing for FluentExpress site.
hosted on the public azure cloud. Using admin account.
it automates authentication and creates virtual test users
for further automation of security and performance testing.

Created on Jul 16, 2018

@version 1.0
@author: vlad
"""

# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class FluentAdminActions(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome("chromedriver")
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.katalon.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_fluent_admin_login(self):
        driver = self.driver
        # ERROR: Caught exception [unknown command [#]]
        driver.get("http://fluentexpress-staging.northeurope.cloudapp.azure.com/login")
        driver.find_element_by_name("email").click()
        driver.find_element_by_name("email").clear()
        driver.find_element_by_name("email").send_keys("casusdr@gmail.com")
        driver.find_element_by_name("password").click()
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys("Ro7I6kCW6enbwKm1zJUk")
        driver.find_element_by_xpath("//button").click()
        return driver
        
    def test_fluent_admin_links(self):
        driver = self.test_fluent_admin_login()
        driver.find_element_by_link_text("Administration").click()
        driver.find_element_by_link_text("Editors").click()
        driver.find_element_by_link_text("Add new corrector").click()
        driver.find_element_by_link_text("Log out").click()
    
    def test_fluent_admin_add_corrector(self):
        driver = self.test_fluent_admin_login()
        driver.find_element_by_link_text("Administration").click()
        driver.find_element_by_link_text("Editors").click()
        driver.find_element_by_link_text("Add new corrector").click()
        driver.find_element_by_name("name").click()
        driver.find_element_by_name("name").clear()
        driver.find_element_by_name("name").send_keys("Q A")
        driver.find_element_by_name("short-name").click()
        driver.find_element_by_name("short-name").clear()
        driver.find_element_by_name("short-name").send_keys("qa")
        driver.find_element_by_name("email").click()
        driver.find_element_by_name("email").clear()
        driver.find_element_by_name("email").send_keys("qa@qa.com")
        driver.find_element_by_name("password").click()
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys("321qa")
        driver.find_element_by_name("photo").click()
        driver.find_element_by_name("photo").clear()
        driver.find_element_by_name("photo").send_keys("admin-icon192x192.png")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        driver.find_element_by_xpath("(//a[contains(text(),'Log out')])[2]").click()
    
    def test_fluent_admin_add_correctors(self):
        for i in range(20, 100):
            driver = self.test_fluent_admin_login()
            driver.find_element_by_link_text("Administration").click()
            driver.find_element_by_link_text("Editors").click()
            driver.find_element_by_link_text("Add new corrector").click()
            self.add_new_corrector(i)
            driver.find_element_by_xpath("//button[@type='submit']").click()
            driver.find_element_by_xpath("(//a[contains(text(),'Log out')])[2]").click()


    def test_fluent_admin_login_logout(self):
        driver = self.test_fluent_admin_login()
        driver.find_element_by_xpath("(//a[contains(text(),'Log out')])[2]").click()
    
    def add_new_corrector(self, n):
        names = ['name', 'short-name', 'email', 'password', 'photo']
        values =['Perf Tester' + str(n), 'pt' + str(n), 'pt'+str(n)+'@pt', '321qa', 'perf-tester.png']
        for i in range(len(names)):
            self.driver.find_element_by_name(names[i]).click()
            self.driver.find_element_by_name(names[i]).clear()
            self.driver.find_element_by_name(names[i]).send_keys(values[i])

    # This function defines alternative way for
    # setting up NVPs as items in elements dictionary
    def add_new_corrector_elements(self, n):
        elements = {}
        el_key = "name" + str(n)
        elements[el_key] = "Perf Tester" + str(n)
        el_key = "short-name" + str(n)
        elements[el_key] = "pt" + str(n)
        el_key = "email" + str(n)
        elements[el_key] = "pt" + str(n) + "@pt"
        el_key = "password" + str(n)
        elements[el_key] = "321qa"
        el_key = "photo" + str(n)
        elements[el_key] = "/Users/vlad/temp/perf-tester.png"
        print ("These are Elements items")
        for ekey in elements.keys():
            print(ekey, elements[ekey])
            self.driver.find_element_by_name(ekey).click()
            self.driver.find_element_by_name(ekey).clear()
            self.driver.find_element_by_name(ekey).send_keys(elements[ekey])


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

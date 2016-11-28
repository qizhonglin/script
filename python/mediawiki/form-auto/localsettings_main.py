# !/usr/bin/python
# coding:utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf8')

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from contextlib import contextmanager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import \
    staleness_of


class MediawikiInitializer:
    def __init__(self, url):
        self.url = url
        profile = webdriver.FirefoxProfile()
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference("network.proxy.no_proxies_on", "	localhost, 127.0.0.1, 161.92.142.*;161.92.141.*")
        profile.update_preferences()
        self.browser = webdriver.Firefox(firefox_profile=profile)
        self.browser.implicitly_wait(60*5)  # seconds

    @contextmanager
    def wait_for_page_load(self, timeout=30):
        old_page = self.browser.find_element_by_tag_name('html')
        yield
        WebDriverWait(self.browser, timeout).until(
            staleness_of(old_page)
        )

    def send_keys(self, id, value):
        element = self.browser.find_element_by_id(id)
        element.clear()
        element.send_keys(value)

    def submit(self):
        with self.wait_for_page_load(timeout=10):
            self.browser.find_element_by_name("submit-continue").submit()

    def run(self):
        # http://161.92.142.80:8080
        self.browser.get(self.url)
        with self.wait_for_page_load(timeout=10):
            self.browser.find_element_by_link_text('set up the wiki').click()

        # /mw-config/index.php?page=Language
        self.submit()

        # /mw-config/index.php?page=Welcome
        self.submit()

        # /mw-config/index.php?page=DBConnect
        self.send_keys('mysql_wgDBserver', 'mysql')
        self.send_keys('mysql_wgDBname', 'mediawiki')
        self.send_keys('mysql__InstallUser', 'root')
        self.send_keys('mysql__InstallPassword', 'q')
        self.submit()

        # /mw-config/index.php?page=DBSettings
        self.submit()

        # /mw-config/index.php?page=Name
        self.send_keys('config_wgSitename', 'knowledge-wiki')
        self.send_keys('config__AdminName', 'admin')
        self.send_keys('config__AdminPassword', 'admin123')
        self.send_keys('config__AdminPasswordConfirm', 'admin123')
        self.submit()

        # /mw-config/index.php?page=Options
        self.browser.find_element_by_id('config_wgEnableUploads').click()
        self.submit()

        # /mw-config/index.php?page=Install
        self.submit()

        # /mw-config/index.php?page=Install
        self.submit()

        # /mw-config/index.php?page=Complete
        #download_url = self.url + '/mw-config/index.php?localsettings=1'



if __name__ == '__main__':
    url = "http://161.92.142.80:8080"
    mediawiki = MediawikiInitializer(url)
    mediawiki.run()

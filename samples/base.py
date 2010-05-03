import unittest

import time
import random


class TestUsers(unittest.TestCase):

    def setUp(self):
        self.browser = self._configure_browser()

    def tearDown(self):
        self.browser.shutdown()

    def test_open(self):
        browser.open('/')
        self.assertTrue('Google' in self.browser.page_title)
import unittest

import time
import random


class TestUsers(unittest.TestCase):

    skip = False

    def _configure_browser(self):
        # the base class can't be run, so skip it if it's tried 
        self.skip = True

    def setUp(self):
        self.browser = self._configure_browser()

    def tearDown(self):
        if self.skip:
            return
        self.browser.shutdown()

    def test_open(self):

        if self.skip:
            return

        self.browser.open('/')
        self.assertTrue('Google' in self.browser.page_title)

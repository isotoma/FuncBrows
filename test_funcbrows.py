import unittest

from funcbrows import FuncBrows
import time

class FuncTests(unittest.TestCase):
    
    def test_creation_testbrowser(self):
        f = FuncBrows('testbrowser', 'http://start.ubuntu.com/')
        
    def test_creation_selenium(self):
        f = FuncBrows('*firefox3', 'http://start.ubuntu.com/', host = '192.168.90.130', port = 4444)
        
        
    def test_google_testbrowser(self):
        f = FuncBrows('testbrowser', 'http://start.ubuntu.com/')
        f.open('9.10/')
        self.assertTrue('Ubuntu' in f.page_title)
        
        
    def test_google_selenium(self):
        f = FuncBrows('*firefox3', 'http://start.ubuntu.com/', host = '192.168.90.130', port = 4444)
        f.open('9.10/')
        self.assertTrue('Ubuntu' in f.page_title)
        
    def test_google_query_testbrowser(self):
        f = FuncBrows('testbrowser', 'http://start.ubuntu.com/')
        f.open('9.10/')
        self.assertTrue('Ubuntu' in f.page_title)
        f.form_name = 'cse-search-box'
        f.set_form_text_field('q', 'test')
        f.submit_form()
        self.assertTrue('test' in f.page_title)
        
    def test_google_query_selenium(self):
        f = FuncBrows('*firefox3', 'http://start.ubuntu.com/', host = '192.168.90.130', port = 4444)
        f.open('9.10/')
        self.assertTrue('Ubuntu' in f.page_title)
        f.form_name = 'cse-search-box'
        f.set_form_text_field('q', 'test')
        f.submit_form()
        self.assertTrue('test' in f.page_title)
        
    def test_form_fails_correctly(self):
        """ Check that we can't fill in a form without setting the form name that we want to fill """
        f = FuncBrows('*firefox3', 'http://start.ubuntu.com/', host = '192.168.90.130', port = 4444)
        f.open('9.10/')
        self.assertTrue('Ubuntu' in f.page_title)
        self.assertRaises(ValueError, f.set_form_text_field,'q', 'test')
        
    def test_click_link_testbrowser(self):
        f = FuncBrows('testbrowser', 'http://start.ubuntu.com/')
        f.open('9.10/')
        self.assertTrue('Ubuntu' in f.page_title)
        
        f.click(url = 'http://help.ubuntu.com/')
        self.assertTrue('Documentation' in f.page_title)
        
    def test_click_link_selenium(self):
        f = FuncBrows('*firefox3', 'http://start.ubuntu.com/', host = '192.168.90.130', port = 4444)
        f.open('9.10/')
        self.assertTrue('Ubuntu' in f.page_title)
        
        f.click(url = 'http://help.ubuntu.com/')
        self.assertTrue('Documentation' in f.page_title)
        
    def test_click_link_text_testbrowser(self):
        f = FuncBrows('testbrowser', 'http://start.ubuntu.com/')
        f.open('9.10/')
        self.assertTrue('Ubuntu' in f.page_title)
        
        f.click(text = 'Ubuntu help')
        self.assertTrue('Documentation' in f.page_title)
        
    def test_click_link_text_selenium(self):
        f = FuncBrows('*firefox3', 'http://start.ubuntu.com/', host = '192.168.90.130', port = 4444)
        f.open('9.10/')
        self.assertTrue('Ubuntu' in f.page_title)
        
        f.click(text = 'Ubuntu help')
        self.assertTrue('Documentation' in f.page_title)
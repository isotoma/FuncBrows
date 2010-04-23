import unittest

from funcbrows import FuncBrows

class FuncTests(unittest.TestCase):
    
    def test_creation_testbrowser(self):
        f = FuncBrows('testbrowser', 'http://www.google.com')
        
    def test_creation_selenium(self):
        f = FuncBrows('IE6', 'http://www.google.com', host = '192.168.90.130', port = 4444)
        
        
    def test_google_testbrowser(self):
        f = FuncBrows('testbrowser', 'http://www.google.com')
        f.open('/')
        self.assertTrue('Google' in f.page_title)
        
        
    def test_google_selenium(self):
        f = FuncBrows('IE6', 'http://www.google.com', host = '192.168.90.130', port = 4444)
        f.open('/')
        self.assertTrue('Google' in f.page_title)
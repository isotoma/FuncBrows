from base import TestUsers
from FuncBrows import funcbrows
    
class TestTestBrowser(TestUsers):

    def _configure_browser(self):
        return funcbrows.FuncBrows('testbrowser', 'http://www.google.com')


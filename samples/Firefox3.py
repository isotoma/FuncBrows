from base import TestUsers
from FuncBrows import funcbrows

class TestFirefox(TestUsers):
    
    def _configure_browser(self):
        return funcbrows.FuncBrows('*firefox3', 'http://www.google.com', host = 'localhost', port = 4444)

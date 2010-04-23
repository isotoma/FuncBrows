

class FuncBrows(object):
    """An abstraction layer over various browser test tools"""
    
    
    def __init__(self, browser = None, base_url = None, **kwargs):
        """ Create the correct instance """
        if not browser:
            raise ValueError("Browser was not specifiec")
        
        if browser == 'testbrowser':
            from zc.testbrowser.browser import Browser as zc_browser
            self.browser = Browser()
            self.browser.base = base_url
            
        else:            
            try:
                import selenium
            except ImportError:
                print "Error import selenium, proceeding with zc.testbrowser"
                from zc.testbrowser.browser import Browser as zc_browser
                self.browser = Browser()
                self.browser.base = base_url
                return
            
            host = kwargs.get('host', None)
            port = kwargs.get('port', None)

            if port and host:
                self.browser = selenium.selenium("192.168.90.130", 4444, "IE6", "http://192.168.90.1:8080")
            else:
                if not port:
                    raise ValueError("Port not specified for selenium")
                if not host:
                    raise ValueError("Host not specified for selenium")
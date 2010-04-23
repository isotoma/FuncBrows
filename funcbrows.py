

class FuncBrows(object):
    """An abstraction layer over various browser test tools"""
    
    browser = None
    mode = None
    
    def __init__(self, browser = None, base_url = None, **kwargs):
        """ Create the correct instance """
        if not browser:
            raise ValueError("Browser was not specifiec")
        
        if browser == 'testbrowser':
            from zc.testbrowser.browser import Browser as zc_browser
            self.browser = zc_browser()
            self.browser.base = base_url
            self.mode = "testbrowser"
            
        else:            
            try:
                import selenium
            except ImportError:
                print "Error import selenium, proceeding with zc.testbrowser"
                from zc.testbrowser.browser import Browser as zc_browser
                self.browser = zc_browser()
                self.browser.base = base_url
                return
            
            host = kwargs.get('host', None)
            port = kwargs.get('port', None)

            if port and host:
                self.browser = selenium.selenium(host, port, browser, base_url)
                self.browser.start()
                self.mode = "selenium"
            else:
                if not port:
                    raise ValueError("Port not specified for selenium")
                if not host:
                    raise ValueError("Host not specified for selenium")
                
              
    def __del__(self):
        """  Close down the connections """
        if self.mode == "testbrowser":
            # doesn't matter
            pass
        elif self.mode == "selenium":
            self.browser.stop()
        
                
    def open(self, url):
        """ Open a given url in the browser of choice """
        if self.mode == "testbrowser":
            self.browser.open(url)
        elif self.mode == "selenium":
            self.browser.open(url)
        else:
            raise ValueError("Open is not supported by this browser mode")
        
        
    @property
    def page_title(self):
        """ Get the title of the page currently loaded by the browser """
        if self.mode == "testbrowser":
            return self.browser.title
        elif self.mode == "selenium":
            return self.browser.get_title()
        else:
            raise ValueError("Page Title is not supported by this browser mode")
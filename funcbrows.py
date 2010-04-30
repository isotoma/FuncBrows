

class FuncBrows(object):
    """An abstraction layer over various browser test tools"""
    
    # browser connection details
    browser = None
    mode = None
    
    # data variables
    form_name = None
    timeout_milliseconds = 60000
    
    def _testbrowser_form(self, form_name):
        """ Attempted fix for bad markup and forms not looking up correctly """
        

        if form_name == "*":
            f = self.browser.getForm(index=0)
            return f
                
        
        
        try:
            f = self.browser.getForm(form_name)
            return f
        except LookupError:
            forms = self.browser.mech_browser.forms()
            for f in forms:
                if f.name == form_name:
                    from zc.testbrowser.browser import Form
                    zc_form = Form(self.browser, f)
                    return zc_form
            raise
    
    def __init__(self, browser = None, base_url = None, **kwargs):
        """ Create the correct instance """
        if not browser:
            raise ValueError("Browser was not specifiec")
        
        if browser == 'testbrowser':
            from zc.testbrowser.browser import Browser as zc_browser
            self.browser = zc_browser()
            self.browser.base = base_url
            self.mode = "testbrowser"
            self.browser.mech_browser.set_handle_robots(False)
            self.browser.mech_browser.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11')]
            
        else:
            # if we can't import selenium, fall over to testbrowser anyway
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
                self.browser.window_maximize()
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
            try:
                self.browser.stop()
            except:
                pass
        
     
    def shutdown(self):
        self.__del__()
            
    def open(self, url):
        """ Open a given url in the browser of choice """
        if self.mode == "testbrowser":
            self.browser.open(url)
        elif self.mode == "selenium":
            self.browser.open(url)
        else:
            raise NotImplementedError("Open is not supported by this browser mode")
        
        
    @property
    def page_title(self):
        """ Get the title of the page currently loaded by the browser """
        if self.mode == "testbrowser":
            return self.browser.title
        elif self.mode == "selenium":
            return self.browser.get_title()
        else:
            raise NotImplementedError("Page Title is not supported by this browser mode")
        
    @property
    def page_contents(self):
        """ Get the contents of the current page """
        if self.mode == "testbrowser":
            return self.browser.contents
        if self.mode == "selenium":
            return self.browser.get_html_source()
        else:
            raise NotImplementedError("Page Contents is not supported by this browser mode")
        
    @property
    def location(self):
        """ Get the location (URL) of the current page """
        if self.mode == 'testbrowser':
            return self.browser.url
        elif self.mode == 'selenium':
            return self.browser.get_location()
        else:
            raise NotImplementedError("Location is not supported by this browser mode")
        
    def set_form_text_field(self, field_name, field_value):
        """ Set a text field in the prespecified form to a value """
        if self.form_name == None:
            raise ValueError("Form name not set")
        
        if self.mode == "testbrowser":
            form = self._testbrowser_form(self.form_name)
            form.getControl(name = field_name).value = field_value
        elif self.mode == "selenium":
            self.browser.type(field_name, field_value)
        else:
            raise NotImplementedError("Setting a text field is not supported by this browser mode")
        
    def get_form_text_field(self, field_name):
        """ Get the current value of a text field """
        if self.form_name == None:
            raise ValueError("Form name not set")
        
        if self.mode == "testbrowser":
            form = self._testbrowser_form(self.form_name)
            return form.getControl(name = field_name).value
        elif self.mode == "selenium":
            return self.browser.get_value('identifier=' + field_name)
        else:
            raise NotImplementedError("Getting the value of a text field is not supported by this browser mode")
        
        
    def set_form_select_option(self, field_name, field_value):
        """ Set the selected value for a select field """
        if self.form_name == None:
            raise ValueError("Form name not set")
        
        if self.mode == "testbrowser":
            form = self._testbrowser_form(self.form_name)
            form.getControl(name = field_name).value = [field_value]
            return
        elif self.mode == "selenium":
            self.browser.select(field_name, 'value=' +field_value)
        else:
            raise NotImplementedError("Setting a select field is not supported by this browser mode")
        
    def get_form_select_option(self, field_name):
        """ Get the selected value for a select field """
        if self.form_name == None:
            raise ValueError("Form name not set")
        
        if self.mode == "testbrowser":
            form = self._testbrowser_form(self.form_name)
            value = form.getControl(name = field_name).value
            if len(value) > 0:
                return value[0]
            else:
                return value
        elif self.mode == "selenium":
            return self.browser.get_selected_value(field_name)
        else:
            raise NotImplementedError("Getting a select field value is not supported by this browser mode")
        
    def set_check_box(self, field_name, value):
        """ Set at checkbox to the given value """
        if self.form_name == None:
            raise ValueError("Form name not set")
        
        if self.mode == "testbrowser":
            self.browser.getControl(name = field_name).controls[0].selected = value
        elif self.mode == "selenium":
            if value == True:
                self.browser.check(field_name)
            else:
                self.browser.unceck(field_name)
        else:
            raise NotImplementedError("Setting a checkbox is not supported by this browser mode")
        
    def submit_form(self):
        """ Submit the prespecified form """
        
        if self.mode == "testbrowser":
            form = self._testbrowser_form(self.form_name)
            form.submit()
            
        elif self.mode == "selenium":
            self.browser.submit(self.form_name)
            self.browser.wait_for_page_to_load(self.timeout_milliseconds)
        else:
            raise NotImplemented("Submitting a form is not supported by this browser mode")
        
    def click(self, url = None, text = None, identifier = None, internal = False):
        """ Click on an element """
        
                
        if self.mode == "testbrowser":
            if url:
                link = self.browser.getLink(url = url)
                link.click()
                return
            if text:
                link = self.browser.getLink(text = text)
                link.click()
                return
            if identifier:
                try:
                    link = self.browser.getLink(id = identifier)
                    link.click()
                except:
                    # we need to account for names
                    # so if the id doesn't work, try grabbing the control by name
                    self.browser.getControl(name = identifier).click()
                    
                return
        elif self.mode == "selenium":
            if url:
                # selenium doesn't have the ability to natively click a link by url
                # grab it using xpath instead
                self.browser.click('xpath=//a[@href="' + url +'"]')
                if not internal:
                    self.browser.wait_for_page_to_load(self.timeout_milliseconds)
                return
            if text:
                self.browser.click('link=' + text)
                if not internal:
                    self.browser.wait_for_page_to_load(self.timeout_milliseconds)
            if identifier:
                self.browser.click('identifier=' + identifier)
                if not internal:
                    self.browser.wait_for_page_to_load(self.timeout_milliseconds)
                return
        else:
            raise NotImplemented("Click is not supported by this browser mode")
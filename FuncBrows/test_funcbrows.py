from funcbrows import FuncBrows
import time

from twisted.trial import unittest
from twisted.internet import reactor, threads, defer
from twisted.web import static, server
from twisted.web.resource import Resource

import threading

class SimpleTestPage(Resource):
    
    def getChild(self, name, request):
        return self
    
    def render_GET(self, request):
        return open('../test.html', 'r').read()
    
    def render_POST(self, request):
        header = """<html><head><title>Results</title></head><body>"""       
        footer = """</body></html>"""
        
        content = ""
        if request.args.get('q', None):
            content += "<p>" + request.args.get('q')[0] + "</p>"
            
        if request.args.get('select-field', None):
            content += "<p>" + str(request.args.get('select-field')) + "</p>"
            
        if request.args.get('check-box', None):
            content += "<p>" + 'checked' + "</p>"
            
        return header + content + footer
    
    
    
def run_in_thread(callback):
    def _(*args):
        return threads.deferToThread(callback, *args)
    return _
    
class FuncTests(unittest.TestCase):
    
    
   
    def setUp(self):
        site = server.Site(SimpleTestPage())
        self.port = reactor.listenTCP(0, site)
        self.portno = self.port.getHost().port
        
    
    @run_in_thread
    def test_creation_testbrowser(self):
        f = FuncBrows('testbrowser', 'http://localhost:%s' % self.portno)
    
    @run_in_thread
    def test_creation_selenium(self):
        f = FuncBrows('*firefox3', 'http://localhost:%s' % self.portno, host = '127.0.0.1', port = 4444)
        
    @run_in_thread
    def test_page_testbrowser(self):
        f = FuncBrows('testbrowser', 'http://localhost:%s' % self.portno)
        f.open('/')
        self.assertTrue("TestPage" in f.page_title)

        
    @run_in_thread  
    def test_page_selenium(self):
        f = FuncBrows('*firefox3', 'http://localhost:%s' % self.portno, host = '127.0.0.1', port = 4444)
        f.open('/')
        self.assertTrue('TestPage' in f.page_title)
        
    @run_in_thread
    def test_page_query_testbrowser(self):
        f = FuncBrows('testbrowser', 'http://localhost:%s' % self.portno)
        f.open('/')
        self.assertTrue("TestPage" in f.page_title)
        f.form_name = 'test-form'
        f.set_form_text_field('q', 'test')
        f.submit_form()
        self.assertTrue('test' in f.page_contents)
    
    @run_in_thread
    def test_page_query_selenium(self):
        f = FuncBrows('*firefox3', 'http://localhost:%s' % self.portno, host = '127.0.0.1', port = 4444)
        f.open('/')
        self.assertTrue('TestPage' in f.page_title)
        f.form_name = 'test-form'
        f.set_form_text_field('q', 'test')
        f.submit_form()
        self.assertTrue('test' in f.page_contents)
        
    @run_in_thread
    def test_form_fails_correctly(self):
        """ Check that we can't fill in a form without setting the form name that we want to fill """
        f = FuncBrows('testbrowser', 'http://localhost:%s' % self.portno)
        f.open('/')
        self.assertTrue("TestPage" in f.page_title)
        self.assertRaises(ValueError, f.set_form_text_field,'q', 'test')
        
    @run_in_thread
    def test_click_link_by_url_testbrowser(self):
        f = FuncBrows('testbrowser', 'http://localhost:%s' % self.portno)
        f.open('/')
        self.assertTrue("TestPage" in f.page_title)
        
        f.click(url = 'http://www.google.com')
        self.assertTrue('Google' in f.page_title)
        
    @run_in_thread
    def test_click_link_by_text_testbrowser(self):
        f = FuncBrows('testbrowser', 'http://localhost:%s' % self.portno)
        f.open('/')
        self.assertTrue("TestPage" in f.page_title)
        
        f.click(text = 'Google')
        self.assertTrue('Google' in f.page_title)
        
    @run_in_thread
    def test_click_link_by_identifier_testbrowser(self):
        f = FuncBrows('testbrowser', 'http://localhost:%s' % self.portno)
        f.open('/')
        self.assertTrue("TestPage" in f.page_title)
        
        f.click(identifier = "google-link")
        self.assertTrue('Google' in f.page_title)
        
    @run_in_thread    
    def test_click_link_by_url_selenium(self):
        f = FuncBrows('*firefox3', 'http://localhost:%s' % self.portno, host = '127.0.0.1', port = 4444)
        f.open('/')
        self.assertTrue("TestPage" in f.page_title)
        
        f.click(url = 'http://www.google.com')
        self.assertTrue('Google' in f.page_title)
        
        
    @run_in_thread    
    def test_click_link_by_text_selenium(self):
        f = FuncBrows('*firefox3', 'http://localhost:%s' % self.portno, host = '127.0.0.1', port = 4444)
        f.open('/')
        self.assertTrue("TestPage" in f.page_title)
        
        f.click(text = 'Google')
        self.assertTrue('Google' in f.page_title)
        
    @run_in_thread    
    def test_click_link_by_identifier_selenium(self):
        f = FuncBrows('*firefox3', 'http://localhost:%s' % self.portno, host = '127.0.0.1', port = 4444)
        f.open('/')
        self.assertTrue("TestPage" in f.page_title)
        
        f.click(identifier = "google-link")
        self.assertTrue('Google' in f.page_title)
        
    @run_in_thread
    def test_get_select_field_testbrowser(self):
        f = FuncBrows('testbrowser', 'http://localhost:%s' % self.portno)
        f.open('/')
        self.assertTrue("TestPage" in f.page_title)
        f.form_name = 'test-form'
        self.assertTrue('1' in f.get_form_select_option('select-field'))
        
    @run_in_thread
    def test_get_select_field_selenium(self):
        f = FuncBrows('*firefox3', 'http://localhost:%s' % self.portno, host = '127.0.0.1', port = 4444)
        f.open('/')
        self.assertTrue("TestPage" in f.page_title)
        f.form_name = 'test-form'
        self.assertTrue('1' in f.get_form_select_option('select-field'))
        self.assertFalse('test' in f.get_form_select_option('select-field'))
        
        
    @run_in_thread
    def test_submit_field_testbrowser(self):
        f = FuncBrows('testbrowser', 'http://localhost:%s' % self.portno)
        f.open('/')
        self.assertTrue("TestPage" in f.page_title)
        f.form_name = 'test-form'
        f.set_form_select_option('select-field', '2')
        self.assertTrue('test-2' in f.page_contents)
        
    @run_in_thread
    def test_submit_field_selenium(self):
        f = FuncBrows('*firefox3', 'http://localhost:%s' % self.portno, host = '127.0.0.1', port = 4444)
        f.open('/')
        self.assertTrue("TestPage" in f.page_title)
        f.form_name = 'test-form'
        f.set_form_select_option('select-field', '2')
        self.assertTrue('test-2' in f.page_contents)
        
        
    @run_in_thread
    def test_set_checkbox_testbrowser(self):
        f = FuncBrows('testbrowser', 'http://localhost:%s' % self.portno)
        f.open('/')
        self.assertTrue("TestPage" in f.page_title)
        f.form_name = 'test-form'
        f.set_check_box('check-box', True)
        f.submit_form()
        self.assertTrue('checked' in f.page_contents)
        
    @run_in_thread
    def test_set_checkbox_selenium(self):
        f = FuncBrows('*firefox3', 'http://localhost:%s' % self.portno, host = '127.0.0.1', port = 4444)
        f.open('/')
        self.assertTrue("TestPage" in f.page_title)
        f.form_name = 'test-form'
        f.set_check_box('check-box', True)
        f.submit_form()
        self.assertTrue('checked' in f.page_contents)
        
    @run_in_thread
    def test_location_testbrowser(self):
        f = FuncBrows('testbrowser', 'http://localhost:%s' % self.portno)
        f.open('/')
        self.assertTrue("TestPage" in f.page_title)
        self.assertTrue("localhost" in f.location)
        
    @run_in_thread
    def test_location_selenium(self):
        f = FuncBrows('*firefox3', 'http://localhost:%s' % self.portno, host = '127.0.0.1', port = 4444)
        f.open('/')
        self.assertTrue("TestPage" in f.page_title)
        self.assertTrue("localhost" in f.location)
        
        
    @run_in_thread
    def test_get_text_field_value_testbrowser(self):
        f = FuncBrows('testbrowser', 'http://localhost:%s' % self.portno)
        f.open('/')
        self.assertTrue("TestPage" in f.page_title)
        f.form_name = 'test-form'
        f.set_form_text_field('q', 'random')
        value = f.get_form_text_field('q')
        self.assertTrue('random' == value)
        
    @run_in_thread
    def test_get_text_field_value_selenium(self):
        f = FuncBrows('*firefox3', 'http://localhost:%s' % self.portno, host = '127.0.0.1', port = 4444)
        f.open('/')
        self.assertTrue("TestPage" in f.page_title)
        f.form_name = 'test-form'
        f.set_form_text_field('q', 'random')
        value = f.get_form_text_field('q')
        self.assertTrue('random' == value)
        
    def tearDown(self):
        self.port.stopListening()
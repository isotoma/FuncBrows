=========
FuncBrows
=========

FuncBrows is a relatively lightweight abstraction wrapper around various functional web testing tools.
It is intended to allow the creation of single unit tests that will run on multiple testing tools with a minimum of configuration. This will allow functional and system tests to be created in a single api.

By necessity, the api will be fairly simple, and will not support the advanced features of certain tools. This is aimed to be a lowest common demoninator, although the selected tool is available, should more complex tests be required (at the cost of tool portability).

Currently Supported
-------------------

There are two fully supported testing tools:
 * Selenium RC (1.*)
 * zc.testbrowser
It is intended that more will be added over time, but these are what were required to scratch my own itch.

Running the Tests
-----------------

FuncBrows comes with a full test suite to exercise all the available methods. It uses twisted to create a local, known webserver which can be used to output the expected results.
To run it, you will need:
 * twisted
 * twisted web
 * trial (twisted testing tool, usually included with a twisted distribution)
To run the tests, execute::
	trial test_funcbrows

API
---

One of the main aims of FuncBrows is to have a simple and clean API. There are however one or two warts that cannot easily be worked around in the underlying tools. I will attempt to provide some examples of the API, and then explain any workarounds that have been implemented.
For more complete examples of every method of the API, see test_funcbrows.py.

Instantiation
~~~~~~~~~~~~~

Instantiating FuncBrows is the main place where the underlying tools show through, as you have to make a selection as to which tool you would like to use.

The basic method takes a browser type, and a URL to test::
	f = FuncBrows('testbrowser', 'http://localhost:80')
*This will instantiate a zc.testbrowser instance, with the pointing at localhost, on port 80*

A selenium instance requires extra parameters (the address and port for the selenium server)::
	f = FuncBrows('*firefox3', 'http://localhost', host = '127.0.0.1', port = 4444)

Form Usage
~~~~~~~~~~

FuncBrows requires the name of the form to work on, before anything can be modified in a particular form. Failure to set this will result in a ValueError. This prevents ambiguous form controls. There is however a wart where zc.testbrowser is concerned, and forms without an id on the page. See the note below for how to workaround this.

Set the value of a text box on a form::
	f = FuncBrows('testbrowser', 'http://localhost:80')
	f.open('/')
	f.form_name = 'test-form'
	f.set_form_text_field('q', 'test')
	f.submit_form()

Page Content
~~~~~~~~~~~~

Currently there are only three available methods for getting meta-data and data from the page that is currently loaded:

location
	Property for the current location of the page (the URL)
page_title
	Property for the title of the current page
page_content
	The HTML content of the page

Warts
~~~~~

Unfortunately, a completely clean abstraction isn't quite possible, so there are a few places where special care is needed.
1. Selenium currently struggles with AJAX loaded pages as they don't fire a page load event. An attempt has been made to get round this, you can pass 'internal=True' into the click() method. This will set Selenium to not expect a page load, and to carry straight on.
2. Forms without an id or name can trip up zc.testbrowser. A workaround for this has been implemented, but is not entirely satisfactory. If you set the form_name = '*', it will use the first form on the page.

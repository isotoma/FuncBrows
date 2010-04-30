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
*italics* This will instantiate a zc.testbrowser instance, with the pointing at localhost, on port 80 *italics*

A selenium instance requires extra parameters (the address and port for the selenium server)::
	f = FuncBrows('*firefox3', 'http://localhost:%s' % self.portno, host = '127.0.0.1', port = 4444)

Form Usage
~~~~~~~~~~

FuncBrows requires the name of the form to work on, before anything can be modified in a particular form. Failure to set this will result in a ValueError. This prevents ambiguous form controls. There is however a wart where zc.testbrowser is concerned, and forms without an id on the page. See the note below for how to workaround this.



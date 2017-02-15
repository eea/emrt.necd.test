import unittest

from edw.seleniumtesting.common import BrowserTestCase


def suite(browser, base_url):
    """Plone login test 
    """
    # setup a new suite
    suite = unittest.TestSuite()

    for name in LoginTestCase.my_tests():
        testcase = LoginTestCase(name, browser, base_url)
        suite.addTest(testcase)

    return suite


class LoginTestCase(BrowserTestCase):

    def setUp(self):
        self.browser.get(self.url)

    def test_login(self):
        """Plone login test.
        """
        self.assertTrue(False)
        

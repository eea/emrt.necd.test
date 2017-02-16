import unittest

from edw.seleniumtesting.common import BrowserTestCase


def suite(browser, base_url):
    """Plone logout test 
    """
    # setup a new suite
    suite = unittest.TestSuite()

    for name in LogoutTestCase.my_tests():
        testcase = LogoutTestCase(name, browser, base_url)
        suite.addTest(testcase)

    return suite


class LogoutTestCase(BrowserTestCase):
    
    def setUp(self):
        self.browser.get(self.url + '/logout')

    def test_logout(self):
        """Plone login test.
        """

        logout = self.browser.find_element_by_id("personaltools-login")

        self.assertEqual(logout.text, "Log in")


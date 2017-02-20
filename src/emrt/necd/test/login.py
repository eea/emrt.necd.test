import unittest

from emrt.necd.test.util import runas
from edw.seleniumtesting.common import BrowserTestCase


def suite(browser, base_url, extra_args):
    """Plone login test
    """
    # setup a new suite
    test_suite = unittest.TestSuite()

    for name in LoginTestCase.my_tests():
        testcase = LoginTestCase(name, browser, base_url, extra_args)
        test_suite.addTest(testcase)

    return test_suite


class LoginTestCase(BrowserTestCase):

    def setUp(self):
        self.browser.get(self.url)

    @runas("admin")
    def test_login(self):
        """Plone login test.
        """
        user_name = self.browser.find_element_by_id("user-name")

        self.assertEqual(user_name.text, "admin")

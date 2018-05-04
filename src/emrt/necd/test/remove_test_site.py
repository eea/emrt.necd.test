import emrt.necd.test.util as util
import unittest

from edw.seleniumtesting.common import BrowserTestCase


FINDER = util.ElementFinder()


def suite(browser, base_url, extra_args):
    """ Call on review folder url providing user mapping and user accounts.\n
    `` seleniumtesting http://localhost/Workflow_test \\
        -ea roles admin acc_admin \\
        -ea users acc_admin acc_admin \\
        -ea ldap_credentials ldap_manager_dn_acc ldap_manager_dn_pwd
    ``
    """
    FINDER.set_browser(browser)

    params = dict(
        browser=browser,
        base_url=base_url,
        extra_args=extra_args
        )

    test_suite = util.TestFactory(
        unittest.TestSuite(),
        **params
        )

    # test admin removes the test site instance
    test_suite.add_tests(RemovePloneSite)

    return test_suite()


class RemovePloneSite(BrowserTestCase):

    def test_remove_site(self):
        """Test zope user removes test site after finishing tests
        """
        pos = self.url.rfind("/")
        base_url = self.url[:pos]

        usr, pwd = list(self.extra_args["zope_user"].items())[0]
        credentials = usr + ":" + pwd + "@"

        pos = base_url.find('//')
        url = base_url[:pos + 2] + credentials + base_url[pos + 2:]
        self.browser.get(url + '/manage_main')

        FINDER.css("input[value='Workflow_test']").click()
        FINDER.css("input[value='Delete']").click()

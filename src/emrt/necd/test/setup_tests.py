import emrt.necd.test.util as util
import unittest

from edw.seleniumtesting.common import BrowserTestCase


FINDER = util.ElementFinder()


def suite(browser, base_url, extra_args):
    """ Call on review folder url providing user mapping and user accounts.\n
    `` seleniumtesting http://localhost/Workflow_test \\
        -ea roles admin acc_admin \\
        -ea users acc_admin acc_admin
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

    # test admin adds a new Plone Site
    test_suite.add_tests(AddPloneSite)

    # test admin sets the cache server
    test_suite.add_tests(SetupCache)

    # test admin sets the LDAP plugin settings
    test_suite.add_tests(SetupLDAPPlugin)

    # test admin adds a new ReviewFolder
    test_suite.add_tests(AddReviewFolder)

    # test admin starts review
    test_suite.add_tests(SetupReviewFolderWorkflow)

    return test_suite()


class AddPloneSite(BrowserTestCase):

    def setUp(self):
        pos = self.url.rfind("/")
        self.browser.get(self.url[:pos])

    def test_add_plone_site(self):
        """Test zope user adds plone site for tests
        """
        base_url = self.browser.current_url

        usr, pwd = list(self.extra_args["zope_user"].items())[0]
        credentials = usr + ":" + pwd + "@"

        pos = base_url.find('//')
        url = base_url[:pos + 2] + credentials + base_url[pos + 2:]
        self.browser.get(url + '/manage_main')

        # Add a Plone Site
        FINDER.css("input[name='site_id'] + input").click()

        # Add a name for the site
        FINDER.css('#site_id').clear()
        FINDER.css('#site_id').send_keys("Workflow_test")

        # Select addons
        FINDER.css("input[id='emrt.necd.content:default']").click()
        FINDER.css("input[id='emrt.necd.theme:default']").click()

        FINDER.css(".formControls > input[type='submit']").click()


class SetupCache(BrowserTestCase):
    """Test zope user sets the memcached settings
    """
    def test_setup_memcached(self):
        came_from = self.browser.current_url
        path = '/memcached/manage_workspace'
        self.browser.get(came_from + path)

        # set correct memcached server
        server_xpath = '/html/body/form/table/tbody/tr[3]/td[2]/textarea'
        memcache_server = FINDER.xpath(server_xpath)
        host, port = memcache_server.text.split(':')
        memcache_server.clear()
        memcache_server.send_keys('memcached' + ':' + port)

        FINDER.css('.form-element > input[type="submit"]').click()

        self.browser.get(came_from)

class SetupLDAPPlugin(BrowserTestCase):

    def test_setup_ldap_plugin(self):
        """Test zope user sets the manager DN settings
        """
        came_from = self.browser.current_url

        # Setup LDAP
        path = '/acl_users/ldap-plugin/acl_users/manage_main'
        self.browser.get(came_from + path)

        # Add credentials
        user, pwd = list(self.extra_args['ldap_credentials'].items())[0]
        manager_dn = "cn={},o=EIONET,l=Europe".format(user)
        FINDER.xpath('/html/body/form/table/tbody/tr[9]/td[2]/input').send_keys(
            manager_dn
        )
        ldap_pwd = FINDER.xpath('/html/body/form/table/tbody/tr[9]/td[4]/input')
        ldap_pwd.clear()
        ldap_pwd.send_keys(pwd)

        select = FINDER.css('select[name="binduid_usage:int"]')
        for el in select.find_elements_by_tag_name('option'):
            if 'Always' in el.text:
                el.click()
                break
        FINDER.xpath('/html/body/form/table/tbody/tr[15]/td[2]/input').click()

        self.browser.get(came_from)


class AddReviewFolder(BrowserTestCase):

    def test_add_review_folder(self):
        """Test admin adds a review folder
        """
        # Add a new ReviewFolder
        FINDER.xpath(
            '//*[@id="plone-contentmenu-factories"]/dt/a/span[2]'
        ).click()

        FINDER.css("#reviewfolder").click()
        # Add title for the ReviewFolder
        FINDER.css("#form-widgets-IDublinCore-title").send_keys(
            "Test ReviewFolder"
        )

        FINDER.css("#form-buttons-save").click()


class SetupReviewFolderWorkflow(BrowserTestCase):

    def test_setup_workflow(self):
        """Test admin sets the workflow state for starting the review
        """
        # publish the ReviewFolder
        FINDER.css(".state-private + span").click()
        FINDER.css("#workflow-transition-publish").click()

        # start the review
        FINDER.css(".state-published + span").click()
        FINDER.css("#workflow-transition-start").click()
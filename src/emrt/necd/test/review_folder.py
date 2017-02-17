import unittest

import emrt.necd.test.util as util
from edw.seleniumtesting.common import BrowserTestCase


def suite(browser, base_url, extra_args):
    """ Call on review folder url providing user mapping and user accounts.
    `` seleniumtesting http://localhost/Plone/2017 \
        -ea roles sectorexpert acc_sectorexpert \
        -ea users acc_sectorexpert acc_sectorexpert_pwd
    ``
    """
    test_suite = unittest.TestSuite()

    for name in ReviewFolderTestCase.my_tests():
        testcase = ReviewFolderTestCase(name, browser, base_url, extra_args)
        test_suite.addTest(testcase)

    return test_suite


class ReviewFolderTestCase(BrowserTestCase):

    def setUp(self):
        self.browser.get(self.url)

    @util.runas('sectorexpert')
    def test_00_review_folder(self):
        """ Test 'Save Observation' button exists
        """
        self.browser.get(self.url)

        new_obs = util.find_link(self.browser, "New observation")
        self.assertEqual("New observation", new_obs.text)

    @util.runas('sectorexpert')
    def test_01_add_observation(self):
        """ Test sectorexpert can add an observation.
        """
        self.browser.get(self.url)

        # click new observation button
        util.find_link(self.browser, "New observation").click()

        # fill in form fields
        util.find_name(self.browser, 'form.widgets.text').send_keys('Test observation')
        util.find_name(self.browser, 'form.widgets.year').send_keys('2017')
        util.find_name(self.browser, 'form.widgets.pollutants:list').click()
        util.find_name(self.browser, 'form.widgets.parameter:list').click()

        # submit form
        util.find_name(self.browser, "form.buttons.save").click()

        # check saved information
        metadata_div = util.find_css(self.browser, '.esdDiv').text

        self.assertTrue('Austria' in metadata_div)
        self.assertTrue('1A1a' in metadata_div)
        self.assertTrue('NOx' in metadata_div)
        self.assertTrue('2017' in metadata_div)

        # expand collapsed elements so the next assertion works
        for elem in self.browser.find_elements_by_css_selector('.collapsed'):
            elem.click()

        # check saved text exists
        self.assertTrue(
            'Test observation' in
            util.find_css(self.browser, '.esdDiv').text
        )

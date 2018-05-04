import emrt.necd.test.constants as constants
import emrt.necd.test.util as util
import time
import unittest

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from edw.seleniumtesting.common import BrowserTestCase


FINDER = util.ElementFinder()


def suite(browser, base_url, extra_args):
    """ Call on review folder url providing user mapping and user accounts.\n
    `` seleniumtesting http://localhost/Plone/2017 \\
        -ea roles sectorexpert acc_sectorexpert \\
        -ea users acc_sectorexpert acc_sectorexpert_pwd
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

    test_suite.add_tests(ReviewFolder)

    #test sectorexpert add observation
    test_suite.add_tests(AddObservation)

    #test sectorexpert add question
    test_suite.add_tests(AddQuestion)

    #test sectorexpert edit question
    test_suite.add_tests(EditQuestion)

    #test sectorexpert edit key flags
    test_suite.add_tests(EditKeyFlags)

    #test sectorexpert request comments
    test_suite.add_tests(RequestComments)

    #test sectorexpert can request finalisation of the observation
    test_suite.add_tests(Conclusions)

    return test_suite()


class ReviewFolder(BrowserTestCase):

    def setUp(self):
        self.browser.get(self.url)

    @util.runas('sectorexpert')
    def test_review_folder(self):
        """ Test 'Save Observation' button exists
        """
        try:
            FINDER.link("Test ReviewFolder").click()
            time.sleep(0.5)
        except:
            pass

        new_obs = FINDER.link("New observation")
        self.assertEqual("New observation", new_obs.text)


class AddObservation(BrowserTestCase):

    def test_add_observation(self):
        """ Test sectorexpert can add an observation.
        """
        # click new observation button
        FINDER.link('New observation').click()

        # fill in form fields
        FINDER.name('form.widgets.text').send_keys('Test observation')
        FINDER.name('form.widgets.year').send_keys('2017')
        FINDER.name('form.widgets.pollutants:list').click()
        FINDER.name('form.widgets.parameter:list').click()

        # submit form
        FINDER.name('form.buttons.save').click()

        # check saved information
        metadata_div = FINDER.css('.esdDiv').text

        self.assertTrue('Austria' in metadata_div)
        self.assertTrue('1A1' in metadata_div)
        self.assertTrue('SO2' in metadata_div)
        self.assertTrue('2017' in metadata_div)

        # expand collapsed elements so the next assertion works
        for elem in self.browser.find_elements_by_css_selector('.collapsed'):
            elem.click()

        # check saved text exists
        self.assertTrue(
            'Test observation' in
            FINDER.css('.esdDiv').text
        )

        util.checks_link_names(self, FINDER, constants.SE_DRAFT_OBSERVATION)


class AddQuestion(BrowserTestCase):

    def test_add_question(self):
        """ Test sector expert can add question.
        """
        # Add questions
        FINDER.css('#add-question-link').click()
        question_text_field = FINDER.css(
            'textarea#form-widgets-text')
        question_text_field.send_keys('Test question.')
        FINDER.xpath('//*[@value="Save question"]').click()

        # Check question added
        answer_content = FINDER.css('.answerContent')
        self.assertTrue('Test question.' in answer_content.text)

        # Check buttons
        util.checks_link_names(self, FINDER, constants.SE_DRAFT)

class EditQuestion(BrowserTestCase):

    def test_edit_question(self):
        """Test sector expert can edit question
        """
        #Edit question
        FINDER.link('Edit question').click()

        # Focus on active element
        time.sleep(0.5)
        popup = self.browser.switch_to.active_element
        popup.send_keys('(edited)')

        # Focus back to page content
        self.browser.switch_to.default_content()
        time.sleep(0.5)

        FINDER.xpath('//*[@id="form-buttons-save"]').click()
        time.sleep(0.5)
        #Check question edited
        edited_answer_content = WebDriverWait(self.browser,10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'answerContent'))
        )

        self.assertTrue('(edited)' in edited_answer_content.text)
        # Check buttons
        util.checks_link_names(self, FINDER, constants.SE_DRAFT)


class SendQuestionForApproval(BrowserTestCase):

    def test_send_question_for_approval(self):

        button = FINDER.link('Send Question for Approval')
        button.click()
        util.checks_link_names(self, FINDER, constants.SE_DRAFTED)


class EditKeyFlags(BrowserTestCase):

    def test_edit_key_flags(self):
        """Test sector expert can edit key flags
        """
        #Edit key flags
        FINDER.link('Edit Key Flags').click()
        checkbox_flag = FINDER.name('form.widgets.highlight:list')
        checkbox_flag.click()
        label_flag = FINDER.css(
            'label[for="{}"]'.format(
                checkbox_flag.get_attribute('id')
            )
        ).text.strip()

        #Submit form
        FINDER.name('form.buttons.save').click()

        #Expand 'Observation details'
        FINDER.css('div.row.collapsiblePanelTitle.collapsed').click()

        #Check information change
        metadata_div = FINDER.css('.esdDiv').text

        #Check if flag was added
        self.assertTrue(label_flag in metadata_div)

class RequestComments(BrowserTestCase):

    def test_request_comments(self):
        FINDER.link('Request Comments').click()
        FINDER.css('.chosen-container').click()
        FINDER.xpath(
            '//*[@class="chosen-results"]/li[contains(text(), "TERT NECD")]'
        ).click()
        FINDER.xpath('//input[@value="Send"]').click()
        # Check buttons
        util.checks_link_names(self, FINDER, constants.SE_COUNTERPART_COMMENTS)


class Conclusions(BrowserTestCase):

    def test_go_to_conclusions(self):
        FINDER.link('Close Comments').click()
        FINDER.link('Go to Conclusions').click()
        time.sleep(1)
        FINDER.css('.formControls > input').click()
        FINDER.link('Request finalisation of the observation').click()

        #Check if save button exists
        request_fin = FINDER.xpath('//*[@value="Request finalisation of the observation"]')
        self.assertTrue('request_fin.is_displayed()')
        request_fin.click()


class DeleteObservation(BrowserTestCase):

    def test_delete_observation(self):

        # go back to observation listing
        FINDER.link("Test ReviewFolder").click()

        # check if observation has been finalised
        row_one = FINDER.xpath('//*[@id="observations-table"]/tbody/tr[1]')
        row_one.click()

        self.browser.get(self.browser.current_url+'/logout')

        # switch to login window and close the other one
        self.browser.switch_to.window(self.browser.window_handles[1])
        self.browser.close()
        self.browser.switch_to.window(self.browser.window_handles[-1])

        # login as admin
        usr, pwd = list(self.extra_args["zope_user"].items())[0]

        # get form fields
        login_name = self.browser.find_element_by_id("__ac_name")
        passwd = self.browser.find_element_by_id("__ac_password")

        # fill in form
        login_name.send_keys(usr)
        passwd.send_keys(pwd)

        # submit
        self.browser.find_element_by_name("submit").send_keys(Keys.RETURN)

        pos = self.browser.current_url.rfind("/")
        url = self.browser.current_url[:pos]
        self.browser.get(url)

        # Delete observation
        FINDER.link("Contents").click()
        FINDER.css("input[type='checkbox']").click()
        FINDER.css("input[name='folder_delete:method']").click()

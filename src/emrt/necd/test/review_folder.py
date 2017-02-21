import unittest
import emrt.necd.test.util as util

from edw.seleniumtesting.common import BrowserTestCase
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

FINDER = util.ElementFinder()


def suite(browser, base_url, extra_args):
    """ Call on review folder url providing user mapping and user accounts.\n
    `` seleniumtesting http://localhost/Plone/2017 \\
        -ea roles sectorexpert acc_sectorexpert \\
        -ea users acc_sectorexpert acc_sectorexpert_pwd
    ``
    """
    FINDER.set_browser(browser)

    test_suite = unittest.TestSuite()

    for name in ReviewFolder.my_tests():
        testcase = ReviewFolder(name, browser, base_url, extra_args)
        test_suite.addTest(testcase)

    for name in AddObservation.my_tests():
        test_suite.addTest(
            AddObservation(name, browser, base_url, extra_args)
        )

    for name in AddQuestion.my_tests():
        test_suite.addTest(
            AddQuestion(name, browser, base_url, extra_args)
        )

    for name in EditQuestion.my_tests():
        test_suite.addTest(
            EditQuestion(name, browser, base_url, extra_args)
        )

    for name in EditKeyFlags.my_tests():
        test_suite.addTest(
            EditKeyFlags(name, browser, base_url, extra_args)
        )

    for name in RequestComments.my_tests():
        test_suite.addTest(
            RequestComments(name, browser, base_url, extra_args)
        )

    return test_suite


class ReviewFolder(BrowserTestCase):

    def setUp(self):
        self.browser.get(self.url)

    @util.runas('sectorexpert')
    def test_review_folder(self):
        """ Test 'Save Observation' button exists
        """
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
        self.assertTrue('1A1a' in metadata_div)
        self.assertTrue('NOx' in metadata_div)
        self.assertTrue('2017' in metadata_div)

        # expand collapsed elements so the next assertion works
        for elem in self.browser.find_elements_by_css_selector('.collapsed'):
            elem.click()

        # check saved text exists
        self.assertTrue(
            'Test observation' in
            FINDER.css('.esdDiv').text
        )


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
        for link_name in (
                'Edit question', 'Upload file', 'Delete Question',
                'Go to Conclusions', 'Request Comments',
                'Send Question for Approval', 'Edit Key Flags'):
            link = FINDER.link(link_name)
            self.assertTrue(link)


class EditQuestion(BrowserTestCase):
    
    def test_edit_question(self):
        """Test sector expert can edit question
        """

        #Edit question
        FINDER.link('Edit question').click()

        question_text_field = WebDriverWait(self.browser, 10).until(
                 EC.presence_of_element_located((By.ID, "form-widgets-text")))
        question_text_field.send_keys('(edited)')
        FINDER.xpath('//*[@id="form-buttons-save"]').click()

        #Check question edited
        edited_answer_content = FINDER.css('.answerContent')
        self.assertTrue('(edited)Test question.' in edited_answer_content.text)

        # Check buttons
        for link_name in (
                'Edit question', 'Upload file', 'Delete Question',
                'Go to Conclusions', 'Request Comments',
                'Send Question for Approval', 'Edit Key Flags'):
            link = FINDER.link(link_name)
            self.assertTrue(link)


class EditKeyFlags(BrowserTestCase):
    
    def test_edit_key_flags(self):
        """Test sector expert can edit key flags
        """

        #Edit key flags
        FINDER.link('Edit Key Flags').click() 
        FINDER.name('form.widgets.highlight:list').click()

        #Submit form
        FINDER.name('form.buttons.save').click()

        #Expand 'Observation details'
        FINDER.css('div.row.collapsiblePanelTitle.collapsed').click()

        #Check information change
        metadata_div = FINDER.css('.esdDiv').text
        
        #Check if flag was added
        self.assertTrue('Not Estimated' in metadata_div)

class RequestComments(BrowserTestCase):
    
    def test_request_comments(self):
        FINDER.link('Request Comments').click()
        FINDER.css('.chosen-container').click()
        FINDER.xpath('//*[@class="chosen-results"]/li').click()
        FINDER.xpath('//input[@value="Send"]').click()

        # Check buttons
        for link_name in (
                'Select new Counterparts',
                'Close Comments',
                'Edit Key Flags'):
            link = FINDER.link(link_name)
            self.assertTrue(link)

import emrt.necd.test.constants as constants
import emrt.necd.test.review_folder as se
import emrt.necd.test.util as util
import time
import unittest


from edw.seleniumtesting.common import BrowserTestCase
from emrt.necd.test.add_answer import (
    ApproveQuestionAndSend, CreateAnswer, AcknowledgeAnswer
)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


FINDER = util.ElementFinder()


def suite(browser, base_url, extra_args):
    """ Call on review folder url providing user mapping and user accounts.\n
    `` seleniumtesting http://localhost/Plone/2017 emrt.necd.test.add_conclusions\\
        -ea roles sectorexpert acc_sectorexpert \\
        -ea users acc_sectorexpert acc_sectorexpert_pwd \\
        -ea roles leadreviewer acc_leadreviewer \\
        -ea users acc_leadreviewer acc_leadreviewer_pwd \\
        -ea roles msauthority acc_msauthority \\
        -ea users acc_msauthority pwd_msauthority
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

    # Add tests for sector expert actions
    test_suite.add_tests(se.ReviewFolder)

    # test sectorexpert add observation
    test_suite.add_tests(se.AddObservation)

    # test sectorexpert add question
    test_suite.add_tests(se.AddQuestion)

    # test sectorexpert edit question
    test_suite.add_tests(se.EditQuestion)

    # test sectorexpert edit key flags
    test_suite.add_tests(se.EditKeyFlags)

    # test sectorexpert sends question for approval
    test_suite.add_tests(se.SendQuestionForApproval)

    # test leadreviewer approves question and sends to MSE
    test_suite.add_tests(ApproveQuestionAndSend)

    # test msauthority creates and submits an answer
    test_suite.add_tests(CreateAnswer)

    # test sectorexpert acknowledges answer
    test_suite.add_tests(AcknowledgeAnswer)

    # test sectorexpert adds conclusion
    test_suite.add_tests(AddConclusions)

    return test_suite()


class AddConclusions(BrowserTestCase):


    def test_add_conclusions(self):

        FINDER.link('Add Conclusions').click()
        time.sleep(1)

        FINDER.xpath('//*[@id="form-buttons-save"]').click()
        time.sleep(1)

        util.checks_link_names(self, FINDER, constants.SE_CONCLUSION)
        text = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, 'Conclusions'))
        )
        print(text)


class RemoveTestSite(BrowserTestCase):

    def test_remove_site(self):
        pass
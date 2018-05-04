import emrt.necd.test.constants as constants
import emrt.necd.test.review_folder as se
import emrt.necd.test.util as util
import time
import unittest

from edw.seleniumtesting.common import BrowserTestCase


FINDER = util.ElementFinder()

def suite(browser, base_url, extra_args):
    """ Call on review folder url providing user mapping and user accounts.\n
    `` seleniumtesting http://localhost/Plone/2017 emrt.necd.test.finish_observation_lr\\
        -ea roles sectorexpert acc_sectorexpert \\
        -ea users acc_sectorexpert acc_sectorexpert_pwd \\
        -ea roles leadreviewer acc_leadreviewer \\
        -ea users acc_leadreviewer acc_leadreviewer_pwd
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

    #Add tests for sector expert actions
    test_suite.add_tests(se.ReviewFolder)

    #test sectorexpert add observation
    test_suite.add_tests(se.AddObservation)

    #test sectorexpert add question
    test_suite.add_tests(se.AddQuestion)

    #test sectorexpert edit question
    test_suite.add_tests(se.EditQuestion)

    # test sectorexpert edit key flags
    test_suite.add_tests(se.EditKeyFlags)

    # test sectorexpert sends question for approval
    test_suite.add_tests(se.SendQuestionForApproval)

    # test leadreviewer goes to conclusions
    test_suite.add_tests(FinishObservationLR)

    # Delete test observation
    test_suite.add_tests(se.DeleteObservation)

    return test_suite()


class FinishObservationLR(BrowserTestCase):

    @util.runas('leadreviewer')
    def test_go_to_conclusions_lr(self):
        """Test leadreviewer goes to conclusions
        """

        # Check buttons for LR
        util.checks_link_names(self, FINDER, constants.LR_DRAFTED)

        FINDER.link("Go to Conclusions").click()
        time.sleep(1)
        FINDER.css('.formControls > input').click()

        util.checks_link_names(self, FINDER, constants.LR_CLOSED)

        FINDER.link("Edit conclusion").click()
        time.sleep(1)
        FINDER.css('#form-widgets-text').send_keys("(edited)")
        FINDER.css('#form-buttons-save').click()
        edited_content = FINDER.xpath('//*[@id="conclusions"]/dl/dd[2]')
        self.assertTrue('(edited)' in edited_content.text)

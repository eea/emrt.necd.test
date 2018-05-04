import emrt.necd.test.constants as constants
import emrt.necd.test.review_folder as se
import emrt.necd.test.util as util
import time
import unittest

from edw.seleniumtesting.common import BrowserTestCase


FINDER = util.ElementFinder()

def suite(browser, base_url, extra_args):
    """ Call on review folder url providing user mapping and user accounts.\n
    `` seleniumtesting http://localhost/Plone/2017 emrt.necd.test.ask_to_redraft\\
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
    test_suite.add_tests(AskToRedraft)

    #test sectorexpert redrafts question
    test_suite.add_tests(SERedraft)

    # Delete test observation
    test_suite.add_tests(se.DeleteObservation)

    return test_suite()


class AskToRedraft(BrowserTestCase):

    @util.runas('leadreviewer')
    def test_ask_to_redraft(self):
        """Test leadreviewer asks sector expert to redraft
        """
        # Check buttons for LR
        util.checks_link_names(self, FINDER, constants.LR_DRAFTED)

        FINDER.link("Ask SE to redraft").click()
        time.sleep(1)
        reason = "Test redraft reason."
        FINDER.css('#form-widgets-redraft_message').send_keys(reason)

        FINDER.css('.formControls > input').click()

        FINDER.link("Edit Key Flags")
        reason_div = FINDER.xpath("(//div[@class='answerContent'])[2]")
        self.assertTrue(reason_div.text == reason)


class SERedraft(BrowserTestCase):

    @util.runas('sectorexpert')
    def test_se_redraft(self):
        """Test sector expert redrafts question
        """

        # Questions cannot be deleted after redrafting
        buttons = constants.SE_DRAFT
        buttons.remove('Delete Question')

        util.checks_link_names(self, FINDER, buttons)
        reason_div = FINDER.xpath("(//div[@class='answerContent'])[2]")

        self.assertEqual(reason_div.text, "Test redraft reason.")




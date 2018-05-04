import emrt.necd.test.constants as constants
import emrt.necd.test.review_folder as se
import emrt.necd.test.util as util
import time
import unittest

from edw.seleniumtesting.common import BrowserTestCase


FINDER = util.ElementFinder()


def suite(browser, base_url, extra_args):
    """ Call on review folder url providing user mapping and user accounts.\n
    `` seleniumtesting http://localhost/Plone/2017 emrt.necd.test.finish_observation\\
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

    # test sector expert adds followup question
    test_suite.add_tests(AddFollowUpQuestion)

    # Delete test observation
    test_suite.add_tests(se.DeleteObservation)

    return test_suite()


class ApproveQuestionAndSend(BrowserTestCase):

    @util.runas('leadreviewer')
    def test_approve_question_and_send(self):

        # Check buttons for LR
        util.checks_link_names(self, FINDER, constants.LR_DRAFTED)

        FINDER.link('Approve question and send').click()

        # Check buttons after approving question
        util.checks_link_names(self, FINDER, constants.LR_PENDING)


class CreateAnswer(BrowserTestCase):

    @util.runas('msauthority')
    def test_create_and_submit_answer(self):
        util.checks_link_names(self, FINDER, constants.MSA_PENDING)

        input = "Test answer."
        FINDER.link('Create answer').click()
        FINDER.css("#form-widgets-text").send_keys(input)
        FINDER.css('.formControls input').click()

        answer = FINDER.css('.commentanswer > .answerContent')
        self.assertEqual(answer.text, input)

        util.checks_link_names(self, FINDER,
                               constants.MSA_PENDING_ANSWER_DRAFTING)

        FINDER.link('Edit answer').click()
        time.sleep(0.5)
        FINDER.css('#form-widgets-text').send_keys("(edited)")
        FINDER.xpath('//*[@id="form-buttons-save"]').click()
        edited_answer = FINDER.css('.commentanswer > .answerContent')
        self.assertEqual(edited_answer.text, '(edited)'+input)

        FINDER.link('Submit Answer').click()

        FINDER.link("Recall")


class AcknowledgeAnswer(BrowserTestCase):

     @util.runas('sectorexpert')
     def test_acknowledge_answer(self):

        util.checks_link_names(self, FINDER, constants.SE_ANSWERED)
        FINDER.link('Acknowledge Answer').click()

        util.checks_link_names(self, FINDER, constants.SE_CLOSED)


class AddFollowUpQuestion(BrowserTestCase):

    def test_add_followup(self):
        FINDER.link('Add follow up question').click()

        time.sleep(0.5)
        FINDER.css('#form-widgets-text').send_keys("Test follow up question.")
        FINDER.css('.formControls input').click()

        followup = FINDER.xpath("(//div[@class='answerContent'])[3]")
        self.assertEqual(followup.text, "Test follow up question.")

        util.checks_link_names(self, FINDER, constants.SE_DRAFT)
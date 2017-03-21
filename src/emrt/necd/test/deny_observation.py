import unittest
import emrt.necd.test.util as util
import emrt.necd.test.review_folder as se
import emrt.necd.test.conclusions as lr


FINDER = util.ElementFinder()

def suite(browser, base_url, extra_args):
    """ Call on review folder url providing user mapping and user accounts.\n
    `` seleniumtesting http://localhost/Plone/2017 emrt.necd.test.deny_observation\\
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

    #test sectorexpert edit key flags
    test_suite.add_tests(se.EditKeyFlags)

    #test sectorexpert request comments
    test_suite.add_tests(se.RequestComments)

    #test sectorexpert can request finalisation of the observation
    test_suite.add_tests(se.Conclusions)

    #Add actions for lead reviewer actions
    test_suite.add_tests(lr.ObservationConclusion)

    #Add test for finishing observation
    test_suite.add_tests(lr.DenyObservation)

    return test_suite()

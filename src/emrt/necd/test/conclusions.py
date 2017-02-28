import unittest
import emrt.necd.test.util as util

import time

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

    params = dict(  
        browser=browser,                                                                         
        base_url=base_url,                                                                       
        extra_args=extra_args                                                                    
        )                                                                                            
     
    test_suite = util.TestFactory(                                                               
        unittest.TestSuite(),                                                                    
        **params
        )
    
    test_suite.add_tests(ObservationConclusion) 
    
    #Add test for finishing observation
    test_suite.add_tests(FinishObservation)

    return test_suite()

class ObservationConclusion(BrowserTestCase):

    def setUp(self):
        self.browser.get(self.url)

    @util.runas('leadreviewer')
    def test_conclusions(self):
        """ Test 'Conclusions' workflow
        """

        first_obs = WebDriverWait(self.browser, 10).until(
                 EC.presence_of_element_located((By.XPATH, '//*[@id="observations-table"]/tbody/tr[1]/td[1]/a')))
        first_obs.click()
        
        conclusions_tab = FINDER.link("Conclusions") 
        self.assertEqual("Conclusions", conclusions_tab.text)
        conclusions_tab.click()


class FinishObservation(BrowserTestCase):

    def test_finish_observation(self):
        """Test leadreviewer can finish observation
        """
        
        came_from = self.url    

        #click finish observation button
        FINDER.link("Finish Observation").click()

        #go back to observation listing
        self.browser.get(came_from)

        #check if observation has been finalised
        row_one = FINDER.xpath('//*[@id="observations-table"]/tbody/tr[1]/td[6]/span')

        self.assertEqual("Finalised", row_one.text)

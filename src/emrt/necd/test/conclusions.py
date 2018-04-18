import time
import emrt.necd.test.util as util

from edw.seleniumtesting.common import BrowserTestCase
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

FINDER = util.ElementFinder()

class ObservationConclusion(BrowserTestCase):

    def setUp(self):
        self.browser.get(self.url)

    @util.runas('leadreviewer')
    def test_conclusions(self):
        """ Test 'Conclusions' workflow
        """

        obs_selector = '//*[@id="observations-table"]/tbody/tr[1]/td[1]/a'
        first_obs = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, obs_selector))
        )
        first_obs.click()

        # Switch to observation window
        obs_window = FINDER.browser.window_handles[1]
        self.browser.switch_to.window(obs_window)
        conclusions_tab = FINDER.link("Conclusions")

        self.assertEqual("Conclusions", conclusions_tab.text)
        conclusions_tab.click()


class FinishObservation(BrowserTestCase):

    def test_finish_observation(self):
        """Test leadreviewer can finish observation
        """
        came_from = self.url

        # click finish observation button
        FINDER.link("Finish Observation").click()

        # go back to observation listing
        self.browser.get(came_from)

        # check if observation has been finalised
        row_one = FINDER.xpath('//*[@id="observations-table"]/tbody/tr[1]')
        self.assertTrue("Finalised" in row_one.text)


class DenyObservation(BrowserTestCase):

    def test_deny_observation(self):
        """Test leadreviewer can deny observation
        """
        came_from = self.url

        # click Conclusions tab
        FINDER.link('Conclusions').click()

        # click deny observation button
        FINDER.link("Deny finishing observation").click()

        # add a reason
        reason_field = FINDER.css('textarea#form-widgets-comments')
        reason_field.send_keys('DENIED!')

        # check if submit button exists
        deny_btn = FINDER.xpath('//*[@value="Deny finishing observation"]')
        self.assertTrue(deny_btn.is_displayed())
        deny_btn.click()

        # go back to observation listing
        self.browser.get(came_from)

        # check if observation has been finalised
        row_one = FINDER.xpath('//*[@id="observations-table"]/tbody/tr[1]')
        self.assertTrue("Conclusions" in row_one.text)

from selenium.webdriver.common.keys import Keys

def runas(username):
    def decorator(func):
        def wrapped(self):
            self.browser.get(self.url + '/login')
            login_name = self.browser.find_element_by_id("__ac_name")
            passwd = self.browser.find_element_by_id("__ac_password")
            
            login_name.send_keys(username)
            passwd.send_keys(self.extra_args["users"][username])

            self.browser.find_element_by_name("submit").send_keys(Keys.RETURN)
            return func(self)
        return wrapped
    return decorator

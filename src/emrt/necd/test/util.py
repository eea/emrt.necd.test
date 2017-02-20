from selenium.webdriver.common.keys import Keys


def runas(role='', user='', pwd_from='users', usr_from='roles'):
    def decorator(func):
        def wrapped(self):
            # extract credentials
            if role:
                username = self.extra_args[usr_from][role]
            elif user:
                username = user

            password = self.extra_args[pwd_from][username]

            # open login
            self.browser.get(self.url + '/login')

            # get form fields
            login_name = self.browser.find_element_by_id("__ac_name")
            passwd = self.browser.find_element_by_id("__ac_password")

            # fill in form
            login_name.send_keys(username)
            passwd.send_keys(password)

            # submit
            self.browser.find_element_by_name("submit").send_keys(Keys.RETURN)

            # call wrapped function
            return func(self)
        return wrapped
    return decorator


def find_css(browser, selector):
    return browser.find_element_by_css_selector(selector)


def find_name(browser, name):
    return browser.find_element_by_name(name)


def find_link(browser, text):
    return browser.find_element_by_link_text(text)


def find_xpath(browser, selector):
    return browser.find_element_by_xpath(selector)

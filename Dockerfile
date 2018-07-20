FROM ubuntu:16.04

SHELL ["/bin/bash", "-c"]

RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add - \
 && add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" \
 && apt-get update \
 && apt-get install -y docker-ce

RUN depsChromeDriver='unzip xvfb libxi6 libgconf-2-4' \
 && apt-get update \
 && apt-get -y install zip unzip curl git python3-pip $depsChromeDriver

# Intall Chrome
RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add \
 && echo "deb [arch=amd64]  http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
 && apt-get -y update \
 && apt-get -y install google-chrome-stable

# Intall ChromeDriver
RUN wget https://chromedriver.storage.googleapis.com/2.35/chromedriver_linux64.zip \
 && unzip chromedriver_linux64.zip \
 && mv chromedriver /usr/bin/chromedriver \
 && chown root:root /usr/bin/chromedriver \
 && chmod +x /usr/bin/chromedriver

RUN useradd --create-home --user-group selenium

USER selenium

RUN mkdir /home/selenium/results
WORKDIR /home/selenium/results

# Install the emrt.necd.test package
RUN pip3 install --user -U git+https://github.com/eea/emrt.necd.test.git@update_tests

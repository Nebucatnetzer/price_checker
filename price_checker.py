#!/usr/bin/env python3
# get user email -> get url -> get price
#download website -> search for price -> compare price
#if price = website.price -> send mail(user.mail, url)

from bs4 import BeautifulSoup
import requests
import time
import smtplib
import configparser

class User(object):

        def __init__ (self):
                self.email = ""

        def prompt_for_email(self):
                self.email = input("Please enter your email address:")
                return self.email

class Website(object):

        def __init__ (self):
                self.url = ""
                self.tree = ""

        def prompt_for_url(self):
                self.url = input("Please enter the url you want to monitor:")

        def get_page(self):
                page = requests.get(self.url)
                self.tree = html.fromstring(page.content)

        def extract_current_price(self, string):
                prices = self.tree.xpath(string)
                return prices

class Price(object):

        def __init__ (self):
                self.desired_price = ""

        def prompt_for_amount(self):
                self.desired_price = input("Please enter the price "
                                        "you're looking for:")

        def compare_prices(self, current_price):
                if not self.desired_price in current_price:
                        return False

class Configuration():
    def check_location():
        # setup the config parser
        config = configparser.ConfigParser()
        # check whether the config file exists either in the home folder or next to
        # the binary
        home = os.getenv('HOME')
        config_file = "price_checker.cfg"
        config_folder = ".config/price_checker/"
        config_path = os.path.join(home, config_folder, config_file)
        if os.path.isfile(config_path):
            config.read(config_path)
        elif os.path.isfile(config_file):
            config.read(config_file)
        else:
            print("Configuration file not found.")
            sys.exit(1)
        # assign the repository variable depending whether it's a remote or a local
        # repository
        if 'server' in config['DEFAULT']:
            repository = (config['DEFAULT']['user']
                        + "@"
                        + config['DEFAULT']['server']
                        + ":"
                        + config['DEFAULT']['repository_path'])
            int_vars.server = config['DEFAULT']['server']
        else:
            repository = config['DEFAULT']['repository_path']
        # assign the password variable
        password = config['DEFAULT']['password']
        # set the environment variables
        os.environ['BORG_REPO'] = repository
        os.environ['BORG_PASSPHRASE'] = password



christian = User()
tui = Website()
budget = Price()

christian.prompt_for_email()
tui.prompt_for_url()
budget.prompt_for_amount()
tui.get_page()
current_price = tui.extract_current_price('//div[@class="product-price"]'
                                              '/text()')

while not budget.compare_prices(current_price):
    tui.get_page()
    current_price = tui.extract_current_price('//div[@class="product-price"]'
                                              '/text()')
    print ('[%s]' % ', '.join(map(str, current_price)))
    result = budget.compare_prices(current_price)
    time.sleep(60)
else:
    print (tui.url)

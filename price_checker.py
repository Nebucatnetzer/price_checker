#!/usr/bin/env python3
# get user email -> get url -> get price
#download website -> search for price -> compare price
#if price = website.price -> send mail(user.mail, url)

from bs4 import BeautifulSoup
import requests
import time
import smtplib
import os
import configparser

class Email(object):

        def __init__ (self):
                self.email = ""

        def prompt_for_recipient(self):
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

        def extract_price(self, string):
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
        def __init__ (self):
                self.config = ""
                self.password = ""
                self.smtp_server = ""
                self.sender_address = ""
                self.check_location()
                self.smtp_port()

        def check_location(self):
            # setup the config parser
            self.config = configparser.ConfigParser()
            # check whether the config file exists either in the home folder or
            # next to the binary
            home = os.getenv('HOME')
            config_file = "price_checker.cfg"
            config_folder = ".config/price_checker/"
            config_path = os.path.join(home, config_folder, config_file)
            if os.path.isfile(config_path):
                self.config.read(config_path)
            elif os.path.isfile(config_file):
                self.config.read(config_file)
            else:
                print("Configuration file not found.")
                sys.exit(1)

        def apply_settings(self):
            # assign the password variable
            self.password = self.config['DEFAULT']['password']
            # assign the smtp_server variable
            self.smtp_server = self.config['DEFAULT']['smtp_server']
            # assign the smtp_port variable
            self.smtp_port = self.config['DEFAULT']['smtp_port']
            # assign the email_address variable
            self.sender_address = self.config['DEFAULT']['sender_address']


config = Configuration()
email = Email()
website = Website()
price = Price()

config.apply_settings()

email.prompt_for_recipient()
website.prompt_for_url()
price.prompt_for_amount()
website.get_page()
current_price = website.extract_price('//div[@class="product-price"]'
                                              '/text()')

while not budget.compare_prices(current_price):
    website.get_page()
    current_price = website.extract_price('//div[@class="product-price"]'
                                              '/text()')
    print ('[%s]' % ', '.join(map(str, current_price)))
    result = price.compare_prices(current_price)
    time.sleep(60)
else:
    print (tui.url)

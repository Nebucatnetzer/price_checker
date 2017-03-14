#!/usr/bin/env python3
# get user email -> get url -> get price
# download website -> search for price -> compare price
# if price = website.price -> send mail(user.mail, url)

from bs4 import BeautifulSoup
import requests
import time
import smtplib
import os
import sys
import configparser


class Email(object):

        def __init__(self):
                self.recipient = input("Please enter your email address:")

        def connecting(self, smtp_server, smtp_port):
                self.server = smtplib.SMTP_SSL(smtp_server, smtp_port)
                self.server.ehlo()

        def login(self, sender, password):
                self.server.login(sender, password)

        def sending(self, sender, message):
                message = "Subject: " + message
                try:
                        self.server.sendmail(sender, self.recipient, message)
                        print("Successfully sent email")
                except SMTPException:
                        print("Error: unable to send email")


class Website(object):

        def __init__(self):
                self.url = input("Please enter the url you want to monitor:")

        def get_page(self):
                page = requests.get(self.url)
                self.tree = html.fromstring(page.content)

        def extract_price(self, string):
                prices = self.tree.xpath(string)
                return prices


class Price(object):

        def __init__(self):
                self.desired_price = input("Please enter the price "
                                           "you're looking for:")

        def compare(self, current_price):
                if not self.desired_price >= current_price:
                        return False


class Configuration():

        def __init__(self):
                self.check_location()
                self.apply_settings()

        def check_location(self):
            # setup the config parser
            self.config = configparser.ConfigParser()
            # check whether the config file exists either in the home
            # folder or next to the binary
            home = os.getenv('HOME')
            config_file = "price_checker.cfg"
            config_folder = ".config/price_checker/"
            config_path = os.path.join(home, config_folder, config_file)
            if os.path.isfile(config_path):
                return self.config.read(config_path)
            elif os.path.isfile(config_file):
                return self.config.read(config_file)
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


settings = Configuration()
email = Email()
#website = Website()
#price = Price()
current_price = ""
message = "Test"

print(settings.password)
print(settings.smtp_server)
print(settings.smtp_port)
print(settings.sender_address)

email.connecting(settings.smtp_server, settings.smtp_port)
email.login(settings.sender_address, settings.password)
email.sending(settings.sender_address, message)
#while not price.compare(current_price):
#    website.get_page()
#    current_price = website.extract_price('//div[@class="product-price"]'
#                                          '/text()')
#    print('[%s]' % ', '.join(map(str, current_price)))
#    result = price.compare(current_price)
#    time.sleep(60)
#else:
#    print(website.url)

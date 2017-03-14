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
import dryscrape
import lxml


class Email(object):

    def __init__(self, recipient):
        self.recipient = recipient

    def connecting(self, smtp_server, smtp_port):
        self.server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        self.server.ehlo()

    def login(self, sender, password):
        self.server.login(sender, password)

    def sending(self, sender, message):
        message = "Subject: " + message
        try:
            self.server.sendmail(sender, self.recipient, message)
            self.server.quit()
            print("Successfully sent email")
        except SMTPException:
            print("Error: unable to send email")
            self.server.quit()


class Website(object):

    def __init__(self, url):
        self.url = url

    def get_page(self):
        session = dryscrape.Session()
        session.visit(self.url)
        page = session.body()
        self.soup = BeautifulSoup(page, "lxml")

    def extract_price(self):
        prices = self.soup.find_all("div", class_="product-price")
        return prices


class Price(object):

    def __init__(self, price):
        self.desired_price = price

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
        # assign the url variable
        self.url = self.config['DEFAULT']['url']
        # assign the price variable
        self.price = self.config['DEFAULT']['price']
        # assign the recipient variable
        self.recipient_address = self.config['DEFAULT']['recipient_address']


settings = Configuration()
email = Email(settings.recipient_address)
website = Website(settings.url)
current_price = ""
price = Price(settings.price)

while not price.compare(current_price):
    website.get_page()
    current_price = website.extract_price()
    time.sleep(1)
else:
    message = "Subject: Found Price match!\n" + settings.url
    email.connecting(settings.smtp_server, settings.smtp_port)
    email.login(settings.sender_address, settings.password)
    email.sending(settings.sender_address, message)

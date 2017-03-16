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
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Email(object):

    def __init__(self, recipient):
        self.recipient = recipient

    def connecting(self, smtp_server, smtp_port):
        self.server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        self.server.ehlo()

    def login(self, sender, password):
        self.server.login(sender, password)

    def sending(self, sender, message):
        msg = MIMEMultipart()
        msg['Subject'] = "Found a price match!"
        msg['From'] = "Price Checker"
        body = message
        msg.attach(MIMEText(body, 'plain'))
        text = msg.as_string()
        try:
            self.server.sendmail(sender, self.recipient, text)
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
        session.set_attribute('auto_load_images', False)
        session.visit(self.url)
        page = session.body()
        self.soup = BeautifulSoup(page, "lxml")

    def extract_price(self):
        prices = [a.get_text() for
                  a in self.soup.find_all("span", class_="amount ng-binding")]
        lowest_price = min(int(s) for s in prices)
        return int(lowest_price)


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
        self.price = int(self.config['DEFAULT']['price'])
        # assign the recipient variable
        self.recipient_address = self.config['DEFAULT']['recipient_address']


dryscrape.start_xvfb()
settings = Configuration()
email = Email(settings.recipient_address)

while True:
    website = Website(settings.url)
    website.get_page()
    if website.extract_price() < settings.price:
        email.connecting(settings.smtp_server, settings.smtp_port)
        email.login(settings.sender_address, settings.password)
        email.sending(settings.sender_address, settings.url)
        sys.exit(0)
    else:
        print("No Match")

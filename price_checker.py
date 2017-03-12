#!/usr/bin/env python3
# get user email -> get url -> get price
#download website -> search for price -> compare price
#if price = website.price -> send mail(user.mail, url)

from lxml import html
import requests
import time

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

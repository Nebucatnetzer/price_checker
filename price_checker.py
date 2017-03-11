#!/usr/bin/env python3
# get user email -> get url -> get price
#download website -> search for price -> compare price
#if price = website.price -> send mail(user.mail, url)

from lxml import html
import requests

class User(object):

        def __init__ (self):
                self.email = ""

        def prompt_for_email(self):
                self.email = input("Please enter your email address:")

class Website(object):

        def __init__ (self):
                self.url = ""

        def prompt_for_url(self):
                url = input("Please enter the url you want to monitor:")

        def get_page(self, url):
                page = requests.get(url)
                tree = html.fromstring(page.content)
                return self.tree


class Price(object):

        def __init__ (self):
                self.desired_price = ""

        def prompt_for_price(self):
                desired_price = input("Please enter the price
                                        you're looking for:")

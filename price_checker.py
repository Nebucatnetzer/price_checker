#!/usr/bin/env python3
# get user email -> get url -> get price
#download website -> search for price -> compare price
#if price = website.price -> send mail(user.mail, url)
#
#
#
#

from lxml import html
import requests

class User():
        email = input("Please enter your email address:")

class Website(object):
        url = input("Please enter the url you want to monitor:")
        page = requests.get(url)
        tree = html.fromstring(page.content)


class Price(object):
        desired_price = input("Please enter the price you're looking for:")

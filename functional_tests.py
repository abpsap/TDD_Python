from selenium import webdriver
import unittest

browser = webdriver.Firefox()
browser.get('http://localhost:8000')

if __name__ == '__main__':
    print ("called from commandline")


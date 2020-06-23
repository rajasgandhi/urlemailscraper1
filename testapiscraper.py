import requests
import urllib.request
from bs4 import BeautifulSoup as bs
import json
import os
from lxml import html
from flask import Flask, render_template, request, jsonify
import re
from selenium import webdriver

app = Flask(__name__)

@app.route('/api/', methods=['GET'])
def main():
    domains=request.args.get('url')
    apikey=request.args.get('apikey')
    if apikey is None:
        return jsonify("Invalid Response", "Make sure API key is present!")
    else:
        return jsonify(logic(domains))

def logic(domains):
    chrome_options=webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver=webdriver.Chrome(chrome_options=chrome_options)
    emails1=[]
    if ',' in domains:
        domains1=domains.split(',')
    else:
        domains1 = domains
        driver.get(domains1)
        emails = re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", driver.find_element_by_tag_name('body').text)
        for email in emails:
            emails1.append(email)
        return emails1
  
    for domain in domains1:
        driver.get(domain)
        emails = re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", driver.find_element_by_tag_name('body').text)
        for email in emails:
            emails1.append(email)
    
    return emails1

if __name__ == "__main__":
    app.run(debug=True)
'''from requests_html import HTMLSession
import re

session = HTMLSession()
r = session.get("http://profoundbiz.com/contact")
r.html.render()
emails = re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", r.html.html)
print(emails)'''

'''domain = "https://profoundbiz.com"
domain = str(domain)
domain2 = domain
if (domain2.startswith("https://")):
    domain2 = "http://" + domain[7:]
print (domain2)'''

'''from requests_html import AsyncHTMLSession
import asyncio
import pyppeteer
import pytest
   
@pytest.mark.asyncio
async def get_post():
    new_loop=asyncio.new_event_loop()
    asyncio.set_event_loop(new_loop)
    session = AsyncHTMLSession()
    browser = await pyppeteer.launch({ 
        'ignoreHTTPSErrors':True, 
        'headless':True, 
        'handleSIGINT':False, 
        'handleSIGTERM':False, 
        'handleSIGHUP':False
    })
    session._browser = browser
    resp_page = await session.get('https://python.org')
    await resp_page.html.arender()
    return resp_page

get_post()

<!--{% for email in emails: %}-->
<!--{% endfor %}-->'''
import os
from quart import Quart, render_template, jsonify, request
import re
from requests_html import AsyncHTMLSession
import asyncio
from pyppeteer import launch

app = Quart(__name__)

@app.route("/")
@app.route("/index")
async def main():
    return await render_template('index.html')

@app.route("/output" , methods=["POST"])
async def output():
    form = await request.form
    domains = form['url']
    
    return await render_template('output.html', emails = await logic(domains), length=(len(await logic(domains)) != 0))

async def logic(urls):
    new_loop=asyncio.new_event_loop()
    asyncio.set_event_loop(new_loop)
    session = AsyncHTMLSession()
    browser = await launch({ 
        'ignoreHTTPSErrors':True, 
        'headless':True, 
        'handleSIGINT':False, 
        'handleSIGTERM':False, 
        'handleSIGHUP':False
    })
    session._browser = browser
    r = await session.get(urls)
    await r.html.arender()

    return re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", r.html.html)
    

@app.route("/api", methods=['GET'])
async def api():
    domains=request.args.get('url')
    apikey=request.args.get('apikey')
    if apikey is None:
        return await jsonify("Invalid Response", "Make sure API key is present!")
    else:
        return await jsonify(logic(domains))

if __name__ == "__main__":
    app.run(debug=True, port='5001')

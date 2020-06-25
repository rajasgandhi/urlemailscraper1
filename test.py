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

import os
from quart import Quart, render_template, jsonify, request
import re
from requests_html import AsyncHTMLSession
import asyncio
from pyppeteer import launch

app = Quart(__name__)

returndict = {}

@app.route("/")
@app.route("/index")
async def main():
    return await render_template('index.html')

@app.route("/output" , methods=["POST"])
async def output():
    form = await request.form
    domains = form['url']
    emails = await logic(domains)
    return await render_template('output.html', emails = emails, length=(len(emails) != 0))

@app.route("/api", methods=['GET'])
async def api():
    url=request.args.get('url')
    apikey=request.args.get('apikey')
    if apikey is None:
        return {"Invalid Response":"Make sure API key is present!"}
    elif url is None:
        return {"Invalid Response": "Make sure URL is present!"}
    else:
        try:
            emails = await logic(url)
            return emails
        except:
            return {"Invalid Response": "Make sure URL is in proper format!"}

async def logic(urls):
    try:
        new_loop=asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        session = AsyncHTMLSession()
        browser = await launch({
            'ignoreHTTPSErrors':True, 
            'headless':True, 
            'handleSIGINT':False, 
            'handleSIGTERM':False, 
            'handleSIGHUP':False,
            'args': ['--no-sandbox', '--disable-setuid-sandbox']
        })
        session._browser = browser
        urls1=urls.split(',')
        emails1=[]
        for url in urls1:
            emails=await fetch(url, session)
            for email in emails:
                emails1.append(email)
        
        for i in range(len(emails1)):
            if(i % 2 == 1):
                emails1.pop(i-1)

        for i in range(len(emails1)):
            returndict.update({'email' + str(i+1):emails1[i]})

        return returndict
    except Exception as e:
        print(e)
        falseret=[]
        return falseret

async def fetch(url, session):
    url=str(url).lower()
    if (url.startswith("https://")):
        url = "http://" + url[8:]
        print (url)
    elif (url.startswith("http://")):
        pass
    else:
        url = "http://" + url
    r = await session.get(url)
    await r.html.arender()
    return re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", r.html.html)

if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=int(os.environ.get('PORT',5000)))
    app.run(debug=True)
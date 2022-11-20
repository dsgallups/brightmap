from requests import Request, Session
from bs4 import BeautifulSoup
from dotenv import dotenv_values
config = dotenv_values(".env")


url = "https://purdue.brightspace.com/d2l/lp/auth/saml/initiate-login?entityId=https://idp.purdue.edu/idp/shibboleth"

sesh = Session()

req = sesh.get(url)
soup = BeautifulSoup(req.text, "html.parser")

#proxy for BURP testing
sesh.proxies = {
    'https': '127.0.0.1:8080'
}


#Username
username=config["USERNAME"]

#Password
password=config["PASSWORD"]


login_request_body = {}
def add_to_request_body(item="", items=[]):
    if (len(item) > 0):
        login_request_body[item] = soup.find('input', {'name': 'lt'}).get('value')
    
    if (len(items) > 0) :
        for i in items:
            login_request_body[i] = soup.find('input', {'name': i}).get('value')


login_request_body["username"] = config["USERNAME"]
login_request_body["password"] = config["PASSWORD"]
add_to_request_body(items=['lt','execution','_eventId','submit'])
print(login_request_body)

#get directory to post to
dir = soup.find("form").get("action")

print(dir)

login_req = Request('POST', "https://www.purdue.edu"+dir, data=login_request_body, cookies=sesh.cookies).prepare()

login_req.headers['Content-Type'] = "application/x-www-form-urlencoded"
login_req.headers["Cache-Control"] = "max-age=0"
login_req.headers["Sec-Fetch-Site"] = "same-origin"
login_req.headers["Sec-Fetch-Mode"] = "navigate"
login_req.headers["Sec-Fetch-User"] = "?1"
login_req.headers["Sec-Fetch-Dest"] = "document"
login_req.headers["Referer"] = "https://www.purdue.edu/apps/account/cas/login?service=https%3A%2F%2Fwww.purdue.edu%2Fapps%2Fidphs%2FAuthn%2FExtCas%3Fconversation%3De1s1&entityId=https%3A%2F%2Ff81993d1-f040-40db-88cd-dddba8664daf.tenants.brightspace.com%2FsamlLogin"
login_req.headers["Connection"] = "close"
login_req.headers["Accept-Encoding"] = "gzip, deflate"
login_req.headers["Accept-Language"] = "en-US,en;q=0.9"
login_req.headers["Upgrade-Insecure-Requests"] = "1"



# Multiple redirects and GET requests happen automatically by purdue when sending, and the response is saved here
purdue_oidc_res = sesh.send(login_req, verify=False)



soup = BeautifulSoup(purdue_oidc_res.text, "html.parser")

#This is hardcoded, but you can parse the form that automatically posts
bspace_verif_url = "https://purdue.brightspace.com/d2l/lp/auth/login/samlLogin.d2l"
bspace_body = {
    "SAMLResponse": soup.find("input", {"name": "SAMLResponse"}).get('value')
}
bspace_verif_req = Request("POST", bspace_verif_url, data=bspace_body, cookies=sesh.cookies).prepare()

bspace_response = sesh.send(bspace_verif_req, verify=False)

print("--------Brightspace Response---------")
print(bspace_response.text)
print("-----------End Brightspace Response---------")

####WE DID IT, we logged in


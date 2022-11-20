# python3 main.py

from dotenv import dotenv_values

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

config = dotenv_values(".env")
driver = webdriver.Firefox()

def document_initialized(driver):
    return driver.execute_script("return initialised")

# href path of West Lafayette button at https://purdue.brightspace.com/
driver.get("https://purdue.brightspace.com/d2l/lp/auth/saml/initiate-login?entityId=https://idp.purdue.edu/idp/shibboleth")

WebDriverWait(driver, timeout=30).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'input')))

# Select and fill out purdue OIDC with credentials
username_input = driver.find_element(by=By.ID, value="username")
password_input = driver.find_element(by=By.ID, value="password")

username_input.send_keys(config["USERNAME"])
password_input.send_keys(config["PASS"])

#click login
driver.find_element(by=By.NAME, value="submit").click()


## Wait 25 seconds
WebDriverWait(driver, timeout=30).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'd2l-card')))

# now we grab all the <d2l-enrollment-card/> elements and create an array
classes = driver.find_elements(By.TAG_NAME, "d2l-card")

print("classes")
print(classes)


print("classes but nice:")
print(' '.join(str(bclass) for bclass in classes))


# Prompt user to select particular class

# Load class content, select first assignment from first tab in content page

# Select last assignment from last tab in content page


# Begin enumerating values in URL header, +1 to last assignment, and continuing until +10 404 errors
# Stop enumeration at 10 404 errors


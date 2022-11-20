# python3 main.py

from dotenv import dotenv_values

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pyshadow.main import Shadow


config = dotenv_values(".env")
driver = webdriver.Chrome()

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
WebDriverWait(driver, timeout=30).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'd2l-my-courses')))

el = driver.find_element(by=By.TAG_NAME, value="d2l-my-courses")
el_shadow = el.shadow_root

def shadow_loaded(driver, parent_name, tag_name):
    return driver.execute_script('return document.getElementsByTagName("'+parent_name+'")[0].root.children[0].tagName === "'+tag_name+'"')

# parent: d2l-my-courses
# child: d2l-my-courses-container
# document.getElementsByTagName("d2l-my-courses")[0].root.children[0].tagName === "D2L-MY-COURSES-CONTAINER" 
WebDriverWait(driver, timeout=30).until(lambda d: shadow_loaded(d, 'd2l-my-courses', 'D2L-MY-COURSES-CONTAINER'))

print("now we here")

# parent: d2l-my-courses-container
# child: d2l-tabs
# document.getElementsByTagName("d2l-my-courses")[0].root.children[0].tagName === "D2L-MY-COURSES-CONTAINER" 



# parent: d2l-tabs
# child: d2l-tab-panel
# document.getElementsByTagName("d2l-my-courses")[0].root.children[0].tagName === "D2L-MY-COURSES-CONTAINER" 

















# print("Shadow Element: ")
# print(el_shadow)
# el_shadow2= el_shadow.find_element(by=By.TAG_NAME, value='d2l-my-courses-container')


# root2 = WebDriverWait(driver, timeout).until(EC.visibility_of(shadow_root1.find_element(by=By.CSS_SELECTOR, value='[page-name="Settings"]')))



#root1 = driver.find_element(By.TAG_NAME, "d2l-my-courses")
#sroot1 = expandRootEl(root1)
#
#root2 = sroot1.find_element(By.TAG_NAME, "d2l-my-courses-container")
#sroot2 = expandRootEl(root2)
#
#print("here we are")
#print(root2)
#print


# now we grab all the <d2l-enrollment-card/> elements and create an array
# classes = driver.find_elements(By.TAG_NAME, "d2l-card")




# Prompt user to select particular class

# Load class content, select first assignment from first tab in content page

# Select last assignment from last tab in content page


# Begin enumerating values in URL header, +1 to last assignment, and continuing until +10 404 errors
# Stop enumeration at 10 404 errors


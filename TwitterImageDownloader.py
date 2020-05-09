from selenium import webdriver
import urllib
import time
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import StaleElementReferenceException

options = Options()
options.add_argument('--headless')


url = "https://twitter.com/UmbrellaAcad"


driver = webdriver.Firefox(options=options)

driver.get(url)


time.sleep(5)

# driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
imageLinkArrays = []

SCROLL_PAUSE_TIME = 4

# Get scroll height

last_height = driver.execute_script("return document.body.scrollHeight")

while True:

    images = driver.find_elements_by_tag_name('img')
    try:

        for image in images:
            if (link := image.get_attribute("src")) is not  None and "https://pbs.twimg.com/media" in link: #make sure to install python3.8 to use the walrus
                imageLinkArrays.append(link)
    except StaleElementReferenceException as e:
        raise e

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)
    
    print("last height = " + str(last_height))
    
    new_height = driver.execute_script("return document.body.scrollHeight")
     # Calculate new scroll height and compare with last scroll height
   
    print("new height = "+ str(new_height))
    
    if new_height == last_height:
        break
    last_height = new_height

    

uniqueSets = set(imageLinkArrays)

counter = 0

print(len(imageLinkArrays))
print(len(uniqueSets))
for i in uniqueSets:
    print(i)
    urllib.request.urlretrieve(i, str(counter)+".jpg")
    counter = counter + 1

driver.close()



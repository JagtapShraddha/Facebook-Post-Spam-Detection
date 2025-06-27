from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import requests
from PIL import Image
import pytesseract
from io import BytesIO
import re

def get_img_src(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless") 

    service = Service("/home/shraddha/AI-Content-Extractor/chromedriver")
    driver = webdriver.Chrome(service=service,options=chrome_options)

    try:
        driver.get(url)

        time.sleep(5)  
        img_element = driver.find_element(
        By.CSS_SELECTOR,
        "div[style='height: 100%; left: 0%; width: calc(100%);'] img"
    )

        src = img_element.get_attribute("src")
      

    finally:
        driver.quit()
    return src


def clean_text(raw):
   
    text = raw.lower()
    
    
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'\b\d+\b', '', text)        
    text = re.sub(r'\b[a-z]*\d+[a-z]*\b', '', text)    
    text = re.sub(r'\([^)]*\)', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def get_img_text(src):
    response = requests.get(src)
    content_type = response.headers.get("Content-Type", "")
    if "image" in content_type:
        img = Image.open(BytesIO(response.content))
      
        text = pytesseract.image_to_string(img, config='--psm 4')

    else:
        print("URL does not contain an image or access denied.")
    return clean_text(text)

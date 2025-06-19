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
    chrome_options.add_argument("--headless")  # Uncomment if you want headless

    service = Service("/home/shraddha/AI-Content-Extractor/chromedriver")
    driver = webdriver.Chrome(service=service,options=chrome_options)

    try:
        driver.get(url)

        time.sleep(7)  # adjust or use WebDriverWait

        # Find the img inside the div with the specified style
        img_element = driver.find_element(
        By.CSS_SELECTOR,
        "div[style='height: 100%; left: 0%; width: calc(100%);'] img"
    )

        src = img_element.get_attribute("src")
        # print("Image src:", src)

    finally:
        driver.quit()
    return src


def clean_text(raw):
    #  Lowercase
    text = raw.lower()
    
    #  Remove user mentions @something
    text = re.sub(r'@\w+', '', text)
    
    #  Remove numbers alone on lines
    text = re.sub(r'\b\d+\b', '', text)         # numbers alone
    text = re.sub(r'\b[a-z]*\d+[a-z]*\b', '', text)  
    
    
    text = re.sub(r'\([^)]*\)', '', text)
    
    #  Remove extra spaces and newlines
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def get_img_text(src):
    # Fetch image content from URL
    response = requests.get(src)


    # Check if the content-type is an image
    if "image" in response.headers.get("Content-Type", ""):
        img = Image.open(BytesIO(response.content))

        

        # OCR
        text = pytesseract.image_to_string(img, config='--psm 4')

        # print("Extracted Text:")
        # print(text)
    else:
        print("URL does not contain an image or access denied.")
    return clean_text(text)
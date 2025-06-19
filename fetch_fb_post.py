import joblib
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import tempfile
import time
import re
import emoji
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

vectorizer = joblib.load('tfidf_vectorizer.pkl')
model = joblib.load('nb_spam_classifier.pkl')

stop_words = set(stopwords.words('english'))
lemmatizer = nltk.stem.WordNetLemmatizer()

def get_post_text(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--lang=en-US")
    options.add_argument("--incognito")
    temp_profile = tempfile.mkdtemp()
    options.add_argument(f"--user-data-dir={temp_profile}")

    service = Service("/home/shraddha/AI-Content-Extractor/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        wait = WebDriverWait(driver, 15)

        # Wait for post content div to load
        wait.until(EC.presence_of_element_located((By.XPATH, "//div[@dir='auto']")))

        # Try to find and click "See more" button if present
        try:
            see_more_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(text(), 'See more') or contains(text(), 'see more')]")
            ))
            see_more_button.click()
            # Wait briefly for the content to expand
            wait.until(EC.staleness_of(see_more_button))
        except:
            # No "See more" button found, continue
            pass

        # After expanding, get the page source and parse
        soup = BeautifulSoup(driver.page_source, "html.parser")
        post = soup.find("div", {"dir": "auto", "style": "text-align: start;"}) or soup.find("div", {"dir": "auto"})

        return post.get_text(strip=True) if post else "No post text found."

    finally:
        driver.quit()
    
def clean_text(text):
  text = text.lower()
  text = re.sub(r'http\S+|www\S+', '', text)
  text = emoji.replace_emoji(text,replace='')
  text = re.sub(r"[^a-z0-9$\s']", '', text) 
  words = nltk.word_tokenize(text)
  words = [word for word in words if word not in stop_words]
  words = [lemmatizer.lemmatize(word) for word in words]
  text = ' '.join(words)
  return text


def explain_prediction(text, model, vectorizer):
    cleaned = clean_text(text)
    vector = vectorizer.transform([cleaned])
    feature_names = vectorizer.get_feature_names_out()
    log_prob_spam = model.feature_log_prob_[1]
    log_prob_ham = model.feature_log_prob_[0]
    word_scores = {}
    for col in vector.nonzero()[1]:
        word = feature_names[col]
        score = log_prob_spam[col] - log_prob_ham[col]
        word_scores[word] = score
    sorted_words = sorted(word_scores.items(), key=lambda x: x[1], reverse=True)
    prediction = model.predict(vector)[0]
    proba = model.predict_proba(vector)[0]
    return prediction, proba, sorted_words



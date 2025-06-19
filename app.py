import streamlit as st
import joblib
from fetch_fb_post import get_post_text, clean_text,explain_prediction
from fetch_img import get_img_src,get_img_text


# Load model and vectorizer
vectorizer = joblib.load('tfidf_vectorizer.pkl')
model = joblib.load('nb_spam_classifier.pkl')

st.title(" Facebook Post Spam Detection")

# Select method: text or image
method = st.radio(
    "What do you want to check?",
    ("Check spam in TEXT content", "Check spam in IMAGE content")
)

# Enter URL
url = st.text_input("Enter Facebook Post URL:")


#  Fetch text based on selected method
if st.button("Fetch and Process"):
    if url == "":
        st.warning("Please enter a URL first.")
    else:
        # Depending on radio selection
        if method == "Check spam in TEXT content":
            raw_text = get_post_text(url)
            if raw_text:
                st.session_state['text'] = raw_text
                st.session_state['cleaned'] = clean_text(raw_text)
            else:
                st.error("Could not fetch post text.")
        else:
            raw_src = get_img_src(url)
            raw_text = get_img_text(raw_src)
            if raw_text:
                st.session_state['text'] = raw_text
                st.session_state['cleaned'] = clean_text(raw_text)
            else:
                st.error("Could not extract text from image.")


# Display text and run spam prediction
if 'text' in st.session_state:
    st.subheader("Extracted Text")
    st.text_area("Post Content", st.session_state['text'], height=200)

    if st.button("Check Spam"):
        pred, proba, words = explain_prediction(st.session_state['cleaned'], model, vectorizer)

        if pred == 1:
            st.success("Prediction: Spam")
        else:
            st.success("Prediction: Ham")

        st.write("Spam Probability:", round(proba[1], 4))
        st.write("Ham Probability:", round(proba[0], 4))

        st.subheader("Top Words that affected prediction")
        for word, score in words[:len(words)]:
            st.write(word)

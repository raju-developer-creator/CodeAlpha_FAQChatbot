# CodeAlpha_FAQChatbot

FAQ chatbot built for the CodeAlpha AI Internship (Task 2). Topic: the CodeAlpha AI internship itself.

## How it works
1. FAQs are stored in `faqs.json` (question + answer).
2. Text is preprocessed with NLTK: lowercase, tokenize, remove stop words, Porter stemming.
3. TF-IDF vectors are built for every FAQ with scikit-learn.
4. A user question is vectorized the same way and compared to all FAQs using cosine similarity.
5. The best match is returned. If the score is below the threshold, the bot says it doesn't know and suggests related questions.

## Run
pip install -r requirements.txt
python app.py

Open http://127.0.0.1:5000

## Stack
Python, Flask, NLTK, scikit-learn, HTML/CSS/JavaScript
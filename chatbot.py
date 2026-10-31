import json
from pathlib import Path

from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

THRESHOLD = 0.15  # below this score we say "I don't know"

_tokenizer = RegexpTokenizer(r"[a-z0-9]+")
_stemmer = PorterStemmer()


def preprocess(text: str) -> str:
    """Lowercase -> tokenize -> remove stop words -> stem."""
    tokens = _tokenizer.tokenize(text.lower())
    tokens = [t for t in tokens if t not in ENGLISH_STOP_WORDS]
    return " ".join(_stemmer.stem(t) for t in tokens)


class FAQBot:
    def __init__(self, path: str = "faqs.json"):
        self.faqs = json.loads(Path(path).read_text(encoding="utf-8"))
        # Match against the question + answer so keywords in answers help too
        corpus = [preprocess(f["q"] + " " + f["q"] + " " + f["a"]) for f in self.faqs]
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2))
        self.matrix = self.vectorizer.fit_transform(corpus)

    def ask(self, user_text: str) -> dict:
        cleaned = preprocess(user_text)
        if not cleaned.strip():
            return {"answer": "Please type a question.", "score": 0.0, "suggestions": self.suggest()}
        vec = self.vectorizer.transform([cleaned])
        scores = cosine_similarity(vec, self.matrix)[0]
        order = scores.argsort()[::-1]
        best = int(order[0])
        if scores[best] < THRESHOLD:
            return {
                "answer": "Sorry, I don't have an answer for that. Try one of these questions:",
                "score": float(scores[best]),
                "suggestions": [self.faqs[int(i)]["q"] for i in order[:3]],
            }
        return {
            "answer": self.faqs[best]["a"],
            "matched_question": self.faqs[best]["q"],
            "score": float(scores[best]),
            "suggestions": [],
        }

    def suggest(self, n: int = 4):
        return [f["q"] for f in self.faqs[:n]]
from flask import Flask, send_from_directory, jsonify, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

YANDEX_URL = "https://yandex.ru/maps/org/214850144202/reviews"  # ссылка на отзывы

@app.route('/api/reviews')
def get_reviews():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    response = requests.get(YANDEX_URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    reviews = []
    for review_block in soup.select(".review__body"):
        author = review_block.select_one(".review__author-name")
        text = review_block.select_one(".review__text")
        rating = review_block.select_one(".rating")  # если есть
        reviews.append({
            "author": author.text.strip() if author else "Аноним",
            "text": text.text.strip() if text else "",
            "rating": rating.text.strip() if rating else "—"
        })

    return jsonify({"reviews": reviews})


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/privacy')
def privacy():
    return render_template('privacy.html')


if __name__ == "__main__":
    app.run(debug=True)

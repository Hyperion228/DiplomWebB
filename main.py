from flask import Flask, render_template, request

import requests

from bs4 import BeautifulSoup

app = Flask(__name__)


def search(query):
    search_url = f"https://www.google.com/search?q={query}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

    response = requests.get(search_url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')

    # Извлекаем результаты поиска из блока с классом 'tF2Cxc'

    results = soup.find_all('div', class_='tF2Cxc')

    links = []

    for result in results:

        link_tag = result.find('a')

        if link_tag:
            link = link_tag['href']

            links.append(link)

    return links


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search_page():
    query = request.form['query']

    results = search(query)

    return render_template('results.html', query=query, results=results)


if __name__ == '__main__':
    app.run(debug=True)
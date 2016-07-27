
from flask import Flask, request, jsonify, abort
import requests
from bs4 import BeautifulSoup
import random
import time
app = Flask(__name__)
DILBOT_TOKEN = "YOUR SLACK COMMAND TOKEN"
DILBERT_EPOCH = 608695895

def get_dilbert(today=False):

    epoch = int(time.time()) if today else random.randint(DILBERT_EPOCH, int(time.time()))
    random_dilbert_date = time.strftime('%Y-%m-%d', time.localtime(epoch))

    page = requests.get('http://dilbert.com/strip/{}'.format(random_dilbert_date))
    soup = BeautifulSoup(page.text)
    image_url = soup.findAll('img', class_='img-comic')[0].get('src')

    return (random_dilbert_date, image_url)


@app.route('/dilbot', methods=['POST'])
def dilbot_command():
    print request.form

    token = request.form.get('token', None)
    command = request.form.get('command', None)
    text = request.form.get('text', None)

    if token != DILBOT_TOKEN:
        abort(400)

    date, image_url = get_dilbert(today = 'today' in text)

    return jsonify({
        'response_type': 'in_channel',
        'attachments': [
            {
                'fallback': 'Dilbert Comic',
                'color': '#36a64f',
                'title':"Dilbert Comic for {}".format(date),
                'title_link': "http://dilbert.com/strip/{}".format(date),
                'image_url': image_url,
            }
        ]
    })

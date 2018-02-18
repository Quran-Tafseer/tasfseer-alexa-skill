import logging
import requests
from flask import Flask, render_template
from flask_ask import Ask, statement, question

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch
def welcome():
    welcome_msg = render_template('welcome')
    return question(welcome_msg)


@ask.intent("AyahTafseerIntent", convert={'verse_number': int,
                                          'chapter_number': int})
def ayah_tafseer(chapter_number, verse_number):
    url = 'http://api.quran-tafseer.com/tafseer/9/{}/{}'.format(chapter_number,
                                                                verse_number)
    tafseer_response = requests.get(url)
    tafseer_text = tafseer_response.json()['text']
    msg = render_template('ayah_tafseer', verse_number=verse_number,
                          chapter_number=chapter_number,
                          tafseer_text=tafseer_text)
    return statement(msg)


if __name__ == '__main__':
    app.run(debug=True)

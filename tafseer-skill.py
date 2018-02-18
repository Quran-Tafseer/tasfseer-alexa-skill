import logging
from flask import Flask, render_template
from flask_ask import Ask, statement, question

from services import QuranTafseerService

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
    tafseer_text = QuranTafseerService.ayah_tafseer(
        chapter_number=chapter_number,
        ayah_number=verse_number,
        tafseer_number=9)
    msg = render_template('ayah_tafseer', verse_number=verse_number,
                          chapter_number=chapter_number,
                          tafseer_text=tafseer_text)
    return statement(msg)


if __name__ == '__main__':
    app.run(debug=True)

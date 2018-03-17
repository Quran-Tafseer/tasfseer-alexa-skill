import logging
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

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
    if verse_number is None:
        return statement(render_template('missing_verse_slot'))
    if chapter_number is None:
        return statement(render_template('missing_chapter_slot'))

    tafseer_response = QuranTafseerService.ayah_tafseer(
        chapter_number=chapter_number,
        ayah_number=verse_number,
        tafseer_number=9)
    tafseer_text = tafseer_response.json()['text']
    has_next = 'X-Next-Ayah' in tafseer_response.headers

    if not has_next:
        msg = render_template('ayah_tafseer', verse_number=verse_number,
                              chapter_number=chapter_number,
                              tafseer_text=tafseer_text)
        return statement(msg)
    session.attributes['next_ayah'] = tafseer_response.headers['X-Next-Ayah']
    msg = render_template('ayah_tafseer_next', verse_number=verse_number,
                          chapter_number=chapter_number,
                          tafseer_text=tafseer_text)
    return question(msg)


@ask.intent('YesNextAyah')
def next_ayah_tafseer():
    chapter_number, verse_number = session.attributes['next_ayah'].split(':')
    tafseer_response = QuranTafseerService.ayah_tafseer(
        chapter_number=chapter_number,
        ayah_number=verse_number,
        tafseer_number=9)
    tafseer_text = tafseer_response.json()['text']
    has_next = 'X-Next-Ayah' in tafseer_response.headers

    if not has_next:
        msg = render_template('ayah_tafseer', verse_number=verse_number,
                              chapter_number=chapter_number,
                              tafseer_text=tafseer_text)
        return statement(msg)
    session.attributes['next_ayah'] = tafseer_response.headers['X-Next-Ayah']
    msg = render_template('ayah_tafseer_next', verse_number=verse_number,
                          chapter_number=chapter_number,
                          tafseer_text=tafseer_text)
    return question(msg)


@ask.intent("AMAZON.StopIntent")
def stop_ayah_intent():
    return statement("Thanks for using Quran Tafseer.")


if __name__ == '__main__':
    app.run(debug=True)

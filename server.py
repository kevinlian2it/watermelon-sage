from flask import Flask
from flask import Response, request, jsonify, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your-secret-key'

lessons = [
    {
        "lesson_id": "1",
        "title": "Sound",
        "description": "Tap the watermelon close to your ear, either with your palm or knuckles. Click the images to simulate this tapping.",
        "good_image": "images/base.png",
        "bad_image": "images/base.png",
        "good_alt": "a regular round watermelon",
        "bad_alt": "a regular round watermelon",
        "good_sound": "audio/reverb.mp3",
        "bad_sound": "audio/dud.mp3",
        "good_text": "A bouncy, reverberating sound indicates a crisp and intact interior.",
        "bad_text": "A dull sound with no reverb indicates a bruised, soggy interior.",
    },

    {
        "lesson_id": "2",
        "title": "Weight",
        "description": "When comparing the weights of watermelons, make sure that they’re roughly the same size; we are technically looking for density.",
        "good_image": "images/15_lb.png",
        "bad_image": "images/10_lb.png",
        "good_alt": "15 lb watermelon",
        "bad_alt": "10 lb watermelon",
        "good_text": "A watermelon that is heavy for its size is likely very juicy.",
        "bad_text": "A watermelon that is lighter for its size likely doesn’t contain enough water and is thus not juicy. ",
    },

    {
        "lesson_id": "3",
        "title": "Shape",
        "description": "Note that some cultivation methods artificially select for perfectly round shapes without increasing the quality of the watermelon.",
        "good_image": "images/oval.png",
        "bad_image": "images/bumpy.png",
        "good_alt": "symmetrical oval watermelon",
        "bad_alt": "bumpy watermelon",
        "good_text": "A symmetrical watermelon with an even surface is likely to be juicier and sweeter.",
        "bad_text": "Irregular bumps may be a sign of incomplete pollination or growth stress.",
    },

    {
        "lesson_id": "4",
        "title": "Field Spot",
        "description": "The field spot is the part of the watermelon that was in contact with the ground as it grew.",
        "good_image": "images/dark_field_spot.png",
        "bad_image": "images/pale_field_spot.png",
        "good_alt": "watermelon with dark field spot",
        "bad_alt": "watermelon with pale field spot",
        "good_text": "A darker, yellow-orange field spot indicates a riper, sweeter watermelon that spent longer on the ground.",
        "bad_text": "A light field spot indicates that the watermelon was harvested prematurely and is underripe.",
    },

    {
        "lesson_id": "5",
        "title": "Webbing",
        "description": "Webbing is scar tissue that forms on the watermelon as it grows. Note that some cultivation methods lead to watermelons with no webbing.",
        "good_image": "images/large_webbing.png",
        "bad_image": "images/small_webbing.png",
        "good_alt": "watermelon with lots of webbing",
        "bad_alt": "watermelon with little webbing",
        "good_text": "Lots of webbing indicates extensive bee pollination, usually corresponding to a sweeter watermelon.",
        "bad_text": "Minimal or no webbing indicates less bee pollination. This usually results in a less sweet fruit.",
    },

    {
        "lesson_id": "6",
        "title": "Sheen",
        "description": "Take a close look at how light bounces off the rind’s surface.",
        "good_image": "images/shiny.png",
        "bad_image": "images/dull.png",
        "good_alt": "dull watermelon",
        "bad_alt": "shiny watermelon",
        "good_text": "A dull exterior indicates a watermelon that has spent more time on the vine and is thus adequately ripe.",
        "bad_text": "A shiny watermelon with its waxy protective exterior intact indicates a watermelon that is not yet ripe.",
    }
]

scenarios = [
    { 'title': 'Pick out the sweetest watermelon', 'subtitle': 'Pick out the sweetest watermelon' },
    { 'title': 'Pick out the crispest watermelon', 'subtitle': 'Tap on each watermelon to hear its sound. Pick out the crispest watermelon' },
    { 'title': 'Pick out the ripest watermelon', 'subtitle': 'Pick out the ripest watermelon' },
    { 'title': 'Pick out the sweetest watermelon (webbing)', 'subtitle': 'Pick out the sweetest watermelon' },
    { 'title': 'Pick out the sweetest watermelon (weight)', 'subtitle': 'Drag each watermelon onto the scale to weigh it. Pick out the sweetest watermelon' },
    { 'title': 'Pick out the ripest watermelon', 'subtitle': 'Pick out the ripest watermelon' },
    { 'title': 'Combine traits: pick the best watermelon', 'subtitle': 'Tap the watermelons to hear their sound and weigh them on the scale to help pick the best one' },
    { 'title': 'Combine traits: pick the best watermelon', 'subtitle': 'Tap the watermelons to hear their sound and weigh them on the scale to help pick the best one' },
    { 'title': 'Combine traits: pick the best watermelon', 'subtitle': 'Tap the watermelons to hear their sound and weigh them on the scale to help pick the best one' },
    { 'title': 'Combine traits: pick the best watermelon', 'subtitle': 'Tap the watermelons to hear their sound and weigh them on the scale to help pick the best one' },
]

@app.route("/")
def home_page():
    return render_template('home.html')

@app.route('/learn')
def learn():
    return render_template('learn.html')

@app.route('/challenge/<int:scenario>')
def challenge(scenario=0):
    if scenario < 1 or scenario > len(scenarios):
        return redirect(url_for('challenge', scenario=1))
    score = session.get('score', 0)
    return render_template(
        'challenge.html',
        scenario=scenario,
        scenarios=scenarios,
        score=score
    )

@app.route('/results')
def results():
    score = session.get('score', 0)
    return render_template('results.html', score=score)

if __name__ == '__main__':
   app.run(debug = True, port=5001)
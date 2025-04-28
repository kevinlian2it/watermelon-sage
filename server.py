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
        "bad_text": "A dull sound with no reverb indicates a bruised, soggy interior."
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
        "bad_text": "A watermelon that is lighter for its size likely doesn’t contain enough water and is thus not juicy. "
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
        "bad_text": "Irregular bumps may be a sign of incomplete pollination or growth stress."
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
        "bad_text": "A light field spot indicates that the watermelon was harvested prematurely and is underripe."
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
        "bad_text": "Minimal or no webbing indicates less bee pollination. This usually results in a less sweet fruit."
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
        "bad_text": "A shiny watermelon with its waxy protective exterior intact indicates a watermelon that is not yet ripe."
    }
]

scenarios = [
    { 
        "scenario_id": "1",
        "subtitle": "Drag the sweetest watermelon into the basket",
        "img_1": "images/small_webbing.png",
        "img_2": "images/base.png",
        "img_3": "images/large_webbing.png",
        "basket": "images/basket.png",
        "basket_full": "images/basket_full.png",
        "answer_1": "Wrong!",
        "answer_2": "Wrong!",
        "answer_3": "Correct!",
        "feedback_1": "This watermelon has minimal webbing.",
        "feedback_2": "This watermelon has no webbing.",
        "feedback_3": "This is the watermelon with the most webbing."
    },

    { 
        "scenario_id": "2",
        "subtitle": "Tap on each watermelon to hear its sound. Drag the crispest watermelon into the basket",
        "img_1": "images/base.png",
        "img_2": "images/base.png",
        "img_3": "images/base.png",
        "audio_1": "audio/ok.mp3",
        "audio_2": "audio/reverb.mp3",
        "audio_3": "audio/dud.mp3",
        "basket": "images/basket.png",
        "basket_full": "images/basket_full.png",
        "answer_1": "Wrong!",
        "answer_2": "Correct!",
        "answer_3": "Wrong!",
        "feedback_1": "The sound is somewhat bouncy, but there's a watermelon that reverberates better.",
        "feedback_2": "This watermelon reverberates nicely when tapped.",
        "feedback_3": "This watermelon doesn't reverberate when tapped."
    },

    { 
        "scenario_id": "3",
        "subtitle": "Drag the ripest watermelon into the basket",
        "img_1": "images/dark_field_spot.png",
        "img_2": "images/pale_field_spot.png",
        "img_3": "images/medium_field_spot.png",
        "basket": "images/basket.png",
        "basket_full": "images/basket_full.png",
        "answer_1": "Correct!",
        "answer_2": "Wrong!",
        "answer_3": "Wrong!",
        "feedback_1": "This watermelon has the darkest field spot.",
        "feedback_2": "This watermelon has the palest field spot. Look for the option with the darkest field spot.",
        "feedback_3": "There is an option with a darker field spot."
    },

    { 
        "scenario_id": "4",
        "subtitle": "Drag the sweetest watermelon into the basket",
        "img_1": "images/oval.png",
        "img_2": "images/bumpy.png",
        "img_3": "images/base.png",
        "basket": "images/basket.png",
        "basket_full": "images/basket_full.png",
    },

    { 
        "scenario_id": "5",
        "subtitle": "Drag each watermelon onto the scale to weigh it. Pick out the juiciest watermelon",
        "img_1": "images/base.png",
        "img_2": "images/base.png",
        "img_3": "images/base.png",
        "scale": "images/scale.png",
        "scale_10_lb": "images/scale_10_lb.png",
        "scale_15_lb": "images/scale_15_lb.png",
        "basket": "images/basket.png",
        "basket_full": "images/basket_full.png",
    },

    { 
        "scenario_id": "6",
        "subtitle": "Pick out the ripest watermelon",
        "img_1": "images/shiny.png",
        "img_2": "images/base.png",
        "img_3": "images/dull.png",
        "basket": "images/basket.png",
        "basket_full": "images/basket_full.png",
    },

    { 
        "scenario_id": "7",
        'title': 'Combine traits: pick the best watermelon', 
        'subtitle': 'Tap the watermelons to hear their sound and weigh them on the scale to help pick the best one',
        "img_1": "images/shiny.png",
        "img_2": "images/dark_field_spot.png",
        "img_3": "images/large_webbing.png",
        "basket": "images/basket.png",
        "basket_full": "images/basket_full.png",
    },

    { 
        "scenario_id": "8",
        'title': 'Combine traits: pick the best watermelon',
        'subtitle': 'Tap the watermelons to hear their sound and weigh them on the scale to help pick the best one',
        "img_1": "images/dark_field_spot.png",
        "img_2": "images/oval_dark_fs_small_web.png",
        "img_3": "images/med_fs_large_web.png",
        "basket": "images/basket.png",
        "basket_full": "images/basket_full.png",
    },

    { 
        "scenario_id": "9",
        'title': 'Combine traits: pick the best watermelon',
        'subtitle': 'Tap the watermelons to hear their sound and weigh them on the scale to help pick the best one',
        "img_1": "images/oval_pale_fs_large_web.png",
        "img_2": "images/shiny_bumpy_small_web.png",
        "img_3": "images/dull.png",
        "basket": "images/basket.png",
        "basket_full": "images/basket_full.png",
    },

    { 
        "scenario_id": "10",
        'title': 'Combine traits: pick the best watermelon',
        'subtitle': 'Tap the watermelons to hear their sound and weigh them on the scale to help pick the best one',
        "img_1": "images/oval_dark_fs_small_web.png",
        "img_2": "images/dark_fs_small_web_dull.png",
        "img_3": "images/dark_fs_small_web_shiny.png",
        "basket": "images/basket.png",
        "basket_full": "images/basket_full.png",
    }
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

@app.route('/submit_answer/<int:scenario>/<int:choice>', methods=['POST'])
def submit_answer(scenario, choice):
    # guard: valid scenario and choice
    if not (1 <= scenario <= len(scenarios) and 1 <= choice <= 3):
        return jsonify({'error': 'Invalid request'}), 400

    # check correctness
    correct = (scenarios[scenario-1].get(f'answer_{choice}') == 'Correct!')
    if correct:
        session['score'] = session.get('score', 0) + 1

    return jsonify({
        'score': session.get('score', 0),
        'correct': correct
    })

@app.route('/results')
def results():
    score = session.get('score', 0)
    return render_template('results.html', score=score)

if __name__ == '__main__':
   app.run(debug = True, port=5001)
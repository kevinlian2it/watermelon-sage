from flask import Flask
from flask import Response, request, jsonify, render_template, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key'

SERVER_START = datetime.utcnow()

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
        "lesson_id": "4",
        "title": "Sheen",
        "description": "Take a close look at how light bounces off the rind’s surface.",
        "bad_image": "images/shiny.png",
        "good_image": "images/dull.png",
        "good_alt": "dull watermelon",
        "bad_alt": "shiny watermelon",
        "good_text": "A dull exterior indicates a watermelon that has spent more time on the vine and is thus adequately ripe.",
        "bad_text": "A shiny watermelon with its waxy protective exterior intact indicates a watermelon that is not yet ripe."
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
        "title": "Shape",
        "description": "Note that some cultivation methods artificially select for perfectly round shapes without increasing the quality of the watermelon.",
        "good_image": "images/oval.png",
        "bad_image": "images/bumpy.png",
        "good_alt": "symmetrical oval watermelon",
        "bad_alt": "bumpy watermelon",
        "good_text": "A symmetrical watermelon with an even surface is likely to be juicier and sweeter.",
        "bad_text": "Irregular bumps may be a sign of incomplete pollination or growth stress."
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
        "answer_1": "Correct!",
        "answer_2": "Wrong!",
        "answer_3": "Correct!",
        "feedback_1": "This is one of the two symmetrical watermelons.",
        "feedback_2": "This watermelon has irregular bumps on it.",
        "feedback_3": "This is one of the two symmetrical watermelons."
    },

    { 
        "scenario_id": "5",
        "subtitle": "Drag each watermelon onto the scale to weigh it. Pick out the juiciest watermelon",
        "img_1": "images/base.png",
        "img_2": "images/base.png",
        "img_3": "images/base.png",
        "scale": "images/scale.png",
        "scale_1": "images/scale_10_lb.png",
        "scale_2": "images/scale_15_lb.png",
        "scale_3": "images/scale_12_lb.png",
        "basket": "images/basket.png",
        "basket_full": "images/basket_full.png",
        "answer_1": "Wrong!",
        "answer_2": "Correct!",
        "answer_3": "Wrong!",
        "feedback_1": "This is the lightest watermelon.",
        "feedback_2": "This is the heaviest/densest watermelon.",
        "feedback_3": "This is not the heaviest watermelon."
    },

    { 
        "scenario_id": "6",
        "subtitle": "Drag the ripest watermelon into the basket",
        "img_1": "images/shiny.png",
        "img_2": "images/base.png",
        "img_3": "images/dull.png",
        "basket": "images/basket.png",
        "basket_full": "images/basket_full.png",
        "answer_1": "Wrong!",
        "answer_2": "Wrong!",
        "answer_3": "Correct!",
        "feedback_1": "This is the shiniest watermelon.",
        "feedback_2": "Close! Not the worst watermelon, but there is an even duller one.",
        "feedback_3": "This the dullest watermelon."
    },

    { 
        "scenario_id": "7",
        "title": "Combine traits: drag the best watermelon into the basket", 
        "subtitle": "Tap the watermelons to hear their sound and weigh them on the scale to help pick the best one",
        "img_1": "images/shiny.png",
        "img_2": "images/dark_field_spot.png",
        "img_3": "images/large_webbing.png",
        "audio_1": "audio/dud.mp3",
        "audio_2": "audio/reverb.mp3",
        "audio_3": "audio/ok.mp3",
        "scale": "images/scale.png",
        "scale_1": "images/scale_10_lb.png",
        "scale_2": "images/scale_14_lb.png",
        "scale_3": "images/scale_15_lb.png",
        "basket": "images/basket.png",
        "basket_full": "images/basket_full.png",
        "answer_1": "Wrong!",
        "answer_2": "Correct!",
        "answer_3": "Wrong!",
        "feedback_1": "This watermelon is shiny, has no webbing or field spot, has a bad sound, and has the lightest weight. It is the worst pick.",
        "feedback_2": "This watermelon has a good sound, the darkest field spot, and is the heaviest out of the bunch, making it a great contender overall!",
        "feedback_3": "Not the absolute worst pick, but despite its larger webbing and relatively heavy weight, this watermelon has only a moderately bouncy sound and no visible field spot."
    },

    { 
        "scenario_id": "8",
        "title": "Combine traits: drag the best watermelon into the basket", 
        "subtitle": "Tap the watermelons to hear their sound and weigh them on the scale to help pick the best one",
        "img_1": "images/dark_field_spot.png",
        "img_2": "images/oval_dark_fs_small_web.png",
        "img_3": "images/med_fs_large_web.png",
        "audio_1": "audio/ok.mp3",
        "audio_2": "audio/dud.mp3",
        "audio_3": "audio/reverb.mp3",
        "scale": "images/scale.png",
        "scale_1": "images/scale_11_lb.png",
        "scale_2": "images/scale_15_lb.png",
        "scale_3": "images/scale_15_lb.png",
        "basket": "images/basket.png",
        "basket_full": "images/basket_full.png",
        "answer_1": "Wrong!",
        "answer_2": "Wrong!",
        "answer_3": "Correct!",
        "feedback_1": "Despite the dark field spot, this watermelon is very light for its size, has no webbing, and produces a dead sound when tapped.",
        "feedback_2": "Despite its dark field spot, this watermelon has little webbing and produces only a moderately bouncy sound. Though tied for the heaviest weight, it is larger in size and therefore less dense.",
        "feedback_3": "This watermelon has the best sound, heaviest weight for its size, and largest webbing. Though the field spot is not the darkest, it is also not pale."
    },

    { 
        "scenario_id": "9",
        "title": "Combine traits: drag the best watermelon into the basket", 
        "subtitle": "Tap the watermelons to hear their sound and weigh them on the scale to help pick the best one",
        "img_1": "images/oval_pale_fs_large_web.png",
        "img_2": "images/shiny_bumpy_small_web.png",
        "img_3": "images/dull.png",
        "audio_1": "audio/ok.mp3",
        "audio_2": "audio/dud.mp3",
        "audio_3": "audio/ok.mp3",
        "scale": "images/scale.png",
        "scale_1": "images/scale_11_lb.png",
        "scale_2": "images/scale_10_lb.png",
        "scale_3": "images/scale_12_lb.png",
        "basket": "images/basket.png",
        "basket_full": "images/basket_full.png",
        "answer_1": "Correct!",
        "answer_2": "Wrong!",
        "answer_3": "Correct!",
        "feedback_1": "To better mirror real life, this round didn’t have any great options. This watermelon is a solid candidate from this batch because of its large webbing, its (albeit pale) field spot, and its moderately reverberant sound.",
        "feedback_2": "To better mirror real life, this round didn’t have any great options. However, this watermelon is not a good choice because of its bumpiness, dead sound, lack of a field spot, minimal webbing, and lighter weight.",
        "feedback_3": "To better mirror real life, this round didn’t have any great options. This watermelon is a solid candidate from this batch because of its dull exterior, comparatively heavier weight, and somewhat reverberant sound."
    },

    { 
        "scenario_id": "10",
        "title": "Combine traits: drag the best watermelon into the basket", 
        "subtitle": "Tap the watermelons to hear their sound and weigh them on the scale to help pick the best one",
        "img_1": "images/oval_dark_fs_small_web.png",
        "img_2": "images/dark_fs_small_web_dull.png",
        "img_3": "images/dark_fs_small_web_shiny.png",
        "basket": "images/basket.png",
        "audio_1": "audio/reverb.mp3",
        "audio_2": "audio/reverb.mp3",
        "audio_3": "audio/ok.mp3",
        "scale": "images/scale.png",
        "scale_1": "images/scale_14_lb.png",
        "scale_2": "images/scale_14_lb.png",
        "scale_3": "images/scale_10_lb.png",
        "basket_full": "images/basket_full.png",
        "answer_1": "Wrong!",
        "answer_2": "Correct!",
        "answer_3": "Wrong!",
        "feedback_1": "To better mirror real life, this round had watermelons that looked very similar. Though alright, this watermelon is not the best one because it is not the dullest and or densest option (tied for heaviest, but larger in size so it's less dense).",
        "feedback_2": "To better mirror real life, this round had watermelons that looked very similar. This watermelon is the best one because it had the dullest exterior and tied for heaviest with a watermelon larger in size (making this one the densest).",
        "feedback_3": "To better mirror real life, this round had watermelons that looked very similar. That said, this is the worst watermelon because of its shiny exterior, only moderately reverberant sound, and light weight."
    }
]

@app.before_request
def reset_after_restart():
    # only care about our learn routes
    if request.endpoint in ('learn', 'lesson'):
        sess_start = session.get('session_start')
        if not sess_start or datetime.fromisoformat(sess_start) < SERVER_START:
            # first time this session touches learn after a server restart
            session['session_start']   = SERVER_START.isoformat()
            session['visited_lessons'] = []

@app.route("/")
def home_page():
    return render_template('home.html')

@app.route('/learn')
def learn():
    visited = session.get('visited_lessons', [])
    return render_template('learn.html',
                           lessons=lessons,
                           visited_lessons=visited)

@app.route('/learn/<int:lesson_id>')
def lesson(lesson_id):
    if not (1 <= lesson_id <= len(lessons)):
        return redirect(url_for('learn'))

    # mark visited
    visited = set(session.get('visited_lessons', []))
    visited.add(lesson_id)
    session['visited_lessons'] = list(visited)

    data = lessons[lesson_id-1]
    return render_template('lesson.html', lesson=data)

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

    answered = session.get('answered_scenarios', [])
    already = scenario in answered

    # check correctness
    correct = (scenarios[scenario-1].get(f'answer_{choice}') == 'Correct!')

    if (not already) and correct:
        session['score'] = session.get('score', 0) + 1

    if not already:
        answered.append(scenario)
        session['answered_scenarios'] = answered

    return jsonify({
        'score': session.get('score', 0),
        'correct': correct
    })

@app.route('/results')
def results():
    score = session.get('score', 0)
    return render_template('results.html', score=score)

@app.route('/retry')
def retry():
    # reset the score and answered list
    session['score'] = 0
    session['answered_scenarios'] = []
    # go back to scenario 1
    return redirect(url_for('challenge', scenario=1))

if __name__ == '__main__':
   app.run(debug = True, port=5001)
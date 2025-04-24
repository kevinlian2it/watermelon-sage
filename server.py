from flask import Flask
from flask import Response, request, jsonify, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your-secret-key'

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
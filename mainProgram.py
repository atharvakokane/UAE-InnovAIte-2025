from flask import Flask, render_template, request, redirect, url_for # type: ignore
import sentiment
from flask import Flask, jsonify, render_template # type: ignore
import subprocess
import json
app = Flask(__name__, static_folder="static", template_folder="templates")

emotion = ""

def run_script(script_path):
    try:
        result = subprocess.run(["python", script_path], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return str(e)

@app.route('/', methods=["GET", "POST"])
def home():
    return render_template('home.html')

@app.route('/journal.html', methods=["GET", "POST"])
def journal():
    return render_template('journal.html')

@app.route('/account', methods=["GET", "POST"])
def account():
    return render_template('login.html')

@app.route('/game')
def game():
    data = json.dumps(request.args.get("result"))
    emotion = sentiment.predict_emotion(data)
    return render_template("game.html",result = emotion)

@app.route('/profile.html')
def profile():
    return render_template("profile.html")

@app.route('/run/relaxation', methods=['GET'])
def run_relaxation():
    output = run_script("relaxationgame/main.py")
    return jsonify({"output": output})

@app.route('/run/focus', methods=['GET'])
def run_focus():
    output = run_script("focusgame/main.py")
    return jsonify({"output": output})

@app.route('/run/empowerment', methods=['GET'])
def run_empowerment():
    output = run_script("empowermentgame/main.py")
    return jsonify({"output": output})


app.run(debug=True)
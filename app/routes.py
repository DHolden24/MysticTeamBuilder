from app import app
from flask import render_template, jsonify, request
from Dex import Dex
from Suggester import Suggester

dex = Dex()
suggester = Suggester()

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html', title='Home')

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/history')
def history():
    return render_template('history.html', title='Change Log')

@app.route('/vgcLegalPokemon', methods=['GET'])
def legalMons():
    return jsonify(dex.get_legal_mons())

@app.route('/getSuggestions', methods=['POST', 'GET'])
def getSuggestions():
    submitted_team = [x.replace("-Gmax", "").replace("-Rapid-Strike", "") for x in request.get_json()["team"] if x != "None"]

    if 1 <= len(submitted_team) <= 5:
        types = []
        for i in submitted_team:
            mon_type = dex.get_mon_type(i)
            for t in mon_type:
                types.append(dex.get_type(t))

        while len(types) < len(submitted_team) * 2:
            types.append(-1)

        team = [dex.get_mon(p) for p in submitted_team]

        suggested_pokemon, suggested_types = suggester.get_suggestions(team, types, dex)

        suggestions = {"note": "None",
                       "pokemon": [(dex.get_mon(p), s) for p, s in suggested_pokemon],
                       "types": [(dex.get_type(t), s) for t, s in suggested_types]}
    elif len(submitted_team) > 5:
        suggestions = {"note": "The team is full!",
                       "pokemon": "",
                       "types": ""}
    elif len(submitted_team) < 1:
        suggestions = {"note": "Add a Pokemon to the Team to Get Suggestions!",
                       "pokemon": "",
                       "types": ""}

    return jsonify(suggestions)
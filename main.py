import flask
from flask import request, jsonify, render_template, url_for
from api import getBatsmenStats, getBowlerStats
from models import getVenue, getCity, getPlayers, getTeams
import pickle
app = flask.Flask(__name__)
app.config["DEBUG"] = True

def convert_over(input):
    a, b = input.split(".")
    return int(a) * 6 + int(b)

def processData(bat_team, bowl_team, city, venue, batsmen, bowlers, toss_winner, toss_decision):
    teamMap = {
        'Mumbai Indians' : 1,
        'Kolkata Knight Riders' : 2,
        'Royal Challengers Bangalore' : 3,
        'Deccan Chargers' : 4,
        'Chennai Super Kings' : 5,
        'Rajasthan Royals' : 6,
        'Delhi Daredevils' : 7,
        'Gujarat Lions' : 8,
        'Kings XI Punjab' : 9,
        'Sunrisers Hyderabad' : 10,
        'Rising Pune Supergiants' : 11,
        'Rising Pune Supergiant' : 11,
        'Kochi Tuskers Kerala' : 12,
        'Pune Warriors' : 13,
        'Delhi Capitals' : 7
    }
    tossDecisionMap = {
        'bat' : 0,
        'field' : 1
    }
    cities = getCity()
    citiesMap = {}
    i = 1
    for city in cities:
        citiesMap[city] = i
        i += 1
    venues = getVenue()
    venuesMap = {}
    i = 1
    for venue in venues:
        venuesMap[venue] = i
        i += 1
    strikeRate = 0
    for b in batsmen:
        strikeRate += float(getBatsmenStats(b))
    strikeRate /= len(batsmen)
    # strikeRate = 120.0
    economy = 0
    print(bowlers)
    for b in bowlers:
        print("Hello", getBowlerStats(b))
        economy += float(getBowlerStats(b))
    economy /= len(bowlers)
    batTeam = teamMap.get(bat_team)
    bowlTeam = teamMap.get(bowl_team)
    tossWinner = teamMap.get(toss_winner)
    tossDecision = tossDecisionMap.get(toss_decision)
    city = citiesMap.get(city)
    venue = venuesMap.get(venue)
    return [batTeam, bowlTeam, city, tossDecision, tossWinner, venue, strikeRate, economy]

@app.route('/', methods = ["GET"])
def hello():
    return render_template('index.html')

@app.route('/ongoing', methods = ["GET"])
def predictOngoing():
    return render_template('ongoing.html'
    )

@app.route('/bmatch', methods = ["GET"])
def beforeMatch():
    return render_template('beforematch.html', teams=getTeams(), cities=getCity(), venues=getVenue(), players=getPlayers()
    )

@app.route('/predict_start', methods = ["POST"])
def predict_start():
    bat_team = request.form.get("bat-team")
    bowl_team = request.form.get("bowl-team")
    city = request.form.get("city")
    venue = request.form.get("venue")
    batsmen = request.form.getlist("batsmen")
    bowlers = request.form.getlist("bowler")
    toss_winner = request.form.get("toss-winner")
    toss_decision = request.form.get("toss-decision")
    data = processData(bat_team, bowl_team, city, venue, batsmen, bowlers, toss_winner, toss_decision)
    loaded_model = pickle.load(open('models/model1.sav', 'rb'))
    score = str(int(loaded_model.predict([data])[0]))
    return render_template('predict.html', score=score)

@app.route('/predict_ongoing', methods = ["POST"])
def predict_ongoing():
    total_runs = request.form.get("run")
    balls_faced = request.form.get("balls-faced")
    strike_rate = request.form.get("strike-rate")
    hundreds = request.form.get("centuries")
    wickets_taken = request.form.get("wickets")
    economy_rate = request.form.get("economy")
    ball_number = request.form.get("curr_over")
    score = request.form.get("curr_score")
    pred_ball = request.form.get("over-ball")
    
    data = [
        int(total_runs),
        int(balls_faced),
        float(strike_rate),
        int(hundreds),
        int(wickets_taken),
        float(economy_rate),
        convert_over(ball_number),
        int(score),
        convert_over(pred_ball)
    ]
    loaded_model = pickle.load(open('models/model2.sav', 'rb'))
    new_score = str(int(loaded_model.predict([data])[0]))
    return render_template('predict.html', score=new_score)
    
if __name__ == '__main__':
    app.run()


import json
from flask import Flask,render_template,request,redirect,flash,url_for
from datetime import datetime


class ClubNotFound(Exception):
    pass

class CompetitionNotFound(Exception):
    pass

def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

def get_club(email):
    for club in clubs:
        if email == club.get('email'):
            return club
    raise ClubNotFound

def get_club_by_name(club):
    for c in clubs:
        if club == c.get('name'):
            return c
    raise ClubNotFound

def get_competition_by_name(competition_name):
    for competition in competitions:
        if competition_name == competition.get('name'):
            return competition
    raise CompetitionNotFound

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    try:
        club = get_club(request.form['email'])
    except ClubNotFound:
        flash("L'email n'existe pas, veuillez rééssayer.")
        return redirect(url_for('index'))
    return render_template('welcome.html',club=club,competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    max_points_club = 12
    if int(foundClub['points']) < 12:
        max_points_club = foundClub['points']
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition,
                               max_points_club=max_points_club)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = get_competition_by_name(request.form['competition'])
    club = get_club_by_name(request.form['club'])
    placesRequired = int(request.form['places'])
    today_date = datetime.now()
    competition_date = datetime.strptime(competition['date'], "%Y-%m-%d %H:%M:%S")
    if int(club["points"]) >= placesRequired:
        if placesRequired > 0 and placesRequired <= 12:
            if competition_date > today_date:
                competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
                club["points"] = int(club["points"]) - placesRequired
                flash('Great-booking complete!')
            else:
                 flash("The competition is past, your reservation is not valid.")
        else:
            flash("You can not redeem less than 1 and more than 12 points by club.")
    else:
        flash('You can not redeem more points than available.')
    return render_template('welcome.html', club=club, competitions=competitions)

@app.route('/displayPoints',methods=['GET'])
def display_points():
    clubs = loadClubs()
    return render_template('points_by_team.html', clubs=clubs)

@app.route('/logout')
def logout():
    return redirect(url_for('index'))
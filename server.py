import json
from flask import Flask, render_template, request, redirect, flash, url_for, session


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


@app.route('/', methods=['POST', 'GET'])
def index():
    if session.get('email') is not None:

        club = [club for club in clubs if club['email'] == session.get('email')]

        return render_template('welcome.html', club=club[0], competitions=competitions)
    else:
        if request.method == "POST":
            try:
                club = [club for club in clubs if club['email'] == request.form['email']]
                session['email'] = request.form['email']
                return render_template('welcome.html', club=club[0], competitions=competitions)
            except:
                flash("Bad email or password")
                return render_template('index.html')
        else:
            return render_template('index.html')


@app.route('/book/<competition>/<club>')
def book(competition, club):
    if session.get('email'):
        try:
            foundClub = [c for c in clubs if c['name'] == club][0]
            foundCompetition = [c for c in competitions if c['name'] == competition][0]
            if foundClub['email'] == session.get('email'):
                return render_template('booking.html', club=foundClub, competition=foundCompetition)
            else:

                club = [club for club in clubs if club['email'] == session.get('email')]
                flash('you try to book for a club that is not yours')
                return render_template('welcome.html', club=club[0], competitions=competitions)
        except:
            club = [club for club in clubs if club['email'] == session.get('email')]
            flash('Club or competition not found!')
            return render_template('welcome.html', club=club[0], competitions=competitions)

    else:
        flash('Not connected')
        return render_template('index.html')


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    if session.get('email'):
        try:
            competition = [c for c in competitions if c['name'] == request.form['competition']][0]
            club = [c for c in clubs if c['name'] == request.form['club']][0]
            placesRequired = int(request.form['places'])
            PlacesByPoints = placesRequired * 3
            if club['email'] == session.get('email'):
                if club['email'] == session.get('email'):
                    print(club['email'])
                    if (PlacesByPoints <= 12) and (int(competition['numberOfPlaces']) - PlacesByPoints >= 0) and \
                            (int(club["points"]) - PlacesByPoints >= 0):
                        competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - PlacesByPoints
                        club["points"] = int(club['points']) - PlacesByPoints
                        flash('Great-booking complete!')
                        return render_template('welcome.html', club=club, competitions=competitions)
                    else:
                        print('pas ok')
                        flash("You can t book")
                        return render_template('welcome.html', club=club, competitions=competitions)
            else:
                flash('You try to book for another club')
                club = [club for club in clubs if club['email'] == session.get('email')]
                return render_template('welcome.html', club=club[0], competitions=competitions)
        except:
            flash("Club or competition not found")
            club = [club for club in clubs if club['email'] == session.get('email')]
            return render_template('welcome.html', club=club[0], competitions=competitions)
    else:
        flash('Not connected')
        return render_template('index.html')


@app.route('/display')
def display():
    return render_template('display.html', club=clubs)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

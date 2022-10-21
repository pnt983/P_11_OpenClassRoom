import pytest
import server
from server import get_club_by_name, get_competition_by_name, ClubNotFound, CompetitionNotFound


def test_get_club_by_name(clubs_fixture):
    club = get_club_by_name(clubs_fixture[0]['name'])
    assert club['email'] == 'john@simplylift.co'

def test_get_club_by_bad_name():
    with pytest.raises(ClubNotFound):
        get_club_by_name('BadNameClub')

def test_get_competition_by_name(competitions_fixture):
    competition = get_competition_by_name(competitions_fixture[0]['name'])
    assert competition["date"] == '2020-03-27 10:00:00'

def test_get_competition_by_bad_name():
    with pytest.raises(CompetitionNotFound):
        get_competition_by_name('BadNameCompetition')

def test_purchasePlaces(client, monkeypatch, competitions_fixture, clubs_fixture):

    def mock_get_competitions_by_name(competition):
        return {
            "name": "Spring Festival",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "25" 
        }
    
    def mock_get_club_by_name(club):
        return {
            "name":"Simply Lift",
            "email":"john@simplylift.co",
            "points":"13"
        }
    
    monkeypatch.setattr(server, 'get_competition_by_name', mock_get_competitions_by_name)
    monkeypatch.setattr(server, 'get_club_by_name', mock_get_club_by_name)
    monkeypatch.setattr(server, 'competitions', competitions_fixture)
    monkeypatch.setattr(server, 'clubs', clubs_fixture)

    response = client.post('/purchasePlaces', data={'club': 'Simply Lift', 'competition': 'Spring Festival', 'places': 1})
    data = response.data.decode()

    assert response.status_code == 200
    assert data.find('<h3>Competitions:</h3>')

def test_purchasePlaces_good_asking_places():
    club = {
        "name":"Simply Lift",
        "email":"john@simplylift.co",
        "points":"13"
    }

    club_points = int(club['points'])
    placesRequired = 5    
    calcul = club_points - placesRequired
    expected_value = 8

    assert calcul == expected_value

def test_purchasePlaces_bad_asking_places(client):

    response = client.post('/purchasePlaces', data={'club': 'Simply Lift',
                                                        'competition': 'Spring Festival', 'places': 14
                                                        }
                               )

    data = response.data.decode()

    assert data.find('You can not redeem more points than available.') != -1

def test_purchasePlaces_more_than_12_places(client):
    response= client.post('/purchasePlaces',data={'club': "Simply Lift", 
                                                  "competition": 'Spring Festival', "places": 13})

    data = response.data.decode()

    assert data.find ("You can not redeem less than 1 and more than 12 points by club.") != -1

def test_purchasePlaces_less_than_12_places(client):
    response= client.post('/purchasePlaces',data={'club': "Simply Lift", 
                                                  "competition": 'Spring Festival', "places": 0})

    data = response.data.decode()

    assert data.find ("You can not redeem less than 1 and more than 12 points by club.") != -1

def test_purchasePlaces_old_competition(client, monkeypatch, clubs_fixture, competitions_fixture):
    monkeypatch.setattr(server, 'clubs', clubs_fixture)
    monkeypatch.setattr(server, 'competitions', competitions_fixture)
    response = client.post('/purchasePlaces', data={'club': 'Simply Lift', 'competition': 'Fall Classic', 'places': 1})

    data = response.data.decode()

    assert data.find ("The competition is past, your reservation is not valid.") != -1

def test_purchasePlaces_good_date_competition(client, monkeypatch, clubs_fixture, competitions_fixture):
    monkeypatch.setattr(server, 'clubs', clubs_fixture)
    monkeypatch.setattr(server, 'competitions', competitions_fixture)
    response = client.post('/purchasePlaces', data={'club': 'Simply Lift', 'competition': 'Competition Test Date', 'places': 1})

    data = response.data.decode()

    assert data.find ("Great-booking complete!") != -1

def test_purchasePlaces_points_club_change(client, monkeypatch, clubs_fixture, competitions_fixture):
    club = {
        "name":"Simply Lift",
        "email":"john@simplylift.co",
        "points":"13"
    }

    monkeypatch.setattr(server, 'clubs', clubs_fixture)
    monkeypatch.setattr(server, 'competitions', competitions_fixture)
    response = client.post('/purchasePlaces', data={'club': 'Simply Lift', 'competition': 'Competition Test Date', 'places': 5})

    data = response.data.decode()

    club_points = int(club['points'])
    placesRequired = 5
    calcul = club_points - placesRequired
    expected_value = f'Points available: {str(calcul)}'
    assert data.find(expected_value) != -1

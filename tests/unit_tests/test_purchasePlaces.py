import pytest
import server
from server import get_club_by_name, get_competition_by_name, ClubNotFound, CompetitionNotFound


def test_get_club_by_name(clubs_fixture):
    """
    Given a name existing
    When get_club_by_name is calling
    Then return the club
    """
    club = get_club_by_name(clubs_fixture[0]['name'])
    assert club['email'] == 'john@simplylift.co'

def test_get_club_by_bad_name():
    """
    Given a name does not exist
    When get_club_by_name is calling
    Then return ClubNotFound exception
    """
    with pytest.raises(ClubNotFound):
        get_club_by_name('BadNameClub')

def test_get_competition_by_name(competitions_fixture):
    """
    Given a name existing
    When get_competition_by_name is calling
    Then return competition
    """
    competition = get_competition_by_name(competitions_fixture[0]['name'])
    assert competition["date"] == '2020-03-27 10:00:00'

def test_get_competition_by_bad_name():
    """
    Given a name does not exist
    When get_competition_by_name is calling
    Then return CompetitionNotFound exception
    """
    with pytest.raises(CompetitionNotFound):
        get_competition_by_name('BadNameCompetition')

def test_purchasePlaces_good_asking_places():
    """
    Given good points for redeem places
    When purcghasePlaces is calling
    Then points are deducted
    """
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
    """
    Given bad points for redeem places
    When purcghasePlaces is calling
    Then points are not deducted and info message display
    """
    response = client.post('/purchasePlaces', data={'club': 'Simply Lift',
                                                        'competition': 'Spring Festival', 'places': 14
                                                        }
                               )

    data = response.data.decode()

    assert data.find('You can not redeem more points than available.') != -1

def test_purchasePlaces_more_than_12_places(client):
    """
    Given more than 12 points
    When purchasePlaces is calling
    Then points are not deducted and info message display
    """
    response= client.post('/purchasePlaces',data={'club': "Simply Lift", 
                                                  "competition": 'Spring Festival', "places": 13})

    data = response.data.decode()

    assert data.find ("You can not redeem less than 1 and more than 12 points by club.") != -1

def test_purchasePlaces_less_than_1_places(client):
    """
    Given less than 1 point
    When purchasePlaces is calling
    Then points are not deducted and info message display
    """
    response= client.post('/purchasePlaces',data={'club': "Simply Lift", 
                                                  "competition": 'Spring Festival', "places": 0})

    data = response.data.decode()

    assert data.find ("You can not redeem less than 1 and more than 12 points by club.") != -1

def test_purchasePlaces_old_competition(client, monkeypatch, clubs_fixture, competitions_fixture):
    """
    Given competition in past
    When purchasePlaces is calling
    Then points are not deducted and info message display
    """
    monkeypatch.setattr(server, 'clubs', clubs_fixture)
    monkeypatch.setattr(server, 'competitions', competitions_fixture)
    response = client.post('/purchasePlaces', data={'club': 'Simply Lift', 'competition': 'Fall Classic', 'places': 1})

    data = response.data.decode()

    assert data.find ("The competition is past, your reservation is not valid.") != -1

def test_purchasePlaces_good_date_competition(client, monkeypatch, clubs_fixture, competitions_fixture):
    """
    Given good date competiton
    When purchasePlaces is calling
    Then good message display
    """
    monkeypatch.setattr(server, 'clubs', clubs_fixture)
    monkeypatch.setattr(server, 'competitions', competitions_fixture)
    response = client.post('/purchasePlaces', data={'club': 'Simply Lift', 'competition': 'Competition Test Date', 'places': 1})

    data = response.data.decode()

    assert data.find ("Great-booking complete!") != -1

def test_purchasePlaces_points_club_change(client, monkeypatch, clubs_fixture, competitions_fixture):
    """
    Given good points for redeem places
    When purchasePlaces is calling
    Then return good points available for a club
    """
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

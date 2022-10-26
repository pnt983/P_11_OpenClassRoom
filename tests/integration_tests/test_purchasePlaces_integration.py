import server


def test_purchasePlaces(client, monkeypatch, competitions_fixture, clubs_fixture):
    """
    Given good competition and good points
    When purchasePlaces is calling
    Then the welcome page is display
    """
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
    assert data.find('Competitions:') != -1
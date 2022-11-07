import server


def test_server(monkeypatch, client, clubs_fixture, competitions_fixture):
    """
    Given 
    When 
    Then 
    """
    # Test de index()
    response_index = client.get('/')
    data = response_index.data.decode()

    assert response_index.status_code == 200
    assert data.find("Welcome to the GUDLFT Registration Portal!") != -1

    # Test de showSummary()
    response_showSummary = client.post('/showSummary', data={'email': 'john@simplylift.co'})
    data = response_showSummary.data.decode()

    assert response_showSummary.status_code == 200
    assert data.find('Welcome, john@simplylift.co') != -1

    # Test de purchasePlaces()
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

    response_purchasePlaces = client.post('/purchasePlaces', data={'club': 'Simply Lift', 'competition': 'Spring Festival', 'places': 1})
    data = response_purchasePlaces.data.decode()

    assert response_purchasePlaces.status_code == 200
    assert data.find('Competitions:') != -1

    # Test de book()
    monkeypatch.setattr(server, 'clubs', clubs_fixture)
    monkeypatch.setattr(server, 'competitions', competitions_fixture)

    club = clubs_fixture[0]['name']
    competition = competitions_fixture[0]['name']

    response_book = client.get(f'/book/{competition}/{club}')
    data = response_book.data.decode()

    assert response_book.status_code == 200
    assert data.find('Booking for') != -1

    # Test de logout()
    response_logout = client.get('/logout')
    data = response_logout.data.decode()

    assert response_logout.status_code == 302
    assert data.find("Redirecting") != -1

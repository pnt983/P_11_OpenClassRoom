import server

def test_book_max_points_more_than_12(client, monkeypatch, competitions_fixture, clubs_fixture):
    """
    Given club points is more than 12
    When book function is calling
    Then max points club == 12
    """
    monkeypatch.setattr(server, 'clubs', clubs_fixture)
    monkeypatch.setattr(server, 'competitions', competitions_fixture)

    club = clubs_fixture[0]['name']
    competition = competitions_fixture[0]['name']

    response = client.get(f'/book/{competition}/{club}')
    data = response.data.decode()

    assert data.find('max="12"') != -1

def test_book_max_points_less_than_12(client, monkeypatch, competitions_fixture, clubs_fixture):
    """
    Given club points is more than 12
    When book function is calling
    Then max points club == 12
    """
    monkeypatch.setattr(server, 'clubs', clubs_fixture)
    monkeypatch.setattr(server, 'competitions', competitions_fixture)

    club = clubs_fixture[1]['name']
    competition = competitions_fixture[0]['name']

    response = client.get(f'/book/{competition}/{club}')
    data = response.data.decode()

    assert data.find('max="4"') != -1

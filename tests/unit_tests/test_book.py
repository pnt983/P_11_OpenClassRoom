import server


def test_book_ok(client, monkeypatch, competitions_fixture, clubs_fixture):
    """
    Given good club and good competition
    When book function is calling
    Then display booking page
    """
    monkeypatch.setattr(server, 'clubs', clubs_fixture)
    monkeypatch.setattr(server, 'competitions', competitions_fixture)

    club = clubs_fixture[0]['name']
    competition = competitions_fixture[0]['name']

    response = client.get(f'/book/{competition}/{club}')
    data = response.data.decode()

    assert response.status_code == 200
    assert data.find('Booking for') != -1

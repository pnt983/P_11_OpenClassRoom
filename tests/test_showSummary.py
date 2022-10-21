import pytest
import server
from server import ClubNotFound, get_club

def test_email_not_found():
    with pytest.raises(ClubNotFound):
        get_club('bad@email.com')

def test_good_email(clubs_fixture):
    club = get_club(clubs_fixture[0]['email'])
    assert club['name'] == 'Simply Lift'

def test_showSummary(client, monkeypatch, competitions_fixture):

    def mock_get_club(email):
        return {
            "name":"Simply Lift",
            "email":"john@simplylift.co",
            "points":"13"
        }
    
    monkeypatch.setattr(server, 'get_club', mock_get_club)
    monkeypatch.setattr(server, 'competitions', competitions_fixture)

    response = client.post('/showSummary', data={'email': 'john@simplylift.co'})
    data = response.data.decode()

    assert response.status_code == 200
    assert data.find('<h2>Welcome, john@simplylift.co <h2>')
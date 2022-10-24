import pytest
import server


def test_display_points_good_response(client, monkeypatch, clubs_fixture):

    monkeypatch.setattr(server, 'clubs', clubs_fixture)
    response = client.get('/displayPoints')
    data = response.data.decode()

    expected_result = f"Club name: {clubs_fixture[0]['name']}"

    assert response.status_code == 200
    assert data.find(expected_result) != -1
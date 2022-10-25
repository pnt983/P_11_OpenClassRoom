

def test_index_good_request(client):
    """
    When index is calling
    Then index is display
    """
    response = client.get('/')
    data = response.data.decode()

    assert response.status_code == 200
    assert data.find("Welcome to the GUDLFT Registration Portal!") != -1


def test_logout(client):
    """
    When logout is calling
    Then club is disconnected
    """
    response = client.get('/logout')
    data = response.data.decode()

    assert response.status_code == 302
    assert data.find("Redirecting") != -1
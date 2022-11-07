

def test_showSummary(client):
    """
    Given good email
    When showSummary is calling
    Then summary page display
    """
    response = client.post('/showSummary', data={'email': 'john@simplylift.co'})
    data = response.data.decode()

    assert response.status_code == 200
    assert data.find('Welcome, john@simplylift.co') != -1

def test_showSummary_bad_email(client):
    """
    Given bad email
    When showSummary is calling
    Then redirect index page display
    """
    response = client.post('/showSummary', data = {'email' : 'bad@email.com'})
    data = response.data.decode()

    assert response.status_code == 302
    assert data.find('Redirecting') != -1
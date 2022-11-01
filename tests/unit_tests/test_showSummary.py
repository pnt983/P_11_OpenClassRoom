import pytest
from server import ClubNotFound, get_club

def test_email_not_found():
    """
    Given bad email
    When get_club is calling
    Then raise ClubNotFound exeption
    """
    with pytest.raises(ClubNotFound):
        get_club('bad@email.com')

def test_good_email(clubs_fixture):
    """
    Given good email
    When get_club is calling
    Then return club
    """
    club = get_club(clubs_fixture[0]['email'])
    assert club['name'] == 'Simply Lift'
    
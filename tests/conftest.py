import pytest
from server import app as server_app


@pytest.fixture
def app():
    server_app.config.from_mapping({"TESTING": True})
    yield server_app

@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def clubs_fixture():
    return [
    {
        "name":"Simply Lift",
        "email":"john@simplylift.co",
        "points":"13"
    },
    {
        "name":"Iron Temple",
        "email": "admin@irontemple.com",
        "points":"4"
    },
    {   "name":"She Lifts",
        "email": "kate@shelifts.co.uk",
        "points":"12"
    }
]

@pytest.fixture
def competitions_fixture():
    return [
        {
            "name": "Spring Festival",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "25"
        },
        {
            "name": "Fall Classic",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "13"
        },
        {
            "name": "Competition Test Date",
            "date": "2023-10-22 13:30:00",
            "numberOfPlaces": "13"
        }
        ]
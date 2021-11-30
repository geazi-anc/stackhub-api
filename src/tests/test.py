import pytest
from pymongo import MongoClient
from fastapi.testclient import TestClient
from app import app


##### VARIABLES #####
api = TestClient(app)


##### CONFIG #####
def teardown_module():
    client = MongoClient("localhost:27017")
    db = client["test_stackhubdb"]

    MongoClient.drop_database(client, db)


##### FIXTURES #####
@pytest.fixture
def default_user_for_tests():
    user = {"first_name": "Jean", "last_name": "Grey",
            "email": "jeangrey@xavierinstitute.com", "password": "jeangrey1234"}
    return user


@pytest.fixture
def logged_user_by_email(default_user_for_tests):
    user = {"email": default_user_for_tests["email"],
            "password": default_user_for_tests["password"]}

    response = api.post("/login", data=user)
    body = response.json()

    return {"response": response, "body": body}


##### TESTS #####
def test_ping():
    response = api.get("ping")
    body = response.json()

    assert response.status_code == 200
    assert body == "PONG!"


def test_save_user(default_user_for_tests):
    response = api.post("/user", data=default_user_for_tests)
    body = response.json()

    assert response.status_code == 200
    assert body == "User has been succesfully created!"


def test_login_user_by_email(logged_user_by_email, default_user_for_tests):
    response = logged_user_by_email["response"]
    body = logged_user_by_email["body"]

    assert response.status_code == 200
    assert body["email"] == default_user_for_tests["email"]
    assert body["first_name"] == default_user_for_tests["first_name"]
    assert body["last_name"] == default_user_for_tests["last_name"]


def test_find_user_by_id(logged_user_by_email, default_user_for_tests):
    logged_user_response = logged_user_by_email["response"]
    logged_user_body = logged_user_by_email["body"]
    url = f"http://127.0.0.1:8000/user/{logged_user_body['_id']}"

    response = api.get(url)
    body = response.json()

    assert body["first_name"] == default_user_for_tests["first_name"]
    assert body["last_name"] == default_user_for_tests["last_name"]
    assert body["email"] == default_user_for_tests["email"]

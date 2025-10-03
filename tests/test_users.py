# tests/test_users.py
import pytest
def user_payload(uid=1, name="Paul", email="pl@atu.ie", age=25, sid="S1234567"):
    return {"user_id": uid, "name": name, "email": email, "age": age, "student_id": sid}

def test_create_user_ok(client):
    r = client.post("/api/users", json=user_payload())
    assert r.status_code == 201
    data = r.json()
    assert data["user_id"] == 1
    assert data["name"] == "Paul"

def test_duplicate_user_id_conflict(client):
    client.post("/api/users", json=user_payload(uid=2))
    r = client.post("/api/users", json=user_payload(uid=2))
    assert r.status_code == 409 # duplicate id -> conflict
    assert "exists" in r.json()["detail"].lower()


@pytest.mark.parametrize("bad_sid", ["BAD123", "s1234567", "S123", "S12345678"])
def test_bad_student_id_422(client, bad_sid):
    r = client.post("/api/users", json=user_payload(uid=3, sid=bad_sid))
    assert r.status_code == 422 # pydantic validation error

def test_get_user_404(client):
    r = client.get("/api/users/999")
    assert r.status_code == 404

def test_delete_then_404(client):
    client.post("/api/users", json=user_payload(uid=10))
    r1 = client.delete("/api/users/10")
    assert r1.status_code == 204
    r2 = client.delete("/api/users/10")
    assert r2.status_code == 404

#reflection
# 1. so whoever clones repo has all the same pip installs to run properly
# 2. says what needs to be tested rather than if a test has just been passed
# 3. validates error responses and negative paths, can tell if a user doesn't exist etc
# 4. shows that a workflow on a commit or branch has passed

def test_put_user_200(client): # had to change main.py, as the put method there, was expecting a 201 status code
    client.post("/api/users", json=user_payload(uid=10,name="original")) #creating a user with an id of 10 and then a name of original
    r1 = client.put("/api/users/10",json=user_payload(uid=10,name="updated")) #updating the user with id 10's name
    assert r1.status_code == 200
    data = r1.json()
    assert data["user_id"] == 10
    assert data["name"] == "updated" #checks if the stuff is the same as updated, fails if not


def test_put_user_404(client): # had to change main.py, as the put method there, was expecting a 409 user already exists
    r = client.put("/api/users/67", json=user_payload(uid=67, name="somebody"))
    assert r.status_code == 404



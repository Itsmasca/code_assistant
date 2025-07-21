import pytest
from fastapi.testclient import TestClient
from dotenv import load_dotenv
from src.api.api import app 
load_dotenv() 




client = TestClient(app)

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYmU4YTE4OTYtZTRlMS00N2RjLTkxM2UtZTM5ZWE0MGU1ODI3IiwiZXhwIjoxNzg0NjUzOTgxfQ.wk_sVAV-44BFvbnKfte4yqnzbNXOrzXvgD8DAXvnzng"
verified_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ2ZXJpZmljYXRpb25fY29kZSI6MTIzNDU2LCJleHAiOjE3ODQ2NTM4OTB9.FAEmnOWH8BjH5Z6xU7he7vHbAuiS8zAY4gnYFWePRYI"
delete_token= "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiOTEwMDA0YWUtY2IxYi00NjIzLTk4MDgtMTMxYWUzYjE4MmExIiwiZXhwIjoxNzgzNTQwMDkwfQ.P0olLSoCpnDlTFYk1VYMafes57hY2MvhG1eV8VfAGU4"

# def test_verify_email_success():
#     with TestClient(app) as client:
#         payload = {
#             "email": "brendan.soullens@gmail.com"
#         }

#         res = client.post("/users/verify-email",
#             json=payload
#         )

#         print("verify email response:::.", res.json())

#         assert res.status_code == 200
#         assert "token" in res.json()

def test_create_user_verified_success():
    with TestClient(app) as client:
        payload = {
            "email": "test1234555@example.com",
            "password": "password123",
            "code": "123456" 
        }

        res = client.post("/users/verified/create",
            headers={"Authorization": f"Bearer {verified_token}"},
            json=payload
        )
        assert res.status_code == 201
        assert res.json()["detail"] == "User created"


    
def test_create_user_verified_invalid_code():
    with TestClient(app) as client:
        payload = {
            "email": "user1234444@example.com",
            "password": "password123",
            "code": "123457" 
        }

        res = client.post("/users/verified/create",
            headers={"Authorization": f"Bearer {verified_token}"},
            json=payload
        )
        assert res.status_code == 403
        assert res.json()["detail"] == "Incorrect verification code"


def test_login_success():
   with TestClient(app) as client:

        payload = {
            "email": "test@example.com",
            "password": "password123"
        }

        res = client.post("/users/login", json=payload)
        print(res.json(), "LOGIN RESPONSE::::::::::")
        assert res.status_code == 200
        assert "token" in res.json()

        

def test_login_incorrect_password():
   with TestClient(app) as client:

        payload = {
            "email": "user333333@example.com",
            "password": "newpass456hhhhhhhhhhhh"
        }

        res = client.post("/users/login", json=payload)
        assert res.status_code == 400
        assert res.json()["detail"] == "Incorrect password"


def test_secure_resource():
    with TestClient(app) as client:
        res = client.get(
            "/users/secure/resource",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert res.status_code == 200
        assert "email" in res.json()


# def test_update_user_password():
#     with TestClient(app) as client:
#         payload = {
#             "oldPassword": "password123",
#             "newPassword": "newpass456"
#         }

#         res = client.put(
#             "/users/secure/update",
#             json=payload,
#             headers={"Authorization": f"Bearer {token}"}
#         )
#         assert res.status_code == 200
#         assert res.json()["message"] == "User updated"

def test_update_user_password_incorrect_password():
    with TestClient(app) as client:
        payload = {
            "oldPassword": "password123",
            "newPassword": "newpass456"
        }

        res = client.put(
            "/users/secure/update",
            json=payload,
            headers={"Authorization": f"Bearer {token}"}
        )
        assert res.status_code == 400
        assert res.json()["detail"] == "Incorrect password"

def test_update_user_password_missing_fields():
    with TestClient(app) as client:
        payload = {
            "newPassword": "newpass456"
        }

        res = client.put(
            "/users/secure/update",
            json=payload,
            headers={"Authorization": f"Bearer {token}"}
        )
        assert res.status_code == 422
        assert res.json()["detail"] == [{'input': {'newPassword': 'newpass456'}, 'loc': ['body', 'oldPassword'], 'msg': 'Field required', 'type': 'missing'}] 


# def test_delete_user():
#     with TestClient(app) as client:
#         res = client.delete(
#             "/users/secure/delete",
#             headers={"Authorization": f"Bearer {delete_token}"}
#         )
#         assert res.status_code == 200
#         assert res.json()["message"] == "User deleted"

import pytest
from fastapi.testclient import TestClient
from dotenv import load_dotenv
from src.api.api import app 
load_dotenv() 




client = TestClient(app)

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYmU4YTE4OTYtZTRlMS00N2RjLTkxM2UtZTM5ZWE0MGU1ODI3IiwiZXhwIjoxNzg0NjUzOTgxfQ.wk_sVAV-44BFvbnKfte4yqnzbNXOrzXvgD8DAXvnzng"
verified_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ2ZXJpZmljYXRpb25fY29kZSI6MTIzNDU2LCJleHAiOjE3ODQ2NTM4OTB9.FAEmnOWH8BjH5Z6xU7he7vHbAuiS8zAY4gnYFWePRYI"
delete_token= "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiOTEwMDA0YWUtY2IxYi00NjIzLTk4MDgtMTMxYWUzYjE4MmExIiwiZXhwIjoxNzgzNTQwMDkwfQ.P0olLSoCpnDlTFYk1VYMafes57hY2MvhG1eV8VfAGU4"




create_chat_payload = {
    "title": "Updated Agent Name"
}

def get_auth_headers():
    return {"Authorization": f"Bearer {token}"}


# def test_create_agent():
#     with TestClient(app) as client:
#         response = client.post(
#             "/chats/secure/create",
#             headers=get_auth_headers()
#         )

#         assert response.status_code == 201
#   
#       assert response.json() == {}



# def test_delete_agent():
#     with TestClient(app) as client:
#         response = client.delete(f"agents/secure/efbbc155-dfdc-45da-b166-8414d3e4b948", headers=get_auth_headers())
#         assert response.status_code == 200
#         assert response.json() == {"detail": "Agent deleted"}


def test_collection():
    with TestClient(app) as client:
        response = client.get("/chats/secure/collection", headers=get_auth_headers())
        
        print(response.json(), "RES::::")
        assert response.status_code == 200


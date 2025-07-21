import pytest
from fastapi.testclient import TestClient
from dotenv import load_dotenv
from src.api.api import app 
load_dotenv() 




client = TestClient(app)
agent_id = "15a66699-3dc8-4d0a-81c0-562931db40c0"

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYmU4YTE4OTYtZTRlMS00N2RjLTkxM2UtZTM5ZWE0MGU1ODI3IiwiZXhwIjoxNzg0NjUzOTgxfQ.wk_sVAV-44BFvbnKfte4yqnzbNXOrzXvgD8DAXvnzng"
verified_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ2ZXJpZmljYXRpb25fY29kZSI6MTIzNDU2LCJleHAiOjE3ODQ2NTM4OTB9.FAEmnOWH8BjH5Z6xU7he7vHbAuiS8zAY4gnYFWePRYI"
delete_token= "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiOTEwMDA0YWUtY2IxYi00NjIzLTk4MDgtMTMxYWUzYjE4MmExIiwiZXhwIjoxNzgzNTQwMDkwfQ.P0olLSoCpnDlTFYk1VYMafes57hY2MvhG1eV8VfAGU4"

# Sample agent data for creation
agent_create_payload = {
    "agentName": "Test Agent",
    "agentDescription": "A test agent",
    "agentPrompt": "Tell funy jokes about according to users input",
    "agentJson": {
        "max_tokens":  4000,
        "model": "gpt-40"
    }
}

# Sample agent update data
agent_update_payload = {
    "agentName": "Updated Agent Name",
    "agentPrompt": "generate code"
}

def get_auth_headers():
    return {"Authorization": f"Bearer {token}"}


# def test_create_agent():
#     with TestClient(app) as client:
#         response = client.post(
#             "/agents/secure/create",
#             json=agent_create_payload,
#             headers=get_auth_headers()
#         )

#         assert response.status_code == 201
#         assert response.json() == {"detail": "Agent created"}

def test_get_agents_collection():
    with TestClient(app) as client:
        response = client.get("/agents/secure/collection", headers=get_auth_headers())
        assert response.status_code == 200
        
     
      


def test_get_agent_resource():
    with TestClient(app) as client:
        response = client.get(f"/agents/secure/resource/{agent_id}", headers=get_auth_headers())
        data = response.json()
    
        assert response.status_code == 200
        assert data["agentId"] == agent_id


def test_update_agent():
    with TestClient(app) as client:
        response = client.put(
            f"/agents/secure/{agent_id}",
            json=agent_update_payload,
            headers=get_auth_headers()
        )

        print("UPDATE::::::::", response.json())
        assert response.status_code == 200
    
        assert response.json()["detail"] == "Agent updated"


# def test_delete_agent():
#     with TestClient(app) as client:
#         response = client.delete(f"agents/secure/efbbc155-dfdc-45da-b166-8414d3e4b948", headers=get_auth_headers())
#         assert response.status_code == 200
#         assert response.json() == {"detail": "Agent deleted"}


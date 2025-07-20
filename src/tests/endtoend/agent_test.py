
import pytest
from src.agent.agent import app

class DummyCodeSolution:
    imports = "a = 1"
    code = "b = a + 1"
    prefix = "Test"

def dummy_chain_invoke(*args, **kwargs):
    return DummyCodeSolution()

@pytest.fixture
def initial_state():
    agent_json = {
      "openapi": "3.0.3",
      "info": {
        "version": "1.6.85",
        "title": "ConfigRouteAnalyzer",
        "description": "NeuralSeek - The business LLM accelerator",
        "license": {
          "name": "End User License Agreement",
          "url": "https://neuralseek.com/eula"
        },
        "contact": {
          "name": "NeuralSeek Support",
          "url": "https://neuralseek.com",
          "email": "support@NeuralSeek.com"
        },
        "termsOfService": "https://neuralseek.com/eula"
      },
      "servers": [
        {
          "url": "https://stagingapi.neuralseek.com/v1/{instance}",
          "description": "NeuralSeek API server",
          "variables": {
            "instance": {
              "default": "Liam-demo",
              "description": "Your instance ID"
            }
          }
        }
      ],
      "paths": {
        "/maistro": {
          "post": {
            "tags": ["maistro"],
            "summary": "Run mAistro NTL or agent",
            "description": "Freeform prompting using NeuralSeek Template Language or a saved agent",
            "operationId": "maistro",
            "parameters": [],
            "requestBody": {},
            "responses": {}
          }
        }
      }
    }
    return {
        "messages": [],
        "iterations": 0,
        "error": "no",
        "agentName": "testkike",
        "improvedPrompt": "Configure a test scenario with routing disabled and strict mode turned off. Provide details on the configuration settings and potential implications of these adjustments.",
        "agentJson": agent_json,
        "generation": DummyCodeSolution(),
        "ntlObject": "ntl",
        "fullResponse": "data"
    }

def test_workflow_e2e(monkeypatch, initial_state):
    # Mock Llmservice.retrieve_chain
    from src.service import Llm_service
    monkeypatch.setattr(Llm_service.Llmservice, "retrieve_chain", lambda self, prompt=None: type("DummyChain", (), {"invoke": dummy_chain_invoke})())
    from src.service import Qdrant
    monkeypatch.setattr(Qdrant.QdrantRetriever, "retrieve", lambda self, query, limit=10: "contexto de prueba")

    result = app.invoke(initial_state)
    print("Respuesta del workflow:", result)

    # Validaciones típicas
    assert "generation" in result
    assert "messages" in result
    assert "iterations" in result
    assert result["error"] in ["no", "yes"]
    # Ejemplo: verifica que el código generado está en la respuesta
    assert hasattr(result["generation"], "code")
    assert hasattr(result["generation"], "imports")
    assert hasattr(result["generation"], "prefix")
    result = app.invoke(initial_state)
    # Verifica que el resultado final tiene los campos esperados
    assert "generation" in result
    assert "messages" in result
    assert "iterations" in result
    assert result["error"] in ["no", "yes"]

    print("Código generado:", result["generation"].code)
    print("Imports:", result["generation"].imports)
    print("Prefix:", result["generation"].prefix)
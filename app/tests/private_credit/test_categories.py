import pytest


def test_list_categories_empty(client):
    response = client.get("/private-credit/categories")
    assert response.status_code == 200
    assert response.json() == []


def test_create_category_success(client):
    payload = {
        "name": "Renda Fixa",
        "description": "Categoria de renda fixa",
        "allocation_planned": 60,
        "currency": "BRL",
        "active": True,
        "module": "private_credit"
    }
    response = client.post("/private-credit/categories", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["allocation_planned"] == payload["allocation_planned"]


def test_create_category_duplicate(client):
    payload = {
        "name": "Duplicada",
        "description": "Primeira vez",
        "allocation_planned": 30,
        "currency": "BRL",
        "active": True,
        "module": "private_credit"
    }
    first = client.post("/private-credit/categories", json=payload)
    assert first.status_code == 201

    second = client.post("/private-credit/categories", json=payload)
    assert second.status_code in (400, 409)


def test_update_category_success(client):
    payload = {
        "name": "Atualizar",
        "description": "Categoria para atualizar",
        "allocation_planned": 10,
        "currency": "BRL",
        "active": True,
        "module": "private_credit"
    }
    create = client.post("/private-credit/categories", json=payload)
    assert create.status_code == 201
    category_id = create.json()["id"]

    update_payload = {"description": "Nova descrição"}
    update = client.patch(f"/private-credit/categories/{category_id}", json=update_payload)
    assert update.status_code == 200
    assert update.json()["description"] == "Nova descrição"


def test_delete_category_success(client):
    payload = {
        "name": "Excluir",
        "description": "Categoria para excluir",
        "allocation_planned": 15,
        "currency": "BRL",
        "active": True,
        "module": "private_credit"
    }
    create = client.post("/private-credit/categories", json=payload)
    assert create.status_code == 201
    category_id = create.json()["id"]

    delete = client.delete(f"/private-credit/categories/{category_id}")
    assert delete.status_code == 204

    get = client.get(f"/private-credit/categories/{category_id}")
    assert get.status_code == 404


@pytest.mark.parametrize(
    "invalid_payload",
    [
        {"name": "", "allocation_planned": 50, "currency": "BRL", "module": "private_credit"},
        {"name": "SemModulo", "allocation_planned": 50, "currency": "BRL", "module": None},
        {"name": "SemAlocacao", "allocation_planned": -5, "currency": "BRL", "module": "private_credit"}
    ],
)
def test_create_category_invalid(client, invalid_payload):
    response = client.post("/private-credit/categories", json=invalid_payload)
    assert response.status_code in (400, 422)


def test_list_categories_after_inserts(client):
    # garantir lista populada
    payload = {
        "name": "Lista Teste",
        "description": "Categoria para lista",
        "allocation_planned": 20,
        "currency": "BRL",
        "active": True,
        "module": "private_credit"
    }
    client.post("/private-credit/categories", json=payload)
    response = client.get("/private-credit/categories")
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_category_stress_insert(client):
    """
    Insere 100 categorias seguidas para stress.
    """
    for i in range(100):
        payload = {
            "name": f"Stress {i}",
            "description": "Categoria stress",
            "allocation_planned": 1 + i % 100,
            "currency": "BRL",
            "active": True,
            "module": "private_credit"
        }
        response = client.post("/private-credit/categories", json=payload)
        assert response.status_code == 201

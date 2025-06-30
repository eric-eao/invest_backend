def test_list_categories_empty(client):
    response = client.get("/categories")
    assert response.status_code == 200
    assert response.json() == []


def test_create_category_success(client):
    payload = {
        "name": "Renda Fixa",
        "description": "Categoria de renda fixa privada",
        "allocation_planned": 50,
        "currency": "BRL",
        "active": True,
        "module": "private_credit"
    }
    response = client.post("/categories", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["currency"] == payload["currency"]
    assert data["allocation_planned"] == payload["allocation_planned"]


def test_create_category_duplicate(client):
    payload = {
        "name": "Duplicada",
        "description": "Teste duplicidade",
        "allocation_planned": 30,
        "currency": "BRL",
        "active": True,
        "module": "private_credit"
    }
    response1 = client.post("/categories", json=payload)
    assert response1.status_code == 201

    response2 = client.post("/categories", json=payload)
    assert response2.status_code in (400, 409)
    assert "Categoria já existe" in response2.text or "duplicate" in response2.text.lower()


def test_update_category_success(client):
    # cria primeiro
    payload = {
        "name": "ParaAtualizar",
        "description": "Categoria para atualizar",
        "allocation_planned": 20,
        "currency": "BRL",
        "active": True,
        "module": "private_credit"
    }
    create_response = client.post("/categories", json=payload)
    assert create_response.status_code == 201
    category_id = create_response.json()["id"]

    # atualiza
    updates = {
        "name": "Atualizada",
        "allocation_planned": 40,
        "currency": "BRL",
        "active": True,
        "module": "private_credit"
    }
    update_response = client.patch(f"/categories/{category_id}", json=updates)
    print(update_response.json())
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["name"] == "Atualizada"
    assert data["allocation_planned"] == 40


def test_delete_category_success(client):
    # cria primeiro
    payload = {
        "name": "ParaDeletar",
        "description": "Categoria para deletar",
        "allocation_planned": 15,
        "currency": "BRL",
        "active": True,
        "module": "private_credit"
    }
    create_response = client.post("/categories", json=payload)
    assert create_response.status_code == 201
    category_id = create_response.json()["id"]

    # deleta
    delete_response = client.delete(f"/categories/{category_id}")
    assert delete_response.status_code == 204

    # tenta buscar e não deve existir
    get_response = client.get(f"/categories/{category_id}")
    assert get_response.status_code == 404

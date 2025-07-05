import pytest


def test_list_assets_empty(client):
    response = client.get("/private-credit/assets")
    assert response.status_code == 200
    assert response.json() == []


def test_create_asset_success(client):
    # primeiro cria uma categoria
    category_payload = {
        "name": "Renda Fixa Asset",
        "description": "Categoria para asset",
        "allocation_planned": 50,
        "currency": "BRL",
        "active": True,
        "module": "private_credit"
    }
    category_response = client.post("/private-credit/categories", json=category_payload)
    assert category_response.status_code == 201
    category_id = category_response.json()["id"]

    asset_payload = {
        "description": "CDB XPTO",
        "code": "CDB123",
        "institution": "Banco XPTO",
        "category_id": category_id,
        "maturity_date": "2027-12-31",
        "rate_type": "POS-FIXADO",
        "indexer": "CDI",
        "fixed_rate": None,
        "spread": 1.5,
        "index_percent": 100,
        "active": True
    }
    response = client.post("/private-credit/assets", json=asset_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["description"] == asset_payload["description"]
    assert data["category_id"] == category_id


def test_create_asset_duplicate_code(client):
    # categoria
    category_payload = {
        "name": "Renda Fixa Dup",
        "description": "Categoria para asset duplicado",
        "allocation_planned": 30,
        "currency": "BRL",
        "active": True,
        "module": "private_credit"
    }
    category_response = client.post("/private-credit/categories", json=category_payload)
    category_id = category_response.json()["id"]

    asset_payload = {
        "description": "CDB DUP",
        "code": "DUP123",
        "institution": "Banco DUP",
        "category_id": category_id,
        "maturity_date": "2027-12-31",
        "rate_type": "POS-FIXADO",
        "indexer": "CDI",
        "fixed_rate": None,
        "spread": 1.0,
        "index_percent": 100,
        "active": True
    }
    first = client.post("/private-credit/assets", json=asset_payload)
    assert first.status_code == 201
    second = client.post("/private-credit/assets", json=asset_payload)
    assert second.status_code in (400, 409)


def test_update_asset_success(client):
    # categoria
    category_payload = {
        "name": "Renda Fixa Atualizar",
        "description": "Categoria update asset",
        "allocation_planned": 40,
        "currency": "BRL",
        "active": True,
        "module": "private_credit"
    }
    category = client.post("/private-credit/categories", json=category_payload)
    category_id = category.json()["id"]

    asset_payload = {
        "description": "CDB Atualizar",
        "code": "UPD123",
        "institution": "Banco UPD",
        "category_id": category_id,
        "maturity_date": "2028-12-31",
        "rate_type": "POS-FIXADO",
        "indexer": "CDI",
        "fixed_rate": None,
        "spread": 2.0,
        "index_percent": 100,
        "active": True
    }
    asset = client.post("/private-credit/assets", json=asset_payload)
    asset_id = asset.json()["id"]

    update_payload = {"description": "CDB Atualizado", "rate_type": "POS-FIXADO"}
    response = client.patch(f"/private-credit/assets/{asset_id}", json=update_payload)
    print(">>>> status code", response.status_code)
    print(">>>> response.text", response.text)
    assert response.status_code == 200
    assert response.json()["description"] == "CDB Atualizado"


def test_delete_asset_success(client):
    # categoria
    category_payload = {
        "name": "Renda Fixa Delete",
        "description": "Categoria delete asset",
        "allocation_planned": 20,
        "currency": "BRL",
        "active": True,
        "module": "private_credit"
    }
    category = client.post("/private-credit/categories", json=category_payload)
    category_id = category.json()["id"]

    asset_payload = {
        "description": "CDB Delete",
        "code": "DEL123",
        "institution": "Banco DEL",
        "category_id": category_id,
        "maturity_date": "2029-12-31",
        "rate_type": "POS-FIXADO",
        "indexer": "CDI",
        "fixed_rate": None,
        "spread": 2.5,
        "index_percent": 100,
        "active": True
    }
    asset = client.post("/private-credit/assets", json=asset_payload)
    asset_id = asset.json()["id"]

    delete = client.delete(f"/private-credit/assets/{asset_id}")
    assert delete.status_code == 204

    get = client.get(f"/private-credit/assets/{asset_id}")
    assert get.status_code == 404


@pytest.mark.parametrize(
    "invalid_payload",
    [
        {"description": "", "code": "X", "institution": "Banco", "category_id": None, "rate_type": "POS-FIXADO", "indexer": "CDI", "index_percent": 100, "active": True},
        {"description": "SemCategoria", "code": "Y", "institution": "Banco", "category_id": None, "rate_type": "POS-FIXADO", "indexer": "CDI", "index_percent": 100, "active": True}
    ]
)
def test_create_asset_invalid(client, invalid_payload):
    response = client.post("/private-credit/assets", json=invalid_payload)
    assert response.status_code in (400, 422)


def test_list_assets_after_inserts(client):
    # cria categoria
    category_payload = {
        "name": "Renda Fixa Lista",
        "description": "Categoria lista asset",
        "allocation_planned": 10,
        "currency": "BRL",
        "active": True,
        "module": "private_credit"
    }
    category = client.post("/private-credit/categories", json=category_payload)
    category_id = category.json()["id"]

    asset_payload = {
        "description": "CDB Lista",
        "code": "LST123",
        "institution": "Banco Lista",
        "category_id": category_id,
        "maturity_date": "2030-12-31",
        "rate_type": "POS-FIXADO",
        "indexer": "CDI",
        "fixed_rate": None,
        "spread": 1.5,
        "index_percent": 100,
        "active": True
    }
    client.post("/private-credit/assets", json=asset_payload)
    response = client.get("/private-credit/assets")
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_asset_stress_insert(client):
    """
    Insere 100 assets para stress.
    """
    # cria categoria
    category_payload = {
        "name": "Renda Fixa Stress",
        "description": "Categoria stress asset",
        "allocation_planned": 20,
        "currency": "BRL",
        "active": True,
        "module": "private_credit"
    }
    category = client.post("/private-credit/categories", json=category_payload)
    category_id = category.json()["id"]

    for i in range(100):
        payload = {
            "description": f"CDB Stress {i}",
            "code": f"STR{i}",
            "institution": "Banco Stress",
            "category_id": category_id,
            "maturity_date": "2031-12-31",
            "rate_type": "POS-FIXADO",
            "indexer": "CDI",
            "fixed_rate": None,
            "spread": 1.0,
            "index_percent": 100,
            "active": True
        }
        response = client.post("/private-credit/assets", json=payload)
        assert response.status_code == 201

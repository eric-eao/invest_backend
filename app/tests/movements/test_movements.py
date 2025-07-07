from sqlalchemy import text

def test_create_movement_syncs_portfolio_dates(client, db_session):
    # cria category
    cat_payload = {
        "name": "MovCat",
        "description": "Categoria movimentos",
        "allocation_planned": 50,
        "currency": "BRL",
        "active": True,
        "module": "private_credit"
    }
    cat_resp = client.post("/private-credit/categories", json=cat_payload)
    category_id = cat_resp.json()["id"]

    # cria module
    mod_payload = {
        "name": "MovMod",
        "description": "Módulo movimentos",
        "active": True,
        "sync_status": "pending"
    }
    mod_resp = client.post("/admin/modules", json=mod_payload)
    module_id = mod_resp.json()["id"]

    # cria asset
    asset_payload = {
        "description": "CDB Teste",
        "code": "CDBMOV",
        "institution": "Banco Teste",
        "category_id": category_id,
        "maturity_date": "2028-12-31",
        "rate_type": "POS-FIXADO",
        "indexer": "CDI",
        "fixed_rate": None,
        "spread": 1.2,
        "index_percent": 100,
        "active": True
    }
    asset_resp = client.post("/private-credit/assets", json=asset_payload)
    asset_id = asset_resp.json()["id"]

    # cria movement
    mov_payload = {
        "asset_id": asset_id,
        "module_id": module_id,
        "movement_type": "DEPOSIT",
        "quantity": 100,
        "unit_price": 1,
        "movement_date": "2024-07-01",
        "settlement_date": "2024-07-02",
        "broker": "XP",
        "transaction_reference": "MOV001",
        "status": "PENDING",
        "notes": "primeiro aporte",
        "source": "manual"
    }
    mov_resp = client.post("/movements", json=mov_payload)
    assert mov_resp.status_code == 201

    result = db_session.execute(
        text("SELECT first_investment FROM control_portfolio_dates WHERE module_id = :module_id"),
        {"module_id": module_id}
    ).fetchone()
    assert result is not None
    assert str(result.first_investment) == "2024-07-01"


def test_update_movement_syncs_portfolio_dates(client, db_session):
    # prepara category
    cat_payload = {
        "name": "MovCatUpdate",
        "description": "Cat mov update",
        "allocation_planned": 50,
        "currency": "BRL",
        "active": True,
        "module": "private_credit"
    }
    cat_resp = client.post("/private-credit/categories", json=cat_payload)
    category_id = cat_resp.json()["id"]

    # prepara module
    mod_payload = {
        "name": "MovModUpdate",
        "description": "Mod mov update",
        "active": True,
        "sync_status": "pending"
    }
    mod_resp = client.post("/admin/modules", json=mod_payload)
    module_id = mod_resp.json()["id"]

    # prepara asset
    asset_payload = {
        "description": "CDB Update",
        "code": "CDBUPD",
        "institution": "Banco Update",
        "category_id": category_id,
        "maturity_date": "2028-12-31",
        "rate_type": "POS-FIXADO",
        "indexer": "CDI",
        "fixed_rate": None,
        "spread": 1.5,
        "index_percent": 100,
        "active": True
    }
    asset_resp = client.post("/private-credit/assets", json=asset_payload)
    asset_id = asset_resp.json()["id"]

    # cria movement
    mov_payload = {
        "asset_id": asset_id,
        "module_id": module_id,
        "movement_type": "DEPOSIT",
        "quantity": 100,
        "unit_price": 1,
        "movement_date": "2024-07-01",
        "settlement_date": "2024-07-02",
        "broker": "BTG",
        "transaction_reference": "UPD001",
        "status": "PENDING",
        "notes": "update test",
        "source": "manual"
    }
    mov_resp = client.post("/movements", json=mov_payload)
    movement_id = mov_resp.json()["id"]

    # atualiza
    upd_payload = {
        "quantity": 200
    }
    upd_resp = client.put(f"/movements/{movement_id}", json=upd_payload)
    assert upd_resp.status_code == 200

    result = db_session.execute(
        text("SELECT last_investment FROM control_portfolio_dates WHERE module_id = :module_id"),
        {"module_id": module_id}
    ).fetchone()
    assert result is not None
    assert result.last_investment is not None


def test_delete_movement_syncs_portfolio_dates(client, db_session):
    # category
    cat_payload = {
        "name": "MovCatDelete",
        "description": "Cat mov delete",
        "allocation_planned": 50,
        "currency": "BRL",
        "active": True,
        "module": "private_credit"
    }
    cat_resp = client.post("/private-credit/categories", json=cat_payload)
    category_id = cat_resp.json()["id"]

    # module
    mod_payload = {
        "name": "MovModDelete",
        "description": "Mod mov delete",
        "active": True,
        "sync_status": "pending"
    }
    mod_resp = client.post("/admin/modules", json=mod_payload)
    module_id = mod_resp.json()["id"]

    # asset
    asset_payload = {
        "description": "CDB Delete",
        "code": "CDBDEL",
        "institution": "Banco Delete",
        "category_id": category_id,
        "maturity_date": "2029-12-31",
        "rate_type": "POS-FIXADO",
        "indexer": "CDI",
        "fixed_rate": None,
        "spread": 2.0,
        "index_percent": 100,
        "active": True
    }
    asset_resp = client.post("/private-credit/assets", json=asset_payload)
    asset_id = asset_resp.json()["id"]

    # movimento
    mov_payload = {
        "asset_id": asset_id,
        "module_id": module_id,
        "movement_type": "DEPOSIT",
        "quantity": 100,
        "unit_price": 1,
        "movement_date": "2024-07-01",
        "settlement_date": "2024-07-02",
        "broker": "Clear",
        "transaction_reference": "DEL001",
        "status": "PENDING",
        "notes": "delete test",
        "source": "manual"
    }
    mov_resp = client.post("/movements", json=mov_payload)
    movement_id = mov_resp.json()["id"]

    # delete
    del_resp = client.delete(f"/movements/{movement_id}")
    assert del_resp.status_code == 204

    result = db_session.execute(
        text("SELECT last_investment FROM control_portfolio_dates WHERE module_id = :module_id"),
        {"module_id": module_id}
    ).fetchone()
    assert result.last_investment is None

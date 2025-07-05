from sqlalchemy import text


def test_list_modules_empty(client):
    response = client.get("/admin/modules")
    assert response.status_code == 200
    assert response.json() == []


def test_create_module_creates_portfolio_date(client, db_session):
    payload = {
        "name": "Private Credit",
        "description": "Módulo Private Credit",
        "active": True,
        "sync_status": "pending"
    }
    response = client.post("/admin/modules", json=payload)
    assert response.status_code == 201
    module_id = response.json()["id"]

    result = db_session.execute(
        text("SELECT * FROM control_portfolio_dates WHERE module_id = :module_id"),
        {"module_id": module_id}
    ).fetchone()
    assert result is not None


def test_update_module_updates_portfolio_date(client, db_session):
    payload = {
        "name": "UpdateTest",
        "description": "Testando update",
        "active": True,
        "sync_status": "pending"
    }
    create = client.post("/admin/modules", json=payload)
    module_id = create.json()["id"]

    update = {"active": False}
    response = client.put(f"/admin/modules/{module_id}", json=update)
    assert response.status_code == 200

    result = db_session.execute(
        text("SELECT * FROM control_portfolio_dates WHERE module_id = :module_id"),
        {"module_id": module_id}
    ).mappings().fetchone()
    assert result["active"] is False


def test_delete_module_deletes_portfolio_date(client, db_session):
    payload = {
        "name": "DeleteTest",
        "description": "Testando delete",
        "active": True,
        "sync_status": "pending"
    }
    create = client.post("/admin/modules", json=payload)
    module_id = create.json()["id"]

    delete = client.delete(f"/admin/modules/{module_id}")
    assert delete.status_code == 204

    result = db_session.execute(
        text("SELECT * FROM control_portfolio_dates WHERE module_id = :module_id"),
        {"module_id": module_id}
    ).fetchone()
    assert result is None

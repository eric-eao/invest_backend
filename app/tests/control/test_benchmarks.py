import pytest


def test_create_benchmark_success(client):
    payload = {
        "name": "CDI",
        "description": "Benchmark CDI",
        "active": True
    }
    response = client.post("/admin/benchmarks", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == payload["name"]

def test_create_benchmark_duplicate(client):
    payload = {
        "name": "IPCA",
        "description": "Benchmark IPCA",
        "active": True
    }
    first = client.post("/admin/benchmarks", json=payload)
    assert first.status_code == 201
    second = client.post("/admin/benchmarks", json=payload)
    assert second.status_code in (400, 409)

@pytest.mark.parametrize(
    "payload,missing_field",
    [
        (
            {
                "description": "Benchmark sem nome",
                "active": True
            },
            "name",
        ),
    ],
)
def test_create_benchmark_missing_fields(client, payload, missing_field):
    response = client.post("/admin/benchmarks", json=payload)
    assert response.status_code == 422
    assert missing_field in response.text


def test_list_benchmarks_empty(client):
    response = client.get("/admin/benchmarks")
    assert response.status_code == 200
    assert response.json() == []

def test_list_benchmarks_after_inserts(client):
    payload = {
        "name": "IGP-M",
        "description": "Benchmark IGP-M",
        "active": True
    }
    client.post("/admin/benchmarks", json=payload)
    response = client.get("/admin/benchmarks")
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_update_benchmark_success(client):
    payload = {
        "name": "SELIC",
        "description": "Benchmark SELIC",
        "active": True
    }
    created = client.post("/admin/benchmarks", json=payload)
    benchmark_id = created.json()["id"]

    update = {"description": "Benchmark SELIC atualizado"}
    response = client.put(f"/admin/benchmarks/{benchmark_id}", json=update)
    assert response.status_code == 200
    assert response.json()["description"] == update["description"]


def test_delete_benchmark_success(client):
    payload = {
        "name": "PRE",
        "description": "Benchmark Pré",
        "active": True
    }
    created = client.post("/admin/benchmarks", json=payload)
    benchmark_id = created.json()["id"]

    delete = client.delete(f"/admin/benchmarks/{benchmark_id}")
    assert delete.status_code == 204

    get = client.get(f"/admin/benchmarks/{benchmark_id}")
    assert get.status_code == 404

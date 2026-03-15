import random
import pytest
import requests
from config.config import PETSTORE_BASE_URL


def _unique_id():
    return random.randint(100_000, 999_999)


def _build_pet(pet_id, name="Buddy", status="available"):
    return {
        "id": pet_id,
        "category": {"id": 1, "name": "dog"},
        "name": name,
        "photoUrls": ["https://example.com/photo.jpg"],
        "tags": [{"id": 1, "name": "friendly"}],
        "status": status,
    }


# ── Positive Tests ──


@pytest.mark.api
def test_create_pet(base_url):
    pet_id = _unique_id()
    payload = _build_pet(pet_id)

    try:
        resp = requests.post(f"{base_url}/pet", json=payload)
        assert resp.status_code == 200, f"Expected 200 but got {resp.status_code}"
        body = resp.json()
        assert body["name"] == payload["name"]
        assert body["status"] == payload["status"]
        assert body["id"] == pet_id
    finally:
        requests.delete(f"{base_url}/pet/{pet_id}")


@pytest.mark.api
def test_get_pet_by_id(base_url):
    pet_id = _unique_id()
    requests.post(f"{base_url}/pet", json=_build_pet(pet_id, name="Shadow"))

    try:
        resp = requests.get(f"{base_url}/pet/{pet_id}")
        assert resp.status_code == 200
        body = resp.json()
        assert body["id"] == pet_id
        assert body["name"] == "Shadow"
    finally:
        requests.delete(f"{base_url}/pet/{pet_id}")


@pytest.mark.api
def test_update_pet(base_url):
    pet_id = _unique_id()
    payload = _build_pet(pet_id, name="OldName", status="available")
    requests.post(f"{base_url}/pet", json=payload)

    try:
        payload["name"] = "NewName"
        payload["status"] = "sold"
        resp = requests.put(f"{base_url}/pet", json=payload)

        assert resp.status_code == 200
        body = resp.json()
        assert body["name"] == "NewName"
        assert body["status"] == "sold"
    finally:
        requests.delete(f"{base_url}/pet/{pet_id}")


@pytest.mark.api
def test_find_pets_by_status(base_url):
    resp = requests.get(f"{base_url}/pet/findByStatus", params={"status": "available"})

    assert resp.status_code == 200
    body = resp.json()
    assert isinstance(body, list), "Response should be a list"
    assert len(body) > 0, "Should find at least one available pet"


@pytest.mark.api
def test_delete_pet(base_url):
    pet_id = _unique_id()
    requests.post(f"{base_url}/pet", json=_build_pet(pet_id))

    resp = requests.delete(f"{base_url}/pet/{pet_id}")
    assert resp.status_code == 200


@pytest.mark.api
def test_verify_deleted_pet(base_url):
    pet_id = _unique_id()
    requests.post(f"{base_url}/pet", json=_build_pet(pet_id))
    requests.delete(f"{base_url}/pet/{pet_id}")

    resp = requests.get(f"{base_url}/pet/{pet_id}")
    assert resp.status_code == 404, f"Deleted pet should return 404, got {resp.status_code}"


# ── Negative Tests ──


@pytest.mark.api
def test_get_pet_invalid_id(base_url):
    resp = requests.get(f"{base_url}/pet/99999999999")
    assert resp.status_code == 404


@pytest.mark.api
def test_create_pet_with_invalid_body(base_url):
    resp = requests.post(
        f"{base_url}/pet",
        data="this is not json",
        headers={"Content-Type": "application/json"},
    )
    # petstore may return 400, 405, or 500 for malformed JSON
    assert resp.status_code in (400, 405, 500), f"Expected error status, got {resp.status_code}"


@pytest.mark.api
def test_delete_nonexistent_pet(base_url):
    resp = requests.delete(f"{base_url}/pet/99999999999")
    assert resp.status_code in (200, 404)


@pytest.mark.api
def test_find_pets_invalid_status(base_url):
    resp = requests.get(f"{base_url}/pet/findByStatus", params={"status": "nonexistent"})
    assert resp.status_code in (200, 400)
    if resp.status_code == 200:
        assert isinstance(resp.json(), list)


@pytest.mark.api
def test_get_pet_with_string_id(base_url):
    resp = requests.get(f"{base_url}/pet/invalidid")
    assert resp.status_code in (400, 404)

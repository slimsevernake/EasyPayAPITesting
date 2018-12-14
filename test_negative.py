import pytest
import requests

from conftest import headers
from src.params import not_a_date, address_id, user_id, past_date, inspector_id
from src.url import schedule_url, update_role_url, delete_inspector_url


def test_create_visit_invalid_date(login_as_manager):
    cookies = login_as_manager
    payload = {"address": {"id": address_id},
               "eventDate": not_a_date, "repeat": "true"}
    response = requests.post(schedule_url, json=payload,
                             headers=headers, cookies=cookies)
    assert response.status_code == 400


def test_create_visit_in_past(login_as_manager):
    cookies = login_as_manager
    payload = {"address": {"id": address_id},
               "eventDate": past_date, "repeat": "true"}
    response = requests.post(schedule_url, json=payload,
                             headers=headers, cookies=cookies)
    assert response.status_code == 400


@pytest.mark.parametrize('role', ("admin", "INSP", "#&"))
def test_update_role(login_as_admin, role):
    cookies = login_as_admin
    payload = {"id": user_id, "role": role, "status": "ACTIVE"}
    response = requests.put(update_role_url, json=payload,
                            headers=headers, cookies=cookies)
    assert response.status_code == 400


def test_remove_wrong_id_inspector(login_as_manager):
    cookies = login_as_manager
    payload = 'inspector'
    response = requests.delete(delete_inspector_url, json=payload,
                               headers=headers, cookies=cookies)
    assert response.status_code == 400


def test_remove_inspector_as_admin(login_as_admin):
    cookies = login_as_admin
    payload = inspector_id
    response = requests.delete(delete_inspector_url, json=payload,
                               headers=headers, cookies=cookies)
    assert response.status_code == 405

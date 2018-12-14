import pytest
import requests

from conftest import headers
from src.db_conn import no_inspector, get_current_count_of_visits, check
from src.params import visit_date, address_id, user_id, inspector_id
from src.url import schedule_url, update_role_url, delete_inspector_url


def test_create_visit(login_as_manager):
    token = login_as_manager
    prev_count = get_current_count_of_visits(visit_date)
    payload = {"address": {"id": address_id},
               "eventDate": visit_date, "repeat": "true"}
    response = requests.post(schedule_url, json=payload,
                             headers=headers, cookies=token)
    assert response.status_code == 201
    new_count = get_current_count_of_visits(visit_date)
    assert new_count - prev_count == 1


@pytest.mark.parametrize('role', ("ADMIN", "INSPECTOR", "USER", "MANAGER"))
def test_update_role(login_as_admin, role):
    token = login_as_admin
    payload = {"id": user_id, "role": role, "status": "ACTIVE"}
    response = requests.put(update_role_url, json=payload,
                            headers=headers, cookies=token)
    assert response.status_code == 200
    assert check(role)


def test_remove_inspector(login_as_manager):
    token = login_as_manager
    payload = inspector_id
    response = requests.delete(delete_inspector_url, json=payload,
                               headers=headers, cookies=token)
    assert response.status_code == 200
    assert no_inspector()

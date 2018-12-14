import pytest
import requests
from src.credentials import manager_email, manager_password, admin_email, \
    admin_password
from src.db_conn import DBConnection
from src.params import user_id
from src.url import authorization_url, update_role_url

headers = {
    'Content-Type': "application/json"
}


@pytest.fixture(scope="function")
def login_as_manager():
    with DBConnection() as db:
        db.add_inspector()
    payload = {"email": manager_email, "password": manager_password}
    response = requests.post(authorization_url, json=payload,
                             headers=headers)
    return response.cookies


@pytest.fixture(scope="function")
def login_as_admin(request):
    payload = {"email": admin_email, "password": admin_password}
    response = requests.post(authorization_url, json=payload,
                             headers=headers)

    def get_role_back():
        payload = {"id": user_id, "role": "INSPECTOR", "status": "ACTIVE"}
        requests.put(update_role_url, json=payload,
                     headers=headers, cookies=response.cookies)
    request.addfinalizer(get_role_back)
    return response.cookies

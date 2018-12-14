from src.params import inspector_id
base_url = "http://localhost:8080"
authorization_url = base_url + "/authorization"
update_role_url = base_url + "/admin/users/update"
schedule_url = "%s/manager/schedule/item/inspector/%s" % \
               (base_url, inspector_id)
delete_inspector_url = base_url + "/manager/schedule/deleteInspector"

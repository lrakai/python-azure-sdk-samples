
# fabricvalidator app registration
SP_ID = 'dc5a0040-341f-40c3-bb62-1cb719c70c14'
SP_SECRET = '...'


def with_hint(result, hint=None):
    return {'result': result, 'hint_message': hint} if hint else result

def get_token_with_password(tenant, username, password):
    """Obtain authentication token using a username/password with MS Identity Platform Endpoint"""
    login_url = "https://login.microsoftonline.com/" + tenant + "/oauth2/v2.0/token"
    resource = "https://api.fabric.microsoft.com"

    payload = {
        'grant_type': 'password',
        'client_id': SP_ID,
        'client_secret': SP_SECRET,
        'scope': f"{resource}/.default",
        'username': username,
        'password': password
    }
    try:
        response = requests.post(
            login_url, data=payload, verify=False, timeout=10)
    except Exception as e:
        print(e)
        raise e

    return json.loads(response.content)["access_token"]

def get_token_for_azure_portal_api(credentials, tenant_id):
    token_endpoint = "https://login.microsoftonline.com/fd1fbf9f-991a-40b4-ae26-61dfc34421ef/oauth2/v2.0/token"
    data = {
        'grant_type': 'client_credentials',
        'client_id': credentials._client_id,
        'client_secret': credentials._client_credential,
        'scope': '74658136-14ec-4630-ad9b-26e160ff0fc6/.default'
    }
    response = requests.post(token_endpoint, data=data)
    return response.json()['access_token']


def authorized_get(uri, token):
    return requests.get(
        uri,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        timeout=10
    )


def authorized_post(uri, token, additional_headers={}, data=None):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    headers.update(additional_headers)
    return requests.post(
        uri,
        headers=headers,
        data=data,
        timeout=10
    )

def authorized_delete(uri, token):
    return requests.delete(
        uri,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        timeout=10
    )


def get_workspaces(token):
    workspaces_url = "https://api.fabric.microsoft.com/v1/workspaces"
    response = authorized_get(workspaces_url, token)
    return response.text


def list_capacities(token):
    capacities_url = "https://api.fabric.microsoft.com/v1/capacities"
    response = authorized_get(capacities_url, token)
    return response.text


def create_workspace(token, name, capacity_id):
    workspaces_url = "https://api.fabric.microsoft.com/v1/workspaces"
    data = {
        "displayName": name,
        "capacityId": capacity_id
    }
    response = authorized_post(workspaces_url, token, data)
    return response


def add_workspace_role(token, workspace_id, role, principal_id):
    workspaces_url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/roleAssignments"
    data = {
        "principal": {
            "id": principal_id,
            "type": "User"
        },
        "role": role
    }
    response = authorized_post(workspaces_url, token, data)
    return response

def delete_workspace_role(token, workspace_id, principal_id):
    workspaces_url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/roleAssignments/{principal_id}"
    response = authorized_delete(workspaces_url, token)
    return response
    
def delete_workspace(token, workspace_id):
    workspaces_url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}"
    response = authorized_delete(workspaces_url, token)
    return response

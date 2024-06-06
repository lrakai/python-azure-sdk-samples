import json
import time

from config import EVENT_CONFIG

# For debug
import logging
import sys
from http.client import HTTPConnection

import requests
import json

from azure.identity import ClientSecretCredential


def with_hint(result, hint=None):
    return {'result': result, 'hint_message': hint} if hint else result


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

def get_oauth2_permission_scopes(token, application_name):
    response = authorized_get(f"https://graph.microsoft.com/v1.0/servicePrincipals?$filter=displayName eq '{application_name}'&$select=id,displayName,appId,oauth2PermissionScopes", token)
    value = response.json()['value']
    return value

def get_service_principals(token, filter):
    applications_url = f"https://graph.microsoft.com/v1.0/servicePrincipals?$filter=displayName eq '{filter}'"
    response = authorized_get(applications_url, token)
    service_principals = json.loads(response.text)
    return service_principals['value']

def grant_admin_consent_graph(token, application_id, resource_id, scope):
    oauth2_permission_grant_url = f"https://graph.microsoft.com/v1.0/oauth2PermissionGrants"
    data = {
        "clientId": application_id,
        "consentType": "AllPrincipals",
        "resourceId": resource_id,
        "scope": scope
    }
    response = authorized_post(oauth2_permission_grant_url, token, {}, json.dumps(data))
    return response.status_code >= 200 and response.status_code < 300

def handler(event, context):
    credentials, subscription_id = get_credentials(event)
    token = credentials.get_token('https://graph.microsoft.com/.default').token
    # application_name = event['provisioning_block_outputs']['userdataAppRegName']['value']
    # jwt_application_name = event['provisioning_block_outputs']['userdataJwtAppRegName']['value']
    application_name = 'cal-postman-teal-cat-nbk'
    jwt_application_name = 'cal-jwt-teal-cat-nbk'
    service_principal = get_service_principals(token, application_name)
    if not any(service_principal):
        return with_hint(False, f'Did not find service principal {application_name}.')
    service_principal = service_principal[0]

    app_scopes = get_oauth2_permission_scopes(token, application_name)
    jwt_app_scopes = get_oauth2_permission_scopes(token, jwt_application_name)
    admin_consent_tally = 0
    for app_scope in app_scopes + jwt_app_scopes:
        app_object_id = app_scope['id']
        for scope in app_scope['oauth2PermissionScopes']:
            try:
                if grant_admin_consent_graph(token, service_principal['id'], app_object_id, scope['value']):
                    admin_consent_tally += 1
            except Exception as e:
                print(e)

    return with_hint(admin_consent_tally >= 2, f'Granted admin consent for {admin_consent_tally} API permissions (expected 2).')


def get_credentials(event):
    subscription_id = event['environment_params']['subscription_id']
    credentials = ClientSecretCredential(
        client_id=event['credentials']['credential_id'],
        client_secret=event['credentials']['credential_key'],
        tenant_id=event['environment_params']['tenant']
    )
    return credentials, subscription_id
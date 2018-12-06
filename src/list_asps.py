import os
import json

from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.web import WebSiteManagementClient

from config import CONFIG


def get_credentials():
    subscription_id = CONFIG['subscription_id']
    credentials = ServicePrincipalCredentials(
        client_id=CONFIG['client_id'],
        secret=CONFIG['client_secret'],
        tenant=CONFIG['tenant_id']
    )
    return credentials, subscription_id


def list_asps():
    ''' List Azure App Service Plans '''
    credentials, subscription_id = get_credentials()
    resource_group = CONFIG['resource_group']

    resource_client = ResourceManagementClient(credentials, subscription_id)
    for item in resource_client.resources.list_by_resource_group(resource_group):
        print(item.name)

    web_client = WebSiteManagementClient(credentials, subscription_id)
    for asp in web_client.app_service_plans.list_by_resource_group(resource_group):
        print(asp.name)

    return any(web_client.app_service_plans.list_by_resource_group(resource_group))

if __name__ == "__main__":
    has_asps = list_asps()
    print(has_asps)
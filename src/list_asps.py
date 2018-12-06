import os
import json

from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.web import WebSiteManagementClient

RESOURCE_GROUP = 'cal-512'


def get_credentials():
    subscription_id = os.environ['AZURE_SUBSCRIPTION_ID']
    credentials = ServicePrincipalCredentials(
        client_id=os.environ['AZURE_CLIENT_ID'],
        secret=os.environ['AZURE_CLIENT_SECRET'],
        tenant=os.environ['AZURE_TENANT_ID']
    )
    return credentials, subscription_id


def list_asps():
    ''' List Azure App Service Plans '''
    credentials, subscription_id = get_credentials()

    resource_client = ResourceManagementClient(credentials, subscription_id)
    for item in resource_client.resources.list_by_resource_group(RESOURCE_GROUP):
        print(item.name)

    web_client = WebSiteManagementClient(credentials, subscription_id)
    for asp in web_client.app_service_plans.list_by_resource_group(RESOURCE_GROUP):
        print(asp.name)

    return any(web_client.app_service_plans.list_by_resource_group(RESOURCE_GROUP))

if __name__ == "__main__":
    has_asps = list_asps()
    print(has_asps)
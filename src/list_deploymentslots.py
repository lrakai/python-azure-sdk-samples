import json

from azure.mgmt.web import WebSiteManagementClient

from config import CONFIG
from credentials import credential_helper

def list_deploymentslots():
    ''' List Azure App Service Plans '''
    credentials, subscription_id = credential_helper.get_credentials()
    resource_group = CONFIG['resource_group']

    web_client = WebSiteManagementClient(credentials, subscription_id)
    for webapp in web_client.web_apps.list_by_resource_group(resource_group):
        if any(web_client.web_apps.list_slots(resource_group, webapp.name)):
            return True
    return False


if __name__ == "__main__":
    has_deploymentslots = list_deploymentslots()
    print(has_deploymentslots)

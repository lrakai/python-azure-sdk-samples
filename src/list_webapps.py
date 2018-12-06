import json

from azure.mgmt.web import WebSiteManagementClient

from config import CONFIG
from credentials import credential_helper


def list_webapps():
    ''' List Azure Web Apps '''
    credentials, subscription_id = credential_helper.get_credentials()
    resource_group = CONFIG['resource_group']

    web_client = WebSiteManagementClient(credentials, subscription_id)
    for webapp in web_client.web_apps.list_by_resource_group(resource_group):
        print(webapp.name)

    return any(web_client.web_apps.list_by_resource_group(resource_group))


if __name__ == "__main__":
    has_webapps = list_webapps()
    print(has_webapps)

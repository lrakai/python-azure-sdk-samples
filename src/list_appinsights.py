import json

from azure.mgmt.resource import ResourceManagementClient

from config import CONFIG
from credentials import credential_helper


def list_appinsights():
    ''' List Application Insights '''
    credentials, subscription_id = credential_helper.get_credentials()
    resource_group = CONFIG['resource_group']

    resource_client = ResourceManagementClient(credentials, subscription_id)
    return any(resource.type == 'microsoft.insights/components' 
                for resource in resource_client.resources.list_by_resource_group(resource_group))


if __name__ == "__main__":
    has_appinsights = list_appinsights()
    print(has_appinsights)

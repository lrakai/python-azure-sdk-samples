import os
import json

from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute import ComputeManagementClient

RESOURCE_GROUP = 'cal-473'


def get_credentials():
    subscription_id = os.environ['AZURE_SUBSCRIPTION_ID']
    credentials = ServicePrincipalCredentials(
        client_id=os.environ['AZURE_CLIENT_ID'],
        secret=os.environ['AZURE_CLIENT_SECRET'],
        tenant=os.environ['AZURE_TENANT_ID']
    )
    return credentials, subscription_id


def list_vms():
    credentials, subscription_id = get_credentials()

    resource_client = ResourceManagementClient(credentials, subscription_id)
    # result_list = resource_client.resource_groups.list()
    # result_list = list(result_list)
    # print(json.dumps(result_list))

    for item in resource_client.resources.list_by_resource_group(RESOURCE_GROUP):
        print(item.name)

    compute_client = ComputeManagementClient(credentials, subscription_id)
    for vm in compute_client.virtual_machines.list(RESOURCE_GROUP):
        print(vm.name)

    return any(compute_client.virtual_machines.list(RESOURCE_GROUP))

if __name__ == "__main__":
    has_vms = list_vms()
    print(has_vms)
import os
import json

from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute import ComputeManagementClient

from config import CONFIG


def get_credentials():
    subscription_id = CONFIG['subscription_id']
    credentials = ServicePrincipalCredentials(
        client_id=CONFIG['client_id'],
        secret=CONFIG['client_secret'],
        tenant=CONFIG['tenant_id']
    )
    return credentials, subscription_id


def list_vms():
    credentials, subscription_id = get_credentials()
    resource_group = CONFIG['resource_group']

    resource_client = ResourceManagementClient(credentials, subscription_id)
    # result_list = resource_client.resource_groups.list()
    # result_list = list(result_list)
    # print(json.dumps(result_list))

    for item in resource_client.resources.list_by_resource_group(resource_group):
        print(item.name)

    compute_client = ComputeManagementClient(credentials, subscription_id)
    for vm in compute_client.virtual_machines.list(resource_group):
        print(vm.name)

    return any(compute_client.virtual_machines.list(resource_group))

if __name__ == "__main__":
    has_vms = list_vms()
    print(has_vms)
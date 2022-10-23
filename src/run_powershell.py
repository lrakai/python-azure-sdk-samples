import json

import re
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.compute import ComputeManagementClient
from msrestazure.azure_exceptions import CloudError

from config import CONFIG
from credentials import credential_helper


def run_powershell():
    credentials, subscription_id = credential_helper.get_credentials()
    resource_group = CONFIG['resource_group']

    compute_client = ComputeManagementClient(credentials, subscription_id)

    machines = [machine for machine in compute_client.virtual_machines.list(resource_group)]
    if not any(machines):
        return False
    vm_name = machines[0].name

    parameters = {
        'command_id': 'RunPowerShellScript',
        'script': [
          '''
          Get-Content -Path C:/Users/student/Desktop/pat.txt | Write-Host
          '''
        ]
    }

    try:
        poller = compute_client.virtual_machines.run_command(resource_group, vm_name, parameters)
        result = poller.result()
    except CloudError as exception:
        if 'Run command extension execution is in progress. Please wait for completion before invoking a run command.' in exception.message:
            return False
        print(exception)
        raise exception

    match = re.search("^\((\d+) rows affected\)$", result.value[0].message)
    return match is not None and int(match.group(1)) > 0


if __name__ == "__main__":
    success = run_powershell()
    print(success)

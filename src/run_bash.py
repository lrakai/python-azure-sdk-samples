from azure.identity import ClientSecretCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.core.exceptions import HttpResponseError

from config import CONFIG
from credentials import credential_helper

def with_hint(result, hint=None):
    return {'result': result, 'hint_message': hint} if hint else result

def run_bash():
    credentials, subscription_id = credential_helper.get_credentials()
    resource_group = CONFIG['resource_group']

    compute_client = ComputeManagementClient(credentials, subscription_id)

    parameters = {
        # Check for any Terraform state files that contai
        'command_id': 'RunShellScript',
        'script': [
            'if [ -f "/cloudacademy/lab/terraformlab/.terraform/terraform.tfstate" ]; then echo -n True; else echo -n False; fi ;'
        ]
    }

    try:
        poller = compute_client.virtual_machines.begin_run_command(
            resource_group, 'terraform-ide', parameters)
        result = poller.result(timeout=None)
    except HttpResponseError as exception:
        if 'Run command extension execution is in progress. Please wait for completion before invoking a run command.' in exception.message:
            print(exception.message)
            return with_hint(False, 'A previous commnand is still running. Please wait retry again in a minute or two.')
        print(exception)
        raise exception

    print(result.value[0].message)
    return with_hint('True' in result.value[0].message, 'Terraform state file not found in terraformlab/.terraform/terraform.tfstate')


def get_credentials(event):
    subscription_id = event['environment_params']['subscription_id']
    credentials = ClientSecretCredential(
        client_id=event['credentials']['credential_id'],
        client_secret=event['credentials']['credential_key'],
        tenant_id=event['environment_params']['tenant']
    )
    return credentials, subscription_id


if __name__ == "__main__":
    success = run_bash()
    print(success)

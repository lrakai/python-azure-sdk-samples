import json


from azure.identity import ClientSecretCredential
from azure.mgmt.compute import ComputeManagementClient


def with_hint(result, hint=None):
    return {"result": result, "hint_message": hint} if hint else result


def handler(event, context):
    credentials, subscription_id = get_credentials(event)
    resource_group = event["environment_params"]["resource_group"]

    client = ComputeManagementClient(credentials, subscription_id)

    machines = [machine for machine in client.virtual_machines.list(resource_group)]
    if not any(machines):
        return with_hint(False, "Wait for the VM to be provisioned.")

    vm_name = machines[0].name

    parameters = {
        "command_id": "RunPowerShellScript",
        "script": [
            """
            Set-Location -Path C:\\Users\\student\\llm-apps
            Write-Host "Bootstrapped"
            """
        ],
    }

    try:
        poller = client.virtual_machines.begin_run_command(
            resource_group, vm_name, parameters
        )
        result = poller.result(timeout=None)
    except Exception as e:
        print(e)
        return with_hint(False, "Failed to run command on the VM.")

    match = "ALL TESTS PASSED" in result.value[0].message
    if match:
        return True
    else:
        return with_hint(False, "Success criteria not met.")


if __name__ == "__main__":
    success = run_powershell()
    print(success)

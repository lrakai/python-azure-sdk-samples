import os

CONFIG = {
    'subscription_id': os.environ.get('AZURE_SUBSCRIPTION_ID'),
    'client_id'      : os.environ.get('AZURE_CLIENT_ID'),
    'client_secret'  : os.environ.get('AZURE_CLIENT_SECRET'),
    'tenant_id'      : os.environ.get('AZURE_TENANT_ID'),
    'resource_group' : os.environ.get('AZURE_RESOURCE_GROUP', 'my-rg')
}

EVENT_CONFIG = {
    'credentials': {
        'credential_id' : CONFIG['client_id'],
        'credential_key': CONFIG['client_secret']
    },
    'environment_params': {
        'subscription_id': CONFIG['subscription_id'],
        'tenant'         : CONFIG['tenant_id'],
        'resource_group' : CONFIG['resource_group']
    }
}
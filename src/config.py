import os

CONFIG = {
    'subscription_id': os.environ.get('AZURE_SUBSCRIPTION_ID'),
    'client_id'      : os.environ.get('AZURE_CLIENT_ID'),
    'client_secret'  : os.environ.get('AZURE_CLIENT_SECRET'),
    'tenant_id'      : os.environ.get('AZURE_TENANT_ID'),
    'resource_group' : os.environ.get('AZURE_RESOURCE_GROUP', 'my-rg')
}
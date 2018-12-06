from azure.common.credentials import ServicePrincipalCredentials

from config import CONFIG


class credential_helper:
    def get_credentials():
        subscription_id = CONFIG['subscription_id']
        credentials = ServicePrincipalCredentials(
            client_id=CONFIG['client_id'],
            secret=CONFIG['client_secret'],
            tenant=CONFIG['tenant_id']
        )
        return credentials, subscription_id

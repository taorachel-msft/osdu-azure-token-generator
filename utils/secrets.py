from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
import logging

logging.getLogger("azure.core").setLevel(logging.ERROR)
logging.getLogger("azure.identity").setLevel(logging.ERROR)

_logger = logging.getLogger(__name__)


def get_secrets(key_vault_uri: str):
    """
    Retrieve required secrets from Azure Key Vault
    """
    secrets = {}

    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=key_vault_uri, credential=credential)

    # aad-client-id & aad-client-secret are used for the Azure AD OAuth flow
    secrets["tenant_id"] = client.get_secret("tenant-id").value
    secrets["client_id"] = client.get_secret("aad-client-id").value
    secrets["client_secret"] = client.get_secret("aad-client-secret").value

    _logger.info("Successfully retrieved secrets from key vault")
    return secrets

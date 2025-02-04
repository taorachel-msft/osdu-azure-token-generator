import logging
import os
import requests
import yaml

from utils.arguments import get_args
from utils.secrets import get_secrets

_logger = logging.getLogger(__name__)


def load_environment(environment: str) -> dict:
    """
    Load variables from environments.yml
    """
    _logger.info(f"Loading {environment} environment")

    app_dir = os.path.dirname(os.path.abspath(__file__))

    with open(f"{app_dir}/environments.yml", "r") as file:
        environments = yaml.safe_load(file)
        return environments[environment]


def generate_token(tenant_id: str, client_id: str) -> str:
    """
    Create token generation url and parse authorization code from redirect
    """
    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/authorize?client_id={client_id}&response_type=code&redirect_uri=http://localhost:8080&response_mode=query&scope={client_id}%2f.default&state=12345&sso_reload=true"

    # Step needs to be done manually due to required Microsoft sso login information
    print(
        f"---------------------------\n\nNavigate to:\n{url}\n\n---------------------------"
    )

    return parse_code(input("Enter the full URL after redirect: "))


def parse_code(url: str) -> str:
    """
    Parse redirect URL and get authorization code
    """
    code = None
    try:
        code = url.split("code=")[1].split("&")[0]
        _logger.info("Successfully parsed authorization code from redirect")
        return code
    except Exception as e:
        _logger.error(f"Error: failed to parse code - {e}")
        exit()


def retrieve_token(
    tenant_id: str, client_id: str, client_secret: str, auth_code: str
) -> str:
    """
    Retrieve token using authorization code
    """
    _logger.info("Retrieving token using authorization code")

    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": f"{client_id}/.default openid profile offline_access",
        "redirect_uri": "http://localhost:8080",
        "code": auth_code,
    }

    response = requests.post(url, headers=headers, data=data)

    try:
        json = response.json()
        _logger.info("Success! Retrieved token")
        return json["access_token"]

    except Exception as e:
        _logger.error(f"Error: {e}")
        _logger.error(f"Response: {response.text}")
        exit()


def main(args):
    env = load_environment(args.env)

    secrets = get_secrets(env["key_vault_uri"])

    auth_code = generate_token(secrets["tenant_id"], secrets["client_id"])
    token = retrieve_token(**secrets, auth_code=auth_code)

    print(
        f"---------------------------\n\nToken:\n{token}\n\n---------------------------"
    )


if __name__ == "__main__":
    args = get_args()
    logging.basicConfig(level=args.log_level)

    _logger.info("Starting token generation")
    main(args)
    _logger.info("Token generation complete")

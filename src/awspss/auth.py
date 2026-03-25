import sys
import time
import webbrowser

import boto3
from botocore.exceptions import ClientError, BotoCoreError


def login(start_url: str, region: str) -> str:
    try:
        oidc = boto3.client("sso-oidc", region_name=region)

        client_info = oidc.register_client(
            clientName="awspss",
            clientType="public",
        )
        client_id = client_info["clientId"]
        client_secret = client_info["clientSecret"]

        device_auth = oidc.start_device_authorization(
            clientId=client_id,
            clientSecret=client_secret,
            startUrl=start_url,
        )
    except (ClientError, BotoCoreError) as e:
        print(f"Error: SSO login failed - {e}", file=sys.stderr)
        raise SystemExit(1)

    verification_uri = device_auth["verificationUriComplete"]
    user_code = device_auth["userCode"]
    device_code = device_auth["deviceCode"]
    interval = device_auth.get("interval", 5)
    expires_in = device_auth["expiresIn"]

    print(f"\nPlease authenticate in your browser.", file=sys.stderr)
    print(f"Code: {user_code}", file=sys.stderr)
    print(f"URL: {verification_uri}\n", file=sys.stderr)

    webbrowser.open(verification_uri)

    token_response = _poll_for_token(
        oidc, client_id, client_secret, device_code, interval, expires_in
    )

    return token_response["accessToken"], token_response["expiresIn"]


def _poll_for_token(
    oidc, client_id: str, client_secret: str,
    device_code: str, interval: int, expires_in: int,
) -> dict:
    deadline = time.time() + expires_in

    while time.time() < deadline:
        try:
            return oidc.create_token(
                clientId=client_id,
                clientSecret=client_secret,
                grantType="urn:ietf:params:oauth:grant-type:device_code",
                deviceCode=device_code,
            )
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "AuthorizationPendingException":
                time.sleep(interval)
            elif error_code == "SlowDownException":
                interval += 5
                time.sleep(interval)
            else:
                raise

    raise TimeoutError("Authentication timed out. Please try again.")

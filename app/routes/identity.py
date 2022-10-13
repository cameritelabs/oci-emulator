import logging
import json

from flask import Blueprint, request, Response


logger = logging.getLogger(__name__)
identity = Blueprint("identity", __name__)


@identity.route("/users", methods=["GET"])
def list_instances():
    compartment_id = request.args.get("compartmentId")

    return Response(
        status=200,
        content_type="application/json",
        response=json.dumps(
            [
                {
                    "capabilities": {
                        "canUseConsolePassword": False,
                        "canUseApiKeys": True,
                        "canUseAuthTokens": True,
                        "canUseSmtpCredentials": True,
                        "canUseCustomerSecretKeys": True,
                        "canUseOAuth2ClientCredentials": True,
                        "canUseDbCredentials": True,
                    },
                    "emailVerified": True,
                    "identityProviderId": "ocid1.saml2idp.oc1..aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                    "externalIdentifier": "0123456789abcdef0123456789abcdef",
                    "timeModified": "2022-10-06T16:49:46.990Z",
                    "isMfaActivated": False,
                    "id": "ocid1.user.oc1..aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                    "compartmentId": compartment_id,
                    "name": "oracleidentitycloudservice/user@mail.com",
                    "description": "user@mail.com",
                    "timeCreated": "2021-02-04T20:36:51.716Z",
                    "freeformTags": {},
                    "definedTags": {
                        "Oracle-Tags": {
                            "CreatedBy": "scim-service",
                            "CreatedOn": "2021-02-04T20:36:51.694Z",
                        }
                    },
                    "lifecycleState": "ACTIVE",
                }
            ]
        ),
        headers={
            "opc-request-id": request.headers["Opc-Request-Id"]
            if "Opc-Request-Id" in request.headers
            else ""
        },
    )


@identity.route("/users/<user_ocid>", methods=["GET"])
def get_instance(user_ocid):
    return Response(
        status=200,
        content_type="application/json",
        response=json.dumps(
            {
                "capabilities": {
                    "canUseConsolePassword": False,
                    "canUseApiKeys": True,
                    "canUseAuthTokens": True,
                    "canUseSmtpCredentials": True,
                    "canUseCustomerSecretKeys": True,
                    "canUseOAuth2ClientCredentials": True,
                    "canUseDbCredentials": True,
                },
                "emailVerified": True,
                "identityProviderId": "ocid1.saml2idp.oc1..aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "externalIdentifier": "0123456789abcdef0123456789abcdef",
                "timeModified": "2022-10-06T16:49:46.990Z",
                "isMfaActivated": False,
                "id": user_ocid,
                "compartmentId": "ocid1.tenancy.oc1..aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "name": "oracleidentitycloudservice/user@mail.com",
                "description": "user@mail.com",
                "timeCreated": "2021-02-04T20:36:51.716Z",
                "freeformTags": {},
                "definedTags": {
                    "Oracle-Tags": {
                        "CreatedBy": "scim-service",
                        "CreatedOn": "2021-02-04T20:36:51.694Z",
                    }
                },
                "lifecycleState": "ACTIVE",
            }
        ),
        headers={
            "opc-request-id": request.headers["Opc-Request-Id"]
            if "Opc-Request-Id" in request.headers
            else ""
        },
    )

from werkzeug.wrappers import Request, Response, ResponseStream
import json


class middleware:
    """
    Simple WSGI middleware
    """

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):

        request = Request(environ)
        if "/n/" in request.path and "/b/" in request.path and "/o/" in request.path:
            return self.app(environ, start_response)

        if "Authorization" not in request.headers:
            res = Response(
                status=404,
                response=json.dumps(
                    {
                        "code": "NotAuthorizedOrNotFound",
                        "message": "Authorization failed or requested resource not found.",
                    }
                ),
                content_type="application/json",
                headers={
                    "opc-request-id": request.headers["Opc-Request-Id"]
                    if "Opc-Request-Id" in request.headers
                    else ""
                },
            )
            return res(environ, start_response)

        tenancy, user, fingerprint = None, None, None
        headers = request.headers["Authorization"].split(",")

        for header in headers:
            if "keyId=" in header:
                header = header.replace('keyId="', "").replace('"', "")
                tenancy, user, fingerprint = header.split("/")

        environ["credentials"] = {
            "tenancy": tenancy,
            "user": user,
            "fingerprint": fingerprint,
        }
        return self.app(environ, start_response)

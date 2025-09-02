
import http.server
import urllib
import requests
from Core import WebSEngine


def Check(handler: http.server.BaseHTTPRequestHandler, method: str, headers: dict, body: str | bytes, checks):
    valid_token_check = checks.get("recaptcha-check", False)
    secret_recaptcha_key = checks.get("recaptcha-secret-key", '')

    if valid_token_check:
        parsed = urllib.parse.urlparse(handler.path)
        queries = urllib.parse.parse_qs(parsed.query)

        response_token = queries.get("recaptcha_token",[])
        response_token = ''.join(response_token)

        r = requests.post("https://www.google.com/recaptcha/api/siteverify",data={
            "secret":secret_recaptcha_key,
            "response":response_token
        })

        if r.json()["success"] is not True:
            WebSEngine.RequestHandlerMethods.SendPlainResponse(handler,"Failed recaptcha check!",403)
            return 0

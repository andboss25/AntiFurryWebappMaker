from Core import WebSEngine
import http.server

def Check(handler: http.server.BaseHTTPRequestHandler, method: str, headers: dict, body: str | bytes, checks):
    valid_token_check = checks.get("valid-token-check", False)
    if valid_token_check:
        token = headers.get('Authroization','')
        if handler.db.Execute("SELECT * FROM users WHERE token=?",(token,)).fetchone() is None:
            WebSEngine.RequestHandlerMethods.SendPlainResponse(handler,'Invalid token or no token supplied!',403)
            return 0
        else:
            pass
    
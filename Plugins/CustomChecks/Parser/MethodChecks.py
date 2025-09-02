
from Core import WebSEngine
import http.server

# Method Related Checks

def Check(handler:http.server.BaseHTTPRequestHandler,method:str,headers:dict,body:str|bytes,checks):
    allowed_methods = checks.get("allowed-methods",["GET"])
    if method not in allowed_methods:
        WebSEngine.RequestHandlerMethods.SendPlainResponse(handler,"Method not allowed!",405)
        return 0

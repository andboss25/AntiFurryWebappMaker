
import WebSEngine
import http.server
import urllib

# URL Related And Param Related Checks

def Check(
    handler:http.server.BaseHTTPRequestHandler,method:str,headers:dict,body:str|bytes,checks):
    require_url_params = checks.get("require-url-params",[])
    if len(require_url_params) > 0:
        parsed = urllib.parse.urlparse(handler.path)
        queries = urllib.parse.parse_qs(parsed.query)
        provided_keys = set(queries.keys())
        required_set = set(require_url_params)

        if not ( required_set <= provided_keys ):
            WebSEngine.RequestHandlerMethods.SendPlainResponse(handler,f"Must attach all parameters in your url: {str(require_url_params)}!",400)
        
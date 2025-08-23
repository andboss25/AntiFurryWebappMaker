
import WebSEngine
import http.server
import json

# JSON Related Checks

def Check(handler:http.server.BaseHTTPRequestHandler,method:str,headers:dict,body:str|bytes,checks):

    must_be_json = checks.get("must-be-json",False)
    required_json_params = checks.get("require-json-params",[])

    if must_be_json == True and headers["Content-Type"] != "application/json":
        WebSEngine.RequestHandlerMethods.SendPlainResponse(handler,"Request must be json!",400)

    if must_be_json == True:
        try:
            json_content = json.loads(body)
        except:
            WebSEngine.RequestHandlerMethods.SendPlainResponse(handler,"Malformed json!",400)
            
    if len(required_json_params) > 0 and must_be_json is True:
        required_set = set(required_json_params)
        provided_set = set(json_content.keys())

        if not required_set <= provided_set:
            WebSEngine.RequestHandlerMethods.SendPlainResponse(handler,f"Must attach all parameters in your json: {str(required_json_params)}!",400)

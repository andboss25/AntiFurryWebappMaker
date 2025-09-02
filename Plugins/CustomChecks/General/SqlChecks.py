

from Core import WebSEngine
import http.server
import urllib

# SQL Related Checks

def Check(handler:http.server.BaseHTTPRequestHandler,method:str,headers:dict,body:str|bytes,checks):
    compare_query_operation = checks.get("compare-query-operation",[])
    if len(compare_query_operation) > 0:
        needed_params = compare_query_operation["params"]
        query = compare_query_operation["query"]
        op = compare_query_operation["operation"]
        failresp = compare_query_operation["failresp"]
            
        parsed = urllib.parse.urlparse(handler.path)
        queries = urllib.parse.parse_qs(parsed.query)

        data = []

        for key in queries:
            data.append(queries[key][0])
            
        if op == "PASS_IF_EXISTS" and len(handler.db.Execute(query,data).fetchall()) == 0:
            WebSEngine.RequestHandlerMethods.SendResponse(handler,failresp,400,"application/json")
            return 0

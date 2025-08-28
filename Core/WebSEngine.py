# Simple Web-Server abstraction layer using http.server
# Written by andreiplsno

import LuaEvaluator
import HandleDatabse

import http.server
import json
import urllib
import lupa
from pathlib import Path
import importlib.util
import sys

class Helpfull:
    def IsLuaTable(obj):
        """Check if an object is a Lua table."""
        return hasattr(obj, "keys") and not isinstance(obj, dict)

    def LuaToPython(self,obj):
        """Recursively convert Lua table to Python dict/list for JSON serialization."""
        if hasattr(obj, "items") and callable(getattr(obj, "items")):
            keys = list(obj.keys())
            if all(isinstance(k, int) for k in keys) and keys == list(range(1, len(keys)+1)):
                return [self.LuaToPython(obj[i]) for i in range(1, len(keys)+1)]
            else:
                return {k: self.LuaToPython(obj[k]) for k in obj.keys()}
        elif isinstance(obj, (str, int, float, bool)) or obj is None:
            return obj
        else:
            return str(obj)

class BaseResponse:
    """
    BaseResponse:
    Reprsents a basic http/https response.
    """
    def __init__(self,code:int,headers:dict,content:bytes):

        """
        Build a BaseResponse with a code , headers of choice and content
        """

        self.code = code
        self.headers = headers
        self.content = content
    
    def BuildBasicHeaderSet(self,content_type):
        """
        Automatically assign headers to your BaseResponse
        Headers assigned are:
            content-type -> content-type provided
            content-length -> length of content
            server -> 'AFWEBAPP - Built using python ThreadingHTTPServer'
        """
        self.headers["content-type"] = f"{content_type};"
        self.headers["content-length"] = len(self.content)
        self.headers["server"] = "AFWEBAPP - Built using python ThreadingHTTPServer"

    def SendBaseResponse(self,handler = http.server.BaseHTTPRequestHandler):
        """
        Send a BaseResponse trough the RequestHandler provided
        """
        handler.send_response(code=self.code)
        for header in self.headers:
            handler.send_header(keyword=header,value=self.headers[header])
        handler.end_headers()
        handler.wfile.write(self.content)

class RequestHandlerMethods:
    # Build methods:
    def BuildResponse(myself = http.server.BaseHTTPRequestHandler,message:str = "",code:int=200,content_type='text/plain') -> BaseResponse:
        """Like SendResponse() but it actually returns the BaseResponse and it does not send it."""
        try:
            message = message.encode()
        except:
            pass

        response = BaseResponse(code,{},message)
        response.BuildBasicHeaderSet(content_type)
        return response
    
    def BuildJsonResponse(myself = http.server.BaseHTTPRequestHandler,message:dict={},code:int=200):
        """Like SendJsonResponse() but it actually returns the BaseResponse and it does not send it."""
        # Turn lua table to python table
        if Helpfull.IsLuaTable(message):
            message = Helpfull().LuaToPython(message)

        response = BaseResponse(code,{},json.dumps(message).encode())
        response.BuildBasicHeaderSet("application/json")
        return response
    
    def BuildPlainResponse(myself = http.server.BaseHTTPRequestHandler,message:str = "",code:int=200):
        """Like SendPlainResponse() but it actually returns the BaseResponse and it does not send it."""
        response = BaseResponse(code,{},message.encode())
        response.BuildBasicHeaderSet("text/plain")
        return response

    def BuildHtmlResponse(myself = http.server.BaseHTTPRequestHandler,message:str = "",code:int=200):
        """Like SendHtmlResponse() but it actually returns the BaseResponse and it does not send it."""
        response = BaseResponse(code,{},message.encode())
        response.BuildBasicHeaderSet("text/html")
        return response
    
    def BuildHtmlResponseFile(myself = http.server.BaseHTTPRequestHandler,file_path:str = "",code:int=200):
        """Like SendHTMLResponseFile() but it actually returns the BaseResponse and it does not send it."""
        file = open(file_path,"r")
        response = BaseResponse(code,{},file.read().encode())
        file.close()
        response.BuildBasicHeaderSet("text/html")
        return response
    
    # Send methods:
    def SendResponse(myself = http.server.BaseHTTPRequestHandler,message:str = "",code:int=200,content_type='text/plain'):
        """Send a HTTP/HTTPS response with all parameters provided."""
        response = RequestHandlerMethods.BuildResponse(myself,message,code,content_type)
        response.SendBaseResponse(myself)
    
    def SendJsonResponse(myself = http.server.BaseHTTPRequestHandler,message:dict={},code:int=200):
        """Send a HTTP/HTTPS dict response (it will be automatically parsed to json) with all parameters provided."""
        response = RequestHandlerMethods.BuildJsonResponse(myself,message,code)
        response.SendBaseResponse(myself)

    def SendPlainResponse(myself = http.server.BaseHTTPRequestHandler,message:str = "",code:int=200):
        """Send a HTTP/HTTPS text/plain response with all parameters provided."""
        response = RequestHandlerMethods.BuildPlainResponse(myself,message,code)
        response.SendBaseResponse(myself)

    def SendHtmlResponse(myself = http.server.BaseHTTPRequestHandler,message:str = "",code:int=200):
        """Send a HTTP/HTTPS text/html response with all parameters provided."""
        response = RequestHandlerMethods.BuildHtmlResponse(myself,message,code)
        response.SendBaseResponse(myself)

    def SendHtmlResponseFile(myself = http.server.BaseHTTPRequestHandler,file_path:str = "",code:int=200):
        """Send a HTTP/HTTPS text/html response with all parameters provided."""
        response = RequestHandlerMethods.BuildHtmlResponseFile(myself,file_path,code)
        response.SendBaseResponse(myself)

class StaticResponsePathTypes:
    HTML_FILE = "HTML_FILE"
    HTML_RAW = "HTML_RAW"
    JSON = "JSON"
    TEXT_LITERAL = "TEXT_LITERAL"
    OTHER = "OTHER"

class StaticResponsePath:
    def __init__(self,path:str = "/",response_type:StaticResponsePathTypes = StaticResponsePathTypes.TEXT_LITERAL,code:int = 200,response:dict|str|bytes = "",content_type_specified:str = "text/plain",model_check_list:dict = {}):
        self.path = path
        self.response_type = response_type
        self.code = code
        self.response = response
        self.content_type_specified = content_type_specified
        self.model_check_list = model_check_list

    def HostWithoutPathAccounting(self,handler:http.server.BaseHTTPRequestHandler,method,headers,body):
        
        # List trough plugin list of checks

        parser_pathlist = Path("Plugins\\CustomChecks\\Parser").rglob('*.py')

        for file in parser_pathlist:
            # Create a module spec from file
            spec = importlib.util.spec_from_file_location(file.stem, str(file))
            module = importlib.util.module_from_spec(spec)
            sys.modules[file.stem] = module
            spec.loader.exec_module(module)

            # Retrieve function
            Check = getattr(module, "Check", None)

            # Weird bug on api listings making checks be lists
            if type(self.model_check_list) != dict:
                self.model_check_list = {}
            if Check(handler,method,headers,body,self.model_check_list) == 0:
                return
        
        general_pathlist = Path("Plugins\\CustomChecks\\General").rglob('*.py')

        for file in general_pathlist:
            # Create a module spec from file
            spec = importlib.util.spec_from_file_location(file.stem, str(file))
            module = importlib.util.module_from_spec(spec)
            sys.modules[file.stem] = module
            spec.loader.exec_module(module)

            # Retrieve function
            Check = getattr(module, "Check", None)
            if Check(handler,method,headers,body,self.model_check_list) == 0:
                return

        # Host based on type

        if self.response_type == "HTML_FILE":
            RequestHandlerMethods.SendHtmlResponseFile(handler,self.response,self.code)
        elif self.response_type == "HTML_RAW":
            RequestHandlerMethods.SendHtmlResponse(handler,self.response,self.code)
        elif self.response_type == "JSON":
            RequestHandlerMethods.SendJsonResponse(handler,self.response,self.code)
        elif self.response_type == "TEXT_LITERAL":
            RequestHandlerMethods.SendPlainResponse(handler,self.response,self.code)
        elif self.response_type == "OTHER":
            RequestHandlerMethods.SendResponse(handler,self.response,self.code,self.content_type_specified)

class DynamicResponsePath:
    def __init__(self,path:str = "/",script_path:str = "",model_check_list:dict = {}):
        self.path = path
        self.script_path = script_path
        self.model_check_list = model_check_list

    def HostWithoutPathAccounting(self,handler:http.server.BaseHTTPRequestHandler,method:str,headers:dict,body:str|bytes):
        
        # List trough plugin list of checks

        parser_pathlist = Path("Plugins\\CustomChecks\\Parser").rglob('*.py')

        for file in parser_pathlist:
            # Create a module spec from file
            spec = importlib.util.spec_from_file_location(file.stem, str(file))
            module = importlib.util.module_from_spec(spec)
            sys.modules[file.stem] = module
            spec.loader.exec_module(module)

            # Retrieve function
            Check = getattr(module, "Check", None)
            if Check(handler,method,headers,body,self.model_check_list) == 0:
                return
        
        general_pathlist = Path("Plugins\\CustomChecks\\General").rglob('*.py')

        for file in general_pathlist:
            # Create a module spec from file
            spec = importlib.util.spec_from_file_location(file.stem, str(file))
            module = importlib.util.module_from_spec(spec)
            sys.modules[file.stem] = module
            spec.loader.exec_module(module)

            # Retrieve function
            Check = getattr(module, "Check", None)
            if Check(handler,method,headers,body,self.model_check_list) == 0:
                return


        # Run script

        runner = LuaEvaluator.LuaRunner(handler_instance=handler)
        parsed = urllib.parse.urlparse(handler.path)

        queries = {}

        for query in urllib.parse.parse_qs(parsed.query):
            queries[query] = str(urllib.parse.parse_qs(parsed.query)[query][0])

        runner.AddGlobals({
            "QUERY_PARAMS": queries
            , "REQUEST_METHOD": method
            , "REQUEST_HEADERS": headers
            , "REQUEST_BODY" : body
            , "APP_DATABASE" : handler.db
        })
        runner.RunLuaMain(self.script_path)()

class RequestHandler(http.server.BaseHTTPRequestHandler):
    paths : dict[StaticResponsePath|DynamicResponsePath] = []
    db:HandleDatabse.Database = None
    not_found_page:StaticResponsePath = None

    def do_GET(self):
        try:
            method = "GET"
            headers = self.headers
            body = self.rfile.read(int(headers.get("Content-Length",0)))
            found = False
            path = urllib.parse.urlparse(self.path).path

            for obj in self.paths:
                if path == obj.path:
                    found = True
                    obj.HostWithoutPathAccounting(self,method,headers,body)
            
            if found == False:
                self.not_found_page.HostWithoutPathAccounting(self,method,headers,body)
        except ConnectionAbortedError:
            pass
        except Exception as e:
            RequestHandlerMethods.SendHtmlResponse(self,f"<h1>500 - Internal Server Error</h1>{str(e)}",500)
            raise e

    def do_POST(self):
        try:
            method = "POST"
            headers = self.headers
            body = self.rfile.read(int(headers.get("Content-Length",0)))
            found = False
            path = urllib.parse.urlparse(self.path).path

            for obj in self.paths:
                if path == obj.path:
                    found = True
                    obj.HostWithoutPathAccounting(self,method,headers,body)
            
            if found == False:
                self.not_found_page.HostWithoutPathAccounting(self,method,headers,body)
        except ConnectionAbortedError:
            pass
        except Exception as e:
            RequestHandlerMethods.SendHtmlResponse(self,f"<h1>500 - Internal Server Error</h1>{str(e)}",500)
            raise e
        
    def do_PUT(self):
        try:
            method = "PUT"
            headers = self.headers
            body = self.rfile.read(int(headers.get("Content-Length",0)))
            found = False
            path = urllib.parse.urlparse(self.path).path

            for obj in self.paths:
                if path == obj.path:
                    found = True
                    obj.HostWithoutPathAccounting(self,method,headers,body)
            
            if found == False:
                self.not_found_page.HostWithoutPathAccounting(self,method,headers,body)
        except ConnectionAbortedError:
            pass
        except Exception as e:
            RequestHandlerMethods.SendHtmlResponse(self,f"<h1>500 - Internal Server Error</h1>{str(e)}",500)
            raise e
        
    def do_PATCH(self):
        try:
            method = "PATCH"
            headers = self.headers
            body = self.rfile.read(int(headers.get("Content-Length",0)))
            found = False
            path = urllib.parse.urlparse(self.path).path

            for obj in self.paths:
                if path == obj.path:
                    found = True
                    obj.HostWithoutPathAccounting(self,method,headers,body)
            
            if found == False:
                self.not_found_page.HostWithoutPathAccounting(self,method,headers,body)
        except ConnectionAbortedError:
            pass
        except Exception as e:
            RequestHandlerMethods.SendHtmlResponse(self,f"<h1>500 - Internal Server Error</h1>{str(e)}",500)
            raise e
        
    def do_DELETE(self):
        try:
            method = "DELETE"
            headers = self.headers
            body = self.rfile.read(int(headers.get("Content-Length",0)))
            found = False
            path = urllib.parse.urlparse(self.path).path

            for obj in self.paths:
                if path == obj.path:
                    found = True
                    obj.HostWithoutPathAccounting(self,method,headers,body)
            
            if found == False:
                self.not_found_page.HostWithoutPathAccounting(self,method,headers,body)
        except ConnectionAbortedError:
            pass
        except Exception as e:
            RequestHandlerMethods.SendHtmlResponse(self,f"<h1>500 - Internal Server Error</h1>{str(e)}",500)
            raise e
        
class Server:
    def __init__(self,port:int = 80,addr:str = '',server_class=http.server.ThreadingHTTPServer,server_handler_class=RequestHandler):
        self.port = port
        self.addr = addr
        self.server_class = server_class
        self.server_handler_class = server_handler_class
        self.server_object = server_class((addr,port), server_handler_class)

    def Serve(self):
        self.server_object.serve_forever()

# Simple Web-Server abstraction layer using http.server
# Written by andreiplsno
import http.server
import json

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
        self.headers["content-lenght"] = len(self.content)
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
    
    def BuildHTMLResponseFile(myself = http.server.BaseHTTPRequestHandler,file_path:str = "",code:int=200):
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

    def SendHTMLResponseFile(myself = http.server.BaseHTTPRequestHandler,file_path:str = "",code:int=200):
        """Send a HTTP/HTTPS text/html response with all parameters provided."""
        response = RequestHandlerMethods.BuildHTMLResponseFile(myself,file_path,code)
        response.SendBaseResponse(myself)

class StaticResponsePathTypes:
    HTML_FILE = "HTML_FILE"
    HTML_RAW = "HTML_RAW"
    JSON = "JSON"
    TEXT_LITERAL = "TEXT_LITERAL"
    OTHER = "OTHER"

class StaticResponsePath:
    def __init__(self,path:str = "/",response_type:StaticResponsePathTypes = StaticResponsePathTypes.TEXT_LITERAL,code:int = 200,response:dict|str|bytes = "",content_type_specified:str = "text/plain"):
        self.path = path
        self.response_type = response_type
        self.code = code
        self.response = response
        self.content_type_specified = content_type_specified

    def HostWithoutPathAccounting(self,handler):
        if self.response_type == "HTML_FILE":
            RequestHandlerMethods.SendHTMLResponseFile(handler,self.response,self.code)
        elif self.response_type == "HTML_RAW":
            RequestHandlerMethods.SendHtmlResponse(handler,self.response,self.code)
        elif self.response_type == "JSON":
            RequestHandlerMethods.SendJsonResponse(handler,self.response,self.code)
        elif self.response_type == "TEXT_LITERAL":
            RequestHandlerMethods.SendPlainResponse(handler,self.response,self.code)
        elif self.response_type == "OTHER":
            RequestHandlerMethods.SendResponse(handler,self.response,self.code,self.content_type_specified)

class RequestHandler(http.server.BaseHTTPRequestHandler):
    paths : dict[StaticResponsePath] = []
    not_found_page:StaticResponsePath = None

    def do_GET(self):

        found = False

        for obj in self.paths:
            if self.path == obj.path:
                found = True
                obj.HostWithoutPathAccounting(self)
        
        if found == False:
            self.not_found_page.HostWithoutPathAccounting(self)
                
class Server:
    def __init__(self,port:int = 80,addr:str = '',server_class=http.server.ThreadingHTTPServer,server_handler_class=RequestHandler):
        self.port = port
        self.addr = addr
        self.server_class = server_class
        self.server_handler_class = server_handler_class
        self.server_object = server_class((addr,port), server_handler_class)

    def Serve(self):
        self.server_object.serve_forever()

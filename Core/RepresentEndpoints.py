# Simple badly written bridge that connects and represents the points from the model file to a WebS engine
# Written by andreiplsno
import ParseModelFile
import WebSEngine

class Briger():
    def __init__(self,app,handler = WebSEngine.RequestHandler):
        self.app = app
        self.handler = handler

    def JoinPath(self, parent, child):
        if not parent:
            return "/" + child.lstrip("/")
        
        return parent.rstrip("/") + "/" + child.lstrip("/")
    
    def InterpretPointToStatic(self,point,current_path:str):
        resp = None
        code = 200
        resp_type = None
        sepcified_content_type = None

        if point.type == "Page":
            resp = point.element_object.source_page
            resp_type = WebSEngine.StaticResponsePathTypes.HTML_FILE
        elif point.type == "Endpoint":
            resp = point.element_object.set_response
            resp_type = WebSEngine.StaticResponsePathTypes.OTHER
            sepcified_content_type = point.element_object.set_response_type
            code = point.element_object.set_response_code
        else:
            resp = {'Message':'This is a path listing!'}
            resp_type = WebSEngine.StaticResponsePathTypes.JSON
            code = 404
        
        return WebSEngine.StaticResponsePath(current_path,resp_type,code,resp,sepcified_content_type)

    def ParsePoint(self, point_dict: dict[ParseModelFile.Object], parent_path=""):
        paths = []
        for point in point_dict:
            current_path = self.JoinPath(parent_path, point.path)

            paths.append(
                self.InterpretPointToStatic(point,current_path)
            )

            if point.children:
                paths.extend(self.ParsePoint(point.children, current_path))

        return paths
    
    def Represent(self):
        self.handler.paths = self.ParsePoint(self.app.points)

        for special_point in self.app.special_points:
            self.handler.not_found_page = self.InterpretPointToStatic(special_point,"")

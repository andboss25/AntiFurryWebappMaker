
# Written by andreiplsno
# Simple model reader that takes care of the structure

# Imports
import json

# Declare Objects

class Object:
    def __init__(self,type:str,path:str,children:list,name:str,element_object):
        self.type = type
        self.path = path
        self.children = children
        self.name = name
        self.element_object = element_object
    
    def __repr__(self):
        return f"<Object name:{self.name} path:{self.path} type:{self.type} children:{self.children} element:{self.element_object}>"

class Endpoint:
    def __init__(self, props: dict):
        # Script props
        self.scriptable: bool = props.get("scriptable", True)

        # Request props
        self.allowed_methods: list = props.get("allowed-methods", ["GET", "POST"])

        # Set response props
        self.set_response: str = props.get("set-response", None)
        self.set_response_type: str = props.get("set-response-type", "json")
        self.set_response_code: int = props.get("set-response-code", 200)

class Page:
    def __init__(self, props: dict):
        # Page props
        self.source_page: str = props.get("source-page", "")

class PathFolder:
    def __init__(self,props:dict):
        pass

class SpecialPoint:
    def __init__(self,policy:str,element_object,name,type):
        self.policy = policy
        self.element_object = element_object
        self.name = name
        self.type = type

    def __repr__(self):
        return f"<SpecialPoint name:{self.name} policy:{self.policy} type:{self.type} element:{self.element_object}>"

class App:
    def __init__(self,points:dict[Object],special_points:dict[SpecialPoint],app_globals:dict,name:str,version:str):
        # App elements
        self.points = points
        self.special_points = special_points
        self.app_globals = app_globals

        # App props
        self.name = name
        self.version = version
    
    def __repr__(self):
        return f"<App name:{self.name} version:{self.version} app-globals:{self.app_globals} points:{self.points} special-points:{self.special_points}>"


class Reader:
    def __init__(self,file):
        self.file = file

    def ParsePoint(self,point_dict):
        objects = []
        for point in point_dict:
            # Define Type

            if point_dict[point]["type"] == "Page":
                element_type = Page(point_dict[point]["prop"])
            elif point_dict[point]["type"] == "Path":
                element_type = PathFolder(point_dict[point]["prop"])
            elif point_dict[point]["type"] == "Endpoint":
                element_type = Endpoint(point_dict[point]["prop"])

            # Define Object
            children_points = point_dict[point]["children"]
            point_object = Object(
                point_dict[point]["type"] ,
                point ,
                self.ParsePoint(children_points) if len(children_points) > 0 else None ,
                point_dict[point]["name"] ,
                element_type

            )

            objects.append(point_object)

        return objects
    
    def ParseSpecialPoint(self,point_dict):
        objects = []
        for point in point_dict:
            # Define Type
            if point_dict[point]["type"] == "Page":
                element_type = Page(point_dict[point]["prop"])
            elif point_dict[point]["type"] == "Path":
                element_type = PathFolder(point_dict[point]["prop"])
            elif point_dict[point]["type"] == "Endpoint":
                element_type = Endpoint(point_dict[point]["prop"])

            # Define Object
            point_object = SpecialPoint(
                point,
                element_type,
                point_dict[point]["name"],
                point_dict[point]["type"]
            )

            objects.append(point_object)

        return objects

    def ParseToApp(self) -> App:
        # Get file contents

        try:
            file_to_read_from = open(self.file,"r")
            file_contents = file_to_read_from.read()
            file_to_read_from.close()
            json_model_data = json.loads(file_contents)
        except:
            raise Exception("Error reading model file!")
        
        # Read App info

        try:
            app_name = json_model_data["app-info"]["name"]
            app_version = json_model_data["app-info"]["version"]
        except:
            raise Exception("Error reading model file app-info!")

        # Read Gobals

        try:
            app_globals = json_model_data["globals"]
        except:
            raise Exception("Error reading model file globals!")
        
        # Traverse points
        try:
            points = self.ParsePoint(json_model_data["points"])
        except:
            raise Exception("Error reading model file points!")
        
        # Travesre special points

        try:
            special_points = self.ParseSpecialPoint(json_model_data["special-points"])
        except:
            raise Exception("Error reading model file special-points!")
        
        return App(points,special_points,app_globals,app_name,app_version)


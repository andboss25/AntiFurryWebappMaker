import lupa
import WebSEngine

class LuaRunner:
    def __init__(self,handler_instance):
        self.env = lupa.LuaRuntime()
        self.env.globals()["RequestHandler"] = handler_instance
        self.env.globals()["RequestHandlerMethods"] = WebSEngine.RequestHandlerMethods
    
    def AddGlobals(self,lua_globals:dict):
        for lua_global in lua_globals:
            self.env.globals()[lua_global] = lua_globals[lua_global]

    def RunLuaMain(self,file_path:str):
        self.env.execute(open(file_path,"r").read())
        return self.env.globals().main
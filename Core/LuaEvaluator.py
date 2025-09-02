import lupa
from pathlib import Path
import importlib
import sys

from Core import WebSEngine


# Some libraries id like the user to be able to use in Lua

class LuaRunner:
    def __init__(self,handler_instance):
        self.env = lupa.LuaRuntime()
        self.env.globals()["RequestHandler"] = handler_instance
        self.env.globals()["RequestHandlerMethods"] = WebSEngine.RequestHandlerMethods
        
        # Declare Libs
        general_pathlist = Path(f"{handler_instance.lua_module_path}").rglob("*.py")

        for file in general_pathlist:
            spec = importlib.util.spec_from_file_location(file.stem, str(file))
            module = importlib.util.module_from_spec(spec)

            if spec and spec.loader:
                spec.loader.exec_module(module)
            else:
                raise ImportError(f"Failed to load wrapper: {file}")

            if hasattr(module, "exports"):
                self.AddGlobals({file.stem: module.exports})
            else:
                self.AddGlobals({file.stem: module})

    def AddGlobals(self,lua_globals:dict):
        for lua_global in lua_globals:
            self.env.globals()[lua_global] = lua_globals[lua_global]

    def RunLuaMain(self,file_path:str):
        self.env.execute(open(file_path,"r").read())
        return self.env.globals().main
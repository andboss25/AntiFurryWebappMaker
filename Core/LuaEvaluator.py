import lupa
import WebSEngine

# Some libraries id like the user to be able to use in Lua

import os
import sys
import io
import platform
import subprocess

import json
import xml

import random
import math

class LuaRunner:
    def __init__(self,handler_instance):
        self.env = lupa.LuaRuntime()
        self.env.globals()["RequestHandler"] = handler_instance
        self.env.globals()["RequestHandlerMethods"] = WebSEngine.RequestHandlerMethods

        # Declare Libs
        self.env.globals()["OS_LIB"] = os
        self.env.globals()["SYS_LIB"] = sys
        self.env.globals()["IO_LIB"] = io
        self.env.globals()["PLATFORM_LIB"] = platform
        self.env.globals()["SUBPROCESS_LIB"] = subprocess

        self.env.globals()["JSON_LIB"] = json
        self.env.globals()["XML_LIB"] = xml

        self.env.globals()["RANDOM_LIB"] = random
        self.env.globals()["MATH_LIB"] = math
    
    def AddGlobals(self,lua_globals:dict):
        for lua_global in lua_globals:
            self.env.globals()[lua_global] = lua_globals[lua_global]

    def RunLuaMain(self,file_path:str):
        self.env.execute(open(file_path,"r").read())
        return self.env.globals().main
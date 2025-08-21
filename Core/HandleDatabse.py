
import sqlite3

import WebSEngine

class Database:
    def __init__(self,db_globals):
        self.db_globals = db_globals
        self.database_connection = sqlite3.connect(self.db_globals["DB_FILEPATH"],check_same_thread=False)
        self.database_connection.autocommit = True

        for script in self.db_globals["DB_INITIALQUERY_PATHS"]:
            self.ExecuteScript(script)
        
    def Execute(self, query: str, params = None) -> sqlite3.Cursor:
        if WebSEngine.Helpfull.IsLuaTable(params):
            params = WebSEngine.Helpfull().LuaToPython(params)
        

        if params is None:
            return self.database_connection.execute(query)
        else:
            return self.database_connection.execute(query, params)
    
    def ExecuteScript(self,filepath) -> sqlite3.Connection:
        with open(filepath,"r") as f:
            query = f.read()
            f.close()
            return self.database_connection.execute(query)
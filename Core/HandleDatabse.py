
import sqlite3

import WebSEngine

class Database:
    def __init__(self,db_globals):
        self.db_globals = db_globals
        self.database_connection = sqlite3.connect(self.db_globals["DB_FILEPATH"],check_same_thread=False)
        self.database_connection.autocommit = True
        self.database_logfile = open(self.db_globals["DB_LOGPATH"],"a+", encoding='utf-8')
        self.database_logfile.write("Database Connection Created 👋\n")
        self.database_logfile.close()

        for script in self.db_globals["DB_INITIALQUERY_PATHS"]:
            self.ExecuteScript(script)
        
    def Execute(self, query: str, params = None) -> sqlite3.Cursor:
        if WebSEngine.Helpfull.IsLuaTable(params):
            params = WebSEngine.Helpfull().LuaToPython(params)

        self.database_logfile = open(self.db_globals["DB_LOGPATH"],"a+", encoding='utf-8')
        self.database_logfile.write(f"Executing '{query}' with params '{str(params)}' ⚙️\n")
        self.database_logfile.close()

        try:
            if params is None:
                return self.database_connection.execute(query)
            else:
                return self.database_connection.execute(query, params)
        except Exception as e:
            self.database_logfile = open(self.db_globals["DB_LOGPATH"],"a+", encoding='utf-8')
            self.database_logfile.write(f"Failed to execute '{query}' with params '{str(params)}' : '{str(e)}' ❌\n")
            self.database_logfile.close()
            raise e
    
    def ExecuteScript(self,filepath) -> sqlite3.Connection:
        self.database_logfile = open(self.db_globals["DB_LOGPATH"],"a+", encoding='utf-8')
        self.database_logfile.write(f"Executing script '{filepath}' ⚙️\n")
        self.database_logfile.close()
        try:
            with open(filepath,"r") as f:
                query = f.read()
                f.close()
                return self.database_connection.executescript(query)
        except Exception as e:
            self.database_logfile = open(self.db_globals["DB_LOGPATH"],"a+", encoding='utf-8')
            self.database_logfile.write(f"Failed to execute script '{filepath}' : '{str(e)}'  ❌\n")
            self.database_logfile.close()
            raise e

from Core import WebSEngine
from Core import RepresentEndpoints
from Core import HandleDatabse
from Core import ParseModelFile

import sys
import os

if "--serve" in sys.argv:
    index_of_argument = sys.argv.index("--serve")
    try:
        address = sys.argv[index_of_argument + 1]
        address = address.split(":")
        ip = address[0]
        port = address[1]
    except:
        print("Ip and port was not specified!")
        ip = "127.0.0.1"
        port = 80

    try:
        r = ParseModelFile.Reader(os.path.join(os.getcwd(),"Models","model.json"))
    except:
        raise Exception("Error reading model file!")
    
    try:
        app = r.ParseToApp()
    except:
        raise Exception("Error parsing model file!")
    try:
        db = HandleDatabse.Database(app.app_globals)
    except:
        raise Exception("Error generating database!")
    
    try:
        WebSEngine.RequestHandler.SetPaths(os.path.join(os.getcwd(),"Plugins","LuaModules"),os.path.join(os.getcwd(),"Plugins","CustomChecks"))
        rep = RepresentEndpoints.Briger(app)
        rep.Represent(db)
    except:
        raise Exception("Error representing app!")
    
    try:
        s = WebSEngine.Server(int(port),ip)
        print(f"Serving app on http://{ip}:{port}")
        s.Serve()
    except KeyboardInterrupt:
        print("Stopping app!")
    except:
        raise Exception("Error serving app!")
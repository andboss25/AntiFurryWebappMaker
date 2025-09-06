
from Core import WebSEngine
from Core import RepresentEndpoints
from Core import HandleDatabse
from Core import ParseModelFile

import sys
import os
import json
import shutil

if "--help" in sys.argv or "-h" in sys.argv:
    print("List of arguments:")
    print("--serve <ip>:<port> = serve the current application")
    print("--new-app <name (no spaces)> = create a new application")

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
        r = ParseModelFile.Reader(os.path.join(os.getcwd(),"model.json"))
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
    
if "--new-app" in sys.argv:
    index_of_argument = sys.argv.index("--new-app")
    try:
        name = sys.argv[index_of_argument + 1]
    except:
        raise Exception("Name not specified!-")
    
    print(f"Making a new application '{name}'...")
    os.mkdir(name)
    os.mkdir(os.path.join(name,"DB"))
    os.mkdir(os.path.join(name,"Logs"))
    open(os.path.join(name,"DB","init.sql"),"w").close()
    model_file = open(os.path.join(name,"model.json"),"w")
    model_file.write(json.dumps(
        {
            "app-info":{
                "name":name,
                "version":1.0
            },
            "globals":{
                "DB_FILEPATH":os.path.join("DB","database.db"),
                "DB_LOGPATH":os.path.join("Logs","DB_LOG.log"),
                "DB_INITIALQUERY_PATHS":[os.path.join("DB","init.sql")]
            },
            "points":{
                "/":{
                    "checks":{
                        "allowed-methods":["GET"]
                    },
                    "children":{},
                    "type":"Page",
                    "name":"Home Page",
                    "prop":{
                        "source-page":"Resources\\index.html"
                    }
                },
                "scriptable":{
                    "checks":{
                        "allowed-methods":["GET"]
                    },
                    "children":{},
                    "type":"Endpoint",
                    "name":"Scripted This",
                    "prop":{
                        "scriptable":True,
                        "script-path":"Scripts\\scriptable.lua"
                    }
                }
            },
            "special-points":{
                "hascode 404;":{
                    "children":{},
                    "type":"Endpoint",
                    "name":"Code 404",
                    "prop":{
                        "scriptable":False,
                        "set-response":"<h1>404 Page not found</h1>",
                        "set-response-type":"text/html",
                        "set-response-code":404
                    }
                }
            }
        },indent=3
    ))
    model_file.close()
    shutil.copytree(
        os.path.join(os.path.dirname(os.path.abspath(__file__)),"Plugins"),
        os.path.join(name,"Plugins")
    )
    os.mkdir(os.path.join(name,"Resources"))
    f = open(os.path.join(name,"Resources","index.html"),"w")
    f.write('<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<title>Prebuild Document</title>\n</head>\n<body>\n<h1>Your af-webapp maker project was generated!\n</h1>\n</body>\n</html>')
    f.close()
    os.mkdir(os.path.join(name,"Scripts"))
    f = open(os.path.join(name,"Scripts","scriptable.lua"),"w")
    f.write('function main()\nRequestHandlerMethods.SendPlainResponse(RequestHandler,"This string came from a preconfigured script that you can modify, glory to antifurry!",200)\n end')
    f.close()

import datetime
import json
import random
import base64
import WebSEngine

class exports:
    class Token():
        def __init__(self,userid,type,props={}):
            self.userid = userid
            self.type = type
            self.token = None
            self.props = WebSEngine.Helpfull().LuaToPython(props)

        def AssignTokenObj(self):
            WebSEngine.RequestHandler.db.Execute("UPDATE users SET token=? WHERE id=?",(self.token,self.userid,))
        
        def AssignToken(token,userid):
            WebSEngine.RequestHandler.db.Execute("UPDATE users SET token=? WHERE id=?",(token,userid,))
        
        def InvalidateTokenObj(self):
            WebSEngine.RequestHandler.db.Execute("UPDATE users SET token=NULL WHERE token=?",(self.token,))
                
        def InvalidateToken(token):
            WebSEngine.RequestHandler.db.Execute("UPDATE users SET token=NULL WHERE token=?",(token,))
        
        def IsValidTokenObj(self):
            if WebSEngine.RequestHandler.db.Execute("SELECT * FROM users WHERE token=?",(self.token,)).fetchone() is not None:
                return True
            
            return False
        
        def IsValidToken(token:str = ""):
            if WebSEngine.RequestHandler.db.Execute("SELECT * FROM users WHERE token=?",(token,)).fetchone() is not None:
                return True
            
            return False
        
        def GetUserFromToken(token:str = ""):
            return WebSEngine.RequestHandler.db.Execute("SELECT * FROM users WHERE token=?",(token,)).fetchone()
        
        def GetUserFromTokenObj(self):
            return WebSEngine.RequestHandler.db.Execute("SELECT * FROM users WHERE token=?",(self.token,)).fetchone()

        def GenerateToken(self,assign=True):
            unix_time = datetime.datetime.now().timestamp() * 1000

            match (self.type):
                case 'JB64':
                    self.token = json.dumps({
                        "secret": str(random.randint(1_000_000,9_999_999))
                        ,"ts": str(unix_time)
                        , "props":self.props
                    })
                    self.token = base64.b64encode(self.token.encode())
                case 'JB85':
                    self.token = json.dumps({
                        "secret": str(random.randint(1_000_000,9_999_999))
                        ,"ts": str(unix_time)
                        ,"props":self.props
                    })
                    self.token = base64.b85encode(self.token.encode())
                case 'UJB64':
                    self.token = json.dumps({
                        "secret": str(random.randint(1_000_000,9_999_999))
                        ,"ts": str(unix_time)
                        ,"props":self.props
                    })
                    self.token = base64.urlsafe_b64encode(self.token.encode())
                case _:
                    raise Exception("Invalid token type provided!")
                
            self.token = self.token.decode()
            
            if assign == True:
                self.AssignTokenObj()

            return self.token

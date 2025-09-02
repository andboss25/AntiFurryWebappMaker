
import requests

class exports:
    def CheckResponseToken(secret_key,response_token):
        r = requests.post("https://www.google.com/recaptcha/api/siteverify",data={
            "secret":secret_key,
            "response":response_token
        })

        json = r.json()
        return json.get("success",False)
import requests

class exports:
    def GET(url: str, provided_params: dict = None, headers: dict = None):
        if provided_params is None:
            provided_params = {}
        if headers is None:
            headers = {}
        rq = requests.get(url, params=provided_params, headers=headers)
        return rq

    def POST(url: str, data: dict = None, headers: dict = None):
        if data is None:
            data = {}
        if headers is None:
            headers = {"Content-Type": "application/json; charset=utf-8"}
        rq = requests.post(url, json=data, headers=headers)
        return rq

    def PUT(url: str, data: dict = None, headers: dict = None):
        if data is None:
            data = {}
        if headers is None:
            headers = {"Content-Type": "application/json; charset=utf-8"}
        rq = requests.put(url, json=data, headers=headers)
        return rq
    
    def PATCH(url: str, data: dict = None, headers: dict = None):
        if data is None:
            data = {}
        if headers is None:
            headers = {"Content-Type": "application/json; charset=utf-8"}
        rq = requests.patch(url, json=data, headers=headers)
        return rq

    def DELETE(url: str, provided_params: dict = None, headers: dict = None):
        if provided_params is None:
            provided_params = {}
        if headers is None:
            headers = {}
        rq = requests.delete(url, params=provided_params, headers=headers)
        return rq

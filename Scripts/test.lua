
function main()
    print(Requests.GET('https://httpbin.org/ip').json()['origin'])
    RequestHandlerMethods.SendHtmlResponse(RequestHandler,'hh',200)
end
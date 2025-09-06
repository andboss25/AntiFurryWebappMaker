The AFWAM project works in this way:

Every project has a model file that contains a strcutre with
`app-info => name and version`,`globals => global files for apis`,`points => endpoints`,`special-points => special points curently only hascode404; (404 page)`

This file has refrences to toher files like scripts pages and images

Then it gets hosted and dynamic scriptable endpoints are run when accessed and static ones just host files and responses

Checks are also run before the endpoints get accessed/run , if one fails then the user cannot access that endpoint!

Scripts also refrence modules inside them and request parameters!

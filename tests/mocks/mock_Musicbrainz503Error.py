from musicbrainz2.webservice import WebServiceError


def getArtists(*args, **kwargs):
    raise WebServiceError("503")


def getReleaseGroups(*args, **kwargs):
    raise WebServiceError("503")


def getTracks(*args, **kwargs):
    raise WebServiceError("503")


def getReleaseGroupById(*args, **kwargs):
    raise WebServiceError("503")


def getArtistById(*args, **kwargs):
    raise WebServiceError("503")


def getReleaseById(*args, **kwargs):
    raise WebServiceError("503")


def inject_mocks(module):
    """Injects mock functions into musicbrainz library"""
    assert module.__name__ == 'r3tagger.query.Musicbrainz'

    funcs = {'getArtists': getArtists,
             'getReleaseGroups': getReleaseGroups,
             'getTracks': getTracks,
             'getReleaseGroupById': getReleaseGroupById,
             'getArtistById': getArtistById,
             'getReleaseById': getReleaseById}

    for name, func in funcs.items():
        setattr(module.ws.Query, name, func)
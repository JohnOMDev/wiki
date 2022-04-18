import suds.cache
class DisableSUDSCache(suds.cache.NoCache):
    def __init__(self, location=None, **duration):
        pass  #No cache logic
suds.cache.ObjectCache = DisableSUDSCache

from . import src
from . import app
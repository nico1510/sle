class FsmParseException(Exception):
    # Base class for all OkFSM exceptions
    pass

class OkFsmException(Exception):
    # Base class for all OkFSM exceptions
    pass

class DistinctIdsException(OkFsmException):
    pass

class SingleInitialException(OkFsmException):
    pass

class DeterministicException(OkFsmException):
    pass

class ResolvableException(OkFsmException):
    pass

class ReachableException(OkFsmException):
    pass

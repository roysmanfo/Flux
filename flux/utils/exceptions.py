"""
General Flux exceptions
"""


class FluxException(Exception):
    """
    Base exception for all Flux exeptions,
    use this class in your except block to catch any exception thrown by Flux
    """
    pass



class FluxIllegalOverwrite(FluxException, TypeError):
    """
    A method that was marked as `prevent_overwrite` has been
    redeclared in a subclass
    """


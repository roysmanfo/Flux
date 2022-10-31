"""
Necessary procedures to prepare the program to work
as intended.
"""

def setup(user, path) -> tuple:
    """
    ## Setup process

    This process retrives all data necessary to start using Cristal, like
    User setings, file locations on the disk, etc.

    This process makes it easier to start Cristal as we just need to call this
    function in the main file and everything will be handled automaticly. 

    @param user : The user class from the info file in settings
    @param path : The path class from the info file in settings
    """
    from os import chdir
    USER = user()
    PATH = path(USER, load_data=True)
    chdir(PATH.terminal)
    return (USER, PATH)

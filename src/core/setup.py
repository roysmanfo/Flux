"""
Necessary procedures to prepare the program to work
as intended.
"""


def setup(user: object) -> tuple:
    """
    ## Setup process

    This process retrives all data necessary to start using Cristal, like
    User setings, file locations on the disk, etc.

    This process makes it easier to start Cristal as we just need to call this
    function in the main file and everything will be handled automaticaly. 

    @param user : The user class from the info file in settings
    """
    from os import chdir
    USER = user()
    chdir(USER.paths.terminal)
    return USER

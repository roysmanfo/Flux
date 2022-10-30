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

    USER = user()
    PATH = path(USER, load_data=True)

    return (USER, PATH)

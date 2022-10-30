def setup():
    """
    ## Setup process
    
    This process retrives all data necessary to start using Cristal, like
    User setings, file locations on the disk, etc.

    This process makes it easier to start Cristal as we just need to call this
    function in the main file and everything will be handled automaticly. 
    """
    from settings.info import User, Path
    
    USER = User()
    PATH = Path(USER, load_data=True)


setup()

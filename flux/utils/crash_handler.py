import datetime
import tempfile
import traceback
from typing import List, Optional, Tuple, Union

try:
    from flux.settings.settings import SysPaths
    LOG_PATH = str(SysPaths.LOGS_FOLDER)
except ImportError:
    # in case that the problem is there we should be able to adapt to this
    LOG_PATH = tempfile.gettempdir()


def write_error_log(
        fileprefix: Optional[str] = None,
        error_log: Optional[Union[str, List[str]]] = None,
        title: Optional[str] = None
    ) -> Tuple[int, str]:

    """

    Params
    -------
    - fileprefix:       the prefix of the .log filename (default: Flux_log_{datetime}_)
    - error_log:        the full error log (default: python default Traceback)
    - title:            the title to put at the start of the error file (default: current_time)


    Returns
    -------
    A tuple containing the file descriptor and file path to the error log file
    (int, str)
    """

    title = title or datetime.datetime.now().ctime()
    date = "_".join(title.replace(":", "_").split())
    fd, tmp = tempfile.mkstemp(".log", fileprefix or f"Flux_log_{date}__", dir=LOG_PATH, text=True)
    
    with open(tmp, 'wt') as log:
        log.write(title + f"\n{'=' * len(title)}" + "\n\n")
        traceback_str = error_log or traceback.format_exc()
        if isinstance(traceback_str, str):
            log.write(traceback_str)
            log.write("\n")
        else:
            log.writelines(traceback_str)


    # print("The full traceback of this error can be found here: \n" + tmp + "\n")
    return (fd, tmp)

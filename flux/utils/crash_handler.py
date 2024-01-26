import datetime
import tempfile
import traceback

def write_error_log(
        fileprefix: str | None = None,
        error_log: str | list[str] | None = None,
        title: str | None = None) -> tuple[int, str]:
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
    fd, tmp = tempfile.mkstemp(".log", fileprefix or f"Flux_log_{date}__", None, text=True)
    
    with open(tmp, 'w') as log:
        log.write(title + f"\n{'=' * len(title)}" + "\n\n")
        traceback_str = error_log or traceback.format_exc()
        if isinstance(traceback_str, str):
            log.write(traceback_str)
            log.write("\n")
        else:
            log.writelines(traceback_str)


    # print("The full traceback of this error can be found here: \n" + tmp + "\n")
    return (fd, tmp)

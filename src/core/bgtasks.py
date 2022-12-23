"""
## bgtasks (Background Tasks)

Handles all background tasks executed on start of the program
"""

# List of all background tasks
# When one of these tasks is added to the list of background tasks, it's command gets 
# suppressed and is ignored if executed by the user, as it is already running. 
BG_TASKS: list[str] = [
    'observer',
]
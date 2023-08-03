
class Namespace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class ParserInterface():
    """
    Interface for argument parsing.

    Works kinda like argparse but excluding its default behaviours
    like exiting the program on the firs parsing error.
    """

    def __init__(self, description=''):
        self._description = description
        self._arguments = []

    def add_argument(self, name, **kwargs):
        self._arguments.append((name, kwargs))

    def parse_args(self, args=None):
        # Split the arguments manually if args is not provided
        if args is None:
            import sys
            args = sys.argv[1:]

        parsed_args = {}
        i = 0
        while i < len(args):
            arg = args[i]
            if arg.startswith('-'):
                try:
                    name, value = arg, None
                    if '=' in arg:
                        name, value = arg.split('=', 1)
                        value = value.strip()
                    elif i + 1 < len(args) and not args[i + 1].startswith('-'):
                        value = args[i + 1]
                        i += 1
                    for arg_name, arg_kwargs in self._arguments:
                        if name == arg_name or arg_name in arg_kwargs.get('aliases', []):
                            if 'action' in arg_kwargs and arg_kwargs['action'] == 'store_true':
                                parsed_args[arg_name] = True
                            else:
                                parsed_args[arg_name] = value
                            break
                    else:
                        raise ValueError(f"Unrecognized argument: {arg}")
                except Exception as e:
                    raise ValueError(f"Error parsing argument: {arg}\n{e}")
            else:
                raise ValueError(f"Unexpected value: {arg}")

            i += 1

        # Additional validation or default values can be added here
        return Namespace(**parsed_args)


    def help() -> None:
        """
        Display the help message
        """
        ...
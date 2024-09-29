# Create your first command

In this tutorial you will learn how to create a new command in flux.  
We will create a command that counts from 0 up to N, where N is given by the user.

Let's define the usage string:
```sh
count LIMIT [STEP]
```
Basically the command `count` has takes a required parameter `LIMIT` and an optional parameter `STEP` that we will define later.

## Create basic structure

Let's start by importing the [`CommandInterface`](./flux_api.md#the-classes-command-and-commandinterface) and [`Parser`](./flux_api.md#parser) classes
and creating the entry point of our command
```py
from flux.core.helpers.commands import (
    CommandInterface,
    Parser
)

# we can specify the entry point of the command
# by setting the ENTRY_POINT register to the name of the class
# that inherits CommandInterface
ENTRY_POINT = "Count"

class Count(CommandInterface):
    pass
```

## Create the parser
Now we can create the parser to get all the needed informations that our
command will need
```py
class Count(CommandInterface):
    def init(self) -> None:
        self.parser = Parser(
            prog="count",
            usage="count LIMIT [STEP]",
            description="count from 0 up to N"
        )

        self.parser.add_argument("LIMIT", type=int, help="upper limit of our counter")

        # the step size is optional, so we can set nargs to "?" (0 or 1 values)
        self.parser.add_argument("STEP", nargs="?", default=1, type=int, help="step size of our counter (default: 1)")

```

if we now run our command with the `-h` flag (`count -h`) we get this help message
```
usage: count LIMIT [STEP]

count from 0 up to N

positional arguments:
  LIMIT       upper limit of our counter
  STEP        step size of our counter (default: 1)

options:
  -h, --help  show this help message and exit
```


> [!NOTE]
> By default `Parser` also creates an help message and adds the arguments `-h`
> and `--help` to our command unless we specify otherwise: `self.parser = Parser(add_help=False, ...)`

## Create the rest of the command
We now need to implement the actuall code that will count up to our LIMIT.

This part needs to be implemented in the [`run()`](./flux_api.md#run) method because we want to execute the rest of the command only if there are no parsing errors.   
(those are detected in the [`setup()`](flux_api.md#setup) method, which will prevent us to call [`run()`](./flux_api.md#run))

```py
def run(self) -> None:
    for n in range(0, self.args.LIMIT, self.args.STEP):
        self.print(n)
```
The parsed arguments can be found in [`self.args`](./flux_api.md#general-attributes) and can be accessed just by placing a dot followed be the name of the argument

Instead of using python's `print()` function, we will use [`self.print()`](flux_api.md#print).  
This method will allow us not to worry about output redirection in cases when
our command is used like this
```
count 100 > numbers.txt
```

## Handling errors
We are almost done, but we did't take into consideration keyboard interrupts (or SIGINT), so with large numbers, if the user presses `ctrl+c`, the command 
will crash and [generate a crash log](./flux_api.md#fail_safe).

We can try and solve this with a simple try-except block
```py
def run(self) -> None:
    try:
        # we add 1 to limit to print it on screen too
        for n in range(0, self.args.LIMIT+1, self.args.STEP):
            self.print(n)
    except KeyboardInterrupt:
        # exit safely
        pass

```
but the interpreter will just keeps going.

To solve cases like this, we can use [interrupts](flux_api.md#register_interrupt).

Let's modify our code accordingly

```py
# modify the imports to include the EventTriggers enum
# containing all supported interrupts
from flux.core.helpers.commands import (
    CommandInterface,
    Parser,
    EventTriggers
)
```
outside the `Command` class we can create a flag and a funtion to set the flag
```py
# create a global flag that will signal to stop the loop 
stop = False

def stop_counting(signum, frame, *args):
    # request to exit
    global stop
    stop = True
```

now inside the `Command` class we can modify our code to stop the
loop
```py
def init(self) -> None:
    ...

    # add our interrupt to the ones controlled by Flux
    # will be automatically deleted after the command exits  
    self.register_interrupt(
        event=EventTriggers.SIGINT,
        target=stop_counting
    )

def run(self) -> None:
    for n in range(0, self.args.LIMIT+1, self.args.STEP):
        # check if the interrupt has been called
        if self.stop:
            break
        self.print(n)
```
and now we are done, you can use your new `count` command inside Flux

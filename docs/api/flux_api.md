# Flux API

- [What is the Flux API](#what-is-the-flux-api)
- [The classes Command and CommandInterface](#the-classes-command-and-commandinterface)
  - [Automatic Calls](#automatic-calls)
    - [init()](#init)
    - [setup()](#setup)
    - [run()](#run)
    - [close()](#close)
    - [exit()](#exit)
    - [fail_safe()](#fail_safe)
  - [General Attributes](#general-attributess)
  - [Helper Methods](#helper-methods)
    - [input()](#input)
    - [print()](#print)
    - [printerr()](#printerr)
    - [get_level_name()](#get_level_name)
    - [get_level_val()](#get_level_val)
    - [register_interrupt()](#register_interrupt)
    - [unregister_interrupt()](#unregister_interrupt)
    - [clear_interrupts()](#clear_interrupts)
  - [Logging Method](#logging-methods)
    - [critical()](#critical)
    - [fatal()](#fatal)
    - [error()](#error)
    - [warning()](#warning)
    - [info()](#info)
    - [debug()](#debug)
  - [Parser](#parser)
  - [Properties](#properties)

## What is the Flux API

The Flux API is a collection of classes and methods that allow to
interract with the rest of the system.  
As a developer the most important part of it is the [CommandInterface](#the-classes-command-and-commandinterface)
that is the most important thing about any command as without it
the program won't even get loaded and executed.

## The classes Command and CommandInterface

This is the first thing that the Flux loader will look for.
In any command you develop, you shoud create a `Command` class that extends
the `CommandInterface`.

```py

class Command(CommandInterface):
  ...

  def run(self):
    # the run method MUST be implemented

```

> [!NOTE]  
> The name of the class that implements `CommandInterface` can be modifid
> if you set the register `ENTRY_POINT` to a different name

Every command that uses this interfacer is equiped with the standard methods to work on the app.  
Every single command should use this class to keep a consistent standard.

### Automatic Calls

Methods that get called regardless by the terminal

#### `init()`

This function is called on start of execution
This method should be used to do setup operations (like create the Parser)

#### `setup()`

This is function is called right before run()
This method is used to parse arguments and exit on parsing errors

> Always remember to call `super().setup()` when overwriting this method  
> It will handle the parsing part and exiting on parsing errors

#### `run()`

This is the core method for the command.  
This method should be used to do all the main operations of the command

> If this method has not been implemented, the command will NOT be executed

#### `close()`

This is the method that gets called right after run() the command  
This method is used to close open files, like a redirected stdout

> Always remember to call `super().close()` when overwriting this method  
> It will close any resource opened by Flux and allow for a safe exit.  
> It will NOT close any resource opened by your command.

#### `exit()`

This is the last method that gets called  
This method should be used to define what status code to return

> Always remember to call `super().exit()` when overwriting this method

#### `fail_safe()`

This method gets called to capture unhandled exception.  
This method may be called at any time, and once called command execution will be terminated without
calling `self.close()` or `self.exit()`

By default creates a crash report with all the Traceback informations
and sets `self.status` to `STATUS_ERR`

The execution flow in pseudo code looks something like this

```
    try to execute the command
        init()
        setup()

        is the status=STATUS_ERR or is parser.exit_execution = True ?
            // parsing error, close and exit
            close()
            status = exit()
            return status

        run()
        close()
        exit()

    any uncaught exception ?
        // create a crash log
        // and exit safely
        fail_safe(exception)

    // the status is used by flux internally,
    // if there has been no error the default status is STATUS_OK
    return the status
```

### General Attributes

Attributes shared by commands

| name       | type                | description                                                                                                |
| ---------- | ------------------- | ---------------------------------------------------------------------------------------------------------- |
| IS_PROCESS | (const, bool)       | Whether or not the command is being runned as a background thread                                          |
| PRIVILEGES | (const, Privileges) | The privileges given to the user to execute the current command [LOW / HIGH / SYSTEM]                      |
| system     | variable, System    | A reference to the instance of the System class, containing all the most important informations about flux |
| settings   | variable, Settings  | A reference to the instance of the Settings class, containing user settings and system paths (SysPaths)    |
| line_args  | variable, list[str] | The full command typed by the user (also contains the command name, es. ['ls', 'some_path'])               |
| status     | variable, int       | The return code of the command (default statuses follow the following convention 'STATUS\_[err/ok/warn]' ) |
| stdout     | variable, TextIO    | The stdout of the command                                                                                  |
| stderr     | variable, TextIO    | The stderr of the command                                                                                  |
| stdin      | variable, TextIO    | The stdin of the command                                                                                   |
| parser     | variable, Parser    | A program targeted implementation of argparse.ArgumentParser                                               |
| args       | variable, Namespace | The usual output returned by ArgumentParser.parse_args                                                     |
| errors     | variable, Errors    | Standardized error/warning messages                                                                        |
| colors     | variable, Colors    | Colors for command output, does not have effect outside terminal                                           |
| levels     | variable, Levels    | All the log levels available                                                                               |
| log_level  | variable, int       | Only logs wit higher severity than this number will be displayed (displays everything by default)          |

### Helper Methods

Other usefull methods, NOT called by the terminal.
If you want to use these methods you need to call them yourself.
(print() and printerr() are not affected by the log_level, but are still to output redirection)

#### `input()`

This is similar to python's `input()`, but uses `self.stdin` and instead of `sys.stdin` .

#### `print()`

This is similar to python's `print()`, but uses `self.stdout` and instead of `sys.stdout` .

#### `printerr()`

This is similar to `self.print()`, but uses `self.stderr` instead.

#### `get_level_name()`

Returns the level's name based on value

#### `get_level_val()`

Returns the level's value based on it's name

#### `register_interrupt()`

Register a new interrupt handler

#### `unregister_interrupt()`

Unregister an interrupt handler

#### `clear_interrupts()`

Unregisters all interrupts

### Logging Methods

These methods work like in the logging module, where only logs with a certain severity are displayed (log_level)

#### `critical()`

This method should be called once a critical error accoures.

#### `fatal()`

This mathod should be called once a fatal error accoures.

#### `error()`

This mathod should be called once an error accoures.

#### `warning()`

This mathod should be called to issue warnings.

#### `info()`

This mathod should be called for providing the end user with some info.

#### `debug()`

This mathod should be called for debugging.

### Parser

Every command will need some form of line argment parsing, and this is where the `Parser`
class comes handy.

It is an adaptation of `argparse.ArgumentParser` that has been extended and designed around
Flux and also comes with some handy methods and properties.

It works kinda like argparse but excluding its default behaviours
like exiting the program on the first parsing error.

You can create a new parser in the init method

```py
# look for the Counter class instead of Command
ENTRY_POINT="Counter"

class Counter(CommandInterface):
  def init(self):
    self.parser = Parser(
      prog="counter",
      description="count up to N",
      usage="counter LIMIT [STEP]"
    )
    # add the arguments
    parser.add_argument("LIMIT", type=int, help="stop counting when reaching this number")
    # set STEP as an optional argument
    parser.add_argument("STEP", nargs"?", type=int, default=1, help="size of a single step")

  def run(self):
    # setup() will parse self.line_args and store the result in self.args
    # If there are parsing errorsa the command will exit with an error
    for i in range(0, args.LIMIT, args.STEP):
      self.print(i)

```

### Properties

Other usefull informations about the state of the command

| Return type | name                  | description                                                               |
| ----------- | --------------------- | ------------------------------------------------------------------------- |
| `bool`      | `redirected_stdout()` | True when the stdout has been redirected                                  |
| `bool`      | `redirected_stderr()` | True when the stderr has been redirected                                  |
| `bool`      | `redirected_stdin()`  | True when the stdin has been redirected                                   |
| `bool`      | `is_output_red()`     | True when the stdout and stderr have been redirected                      |
| `bool`      | `is_any_red()`        | True when at least one among stdout, stderr and stdin has been redirected |
| `bool`      | `is_all_red()`        | True when stdout, stderr and stdin have been redirected                   |
| `bool`      | `is_alive()`          | True from when the commaand gets loaded to after exit() or fail_safe()    |
| `bool`      | `has_high_priv()`     | True if the command has been run with high/system privileges              |
| `bool`      | `has_sys_priv()`      | True if the command has been run with system privileges                   |
| `bool`      | `ihandles()`          | Retuns a set of all interrupt handles                                     |
| `bool`      | `recv_from_pipe()`    | True if `self.stdin` is pointing to a `pipe`                              |
| `bool`      | `send_to_pipe()`      | True if `self.stdout` is pointing to a `pipe`                             |

# Flux API

- [What is the Flux API](#what-is-the-flux-api)
- [The classes Command and CommandInterface](#the-classes-command-and-commandinterface)
  - [Automatic Calls](#automatic-calls)
    - [init()](#init)
    - [setup()](#setup)
    - [run()](#run)
    - [close()](#close)
    - [exit()](#exit)
    - [fail_safe()](#fail_safe)
  - [General Attributes](#general-attributess)
  - [Helper Methods](#helper-methods)
    - [input()](#input)
    - [print()](#print)
    - [printerr()](#printerr)
    - [get_level_name()](#get_level_name)
    - [get_level_val()](#get_level_val)
    - [register_interrupt()](#register_interrupt)
    - [unregister_interrupt()](#unregister_interrupt)
    - [clear_interrupts()](#clear_interrupts)
  - [Logging Method](#logging-methods)
    - [critical()](#critical)
    - [fatal()](#fatal)
    - [error()](#error)
    - [warning()](#warning)
    - [info()](#info)
    - [debug()](#debug)
  - [Parser](#parser)
  - [Properties](#properties)

## What is the Flux API

The Flux API is a collection of classes and methods that allow to
interract with the rest of the system.  
As a developer the most important part of it is the [CommandInterface](#the-classes-command-and-commandinterface)
that is the most important thing about any command as without it
the program won't even get loaded and executed.

## The classes Command and CommandInterface

This is the first thing that the Flux loader will look for.
In any command you develop, you shoud create a `Command` class that extends
the `CommandInterface`.

```py

class Command(CommandInterface):
  ...

  def run(self):
    # the run method MUST be implemented

```

> [!NOTE]  
> The name of the class that implements `CommandInterface` can be modifid
> if you set the register `ENTRY_POINT` to a different name

Every command that uses this interfacer is equiped with the standard methods to work on the app.  
Every single command should use this class to keep a consistent standard.

### Automatic Calls

Methods that get called regardless by the terminal

#### `init()`

This function is called on start of execution
This method should be used to do setup operations (like create the Parser)

#### `setup()`

This is function is called right before run()
This method is used to parse arguments and exit on parsing errors

> Always remember to call `super().setup()` when overwriting this method  
> It will handle the parsing part and exiting on parsing errors

#### `run()`

This is the core method for the command.  
This method should be used to do all the main operations of the command

> If this method has not been implemented, the command will NOT be executed

#### `close()`

This is the method that gets called right after run() the command  
This method is used to close open files, like a redirected stdout

> Always remember to call `super().close()` when overwriting this method  
> It will close any resource opened by Flux and allow for a safe exit.  
> It will NOT close any resource opened by your command.

#### `exit()`

This is the last method that gets called  
This method should be used to define what status code to return

> Always remember to call `super().exit()` when overwriting this method

#### `fail_safe()`

This method gets called to capture unhandled exception.  
This method may be called at any time, and once called command execution will be terminated without
calling `self.close()` or `self.exit()`

By default creates a crash report with all the Traceback informations
and sets `self.status` to `STATUS_ERR`

The execution flow in pseudo code looks something like this

```
    try to execute the command
        init()
        setup()

        is the status=STATUS_ERR or is parser.exit_execution = True ?
            // parsing error, close and exit
            close()
            status = exit()
            return status

        run()
        close()
        exit()

    any uncaught exception ?
        // create a crash log
        // and exit safely
        fail_safe(exception)

    // the status is used by flux internally,
    // if there has been no error the default status is STATUS_OK
    return the status
```

### General Attributess

Attributes shared by commands

| name       | type                | description                                                                                                |
| ---------- | ------------------- | ---------------------------------------------------------------------------------------------------------- |
| IS_PROCESS | (const, bool)       | Whether or not the command is being runned as a background thread                                          |
| PRIVILEGES | (const, Privileges) | The privileges given to the user to execute the current command [LOW / HIGH / SYSTEM]                      |
| system     | variable, System    | A reference to the instance of the System class, containing all the most important informations about flux |
| settings   | variable, Settings  | A reference to the instance of the Settings class, containing user settings and system paths (SysPaths)    |
| line_args  | variable, list[str] | The full command typed by the user (also contains the command name, es. ['ls', 'some_path'])               |
| status     | variable, int       | The return code of the command (default statuses follow the following convention 'STATUS\_[err/ok/warn]' ) |
| stdout     | variable, TextIO    | The stdout of the command                                                                                  |
| stderr     | variable, TextIO    | The stderr of the command                                                                                  |
| stdin      | variable, TextIO    | The stdin of the command                                                                                   |
| parser     | variable, Parser    | A program targeted implementation of argparse.ArgumentParser                                               |
| args       | variable, Namespace | The usual output returned by ArgumentParser.parse_args                                                     |
| errors     | variable, Errors    | Standardized error/warning messages                                                                        |
| colors     | variable, Colors    | Colors for command output, does not have effect outside terminal                                           |
| levels     | variable, Levels    | All the log levels available                                                                               |
| log_level  | variable, int       | Only logs wit higher severity than this number will be displayed (displays everything by default)          |

### Helper Methods

Other usefull methods, NOT called by the terminal.
If you want to use these methods you need to call them yourself.
(print() and printerr() are not affected by the log_level, but are still to output redirection)

#### `input()`

This is similar to python's `input()`, but uses `self.stdin` and instead of `sys.stdin` .

#### `print()`

This is similar to python's `print()`, but uses `self.stdout` and instead of `sys.stdout` .

#### `printerr()`

This is similar to `self.print()`, but uses `self.stderr` instead.

#### `get_level_name()`

Returns the level's name based on value

#### `get_level_val()`

Returns the level's value based on it's name

#### `register_interrupt()`

Register a new interrupt handler

#### `unregister_interrupt()`

Unregister an interrupt handler

#### `clear_interrupts()`

Unregisters all interrupts

### Logging Methods

These methods work like in the logging module, where only logs with a certain severity are displayed (log_level)

#### `critical()`

This method should be called once a critical error accoures.

#### `fatal()`

This mathod should be called once a fatal error accoures.

#### `error()`

This mathod should be called once an error accoures.

#### `warning()`

This mathod should be called to issue warnings.

#### `info()`

This mathod should be called for providing the end user with some info.

#### `debug()`

This mathod should be called for debugging.

### Parser

Every command will need some form of line argment parsing, and this is where the `Parser`
class comes handy.

It is an adaptation of `argparse.ArgumentParser` that has been extended and designed around
Flux and also comes with some handy methods and properties.

It works kinda like argparse but excluding its default behaviours
like exiting the program on the first parsing error.

You can create a new parser in the init method

```py
# look for the Counter class instead of Command
ENTRY_POINT="Counter"

class Counter(CommandInterface):
  def init(self):
    self.parser = Parser(
      prog="counter",
      description="count up to N",
      usage="counter LIMIT [STEP]"
    )
    # add the arguments
    parser.add_argument("LIMIT", type=int, help="stop counting when reaching this number")
    # set STEP as an optional argument
    parser.add_argument("STEP", nargs"?", type=int, default=1, help="size of a single step")

  def run(self):
    # setup() will parse self.line_args and store the result in self.args
    # If there are parsing errorsa the command will exit with an error
    for i in range(0, args.LIMIT, args.STEP):
      self.print(i)

```

### Properties

Other usefull informations about the state of the command

| Return type | name                  | description                                                               |
| ----------- | --------------------- | ------------------------------------------------------------------------- |
| `bool`      | `redirected_stdout()` | True when the stdout has been redirected (ex. command > file.txt)         |
| `bool`      | `redirected_stderr()` | True when the stderr has been redirected (ex. command 2> file.txt)        |
| `bool`      | `redirected_stdin()`  | True when the stdin has been redirected  (ex. command < file.txt)         |
| `bool`      | `is_output_red()`     | True when the stdout and stderr have been redirected                      |
| `bool`      | `is_any_red()`        | True when at least one among stdout, stderr and stdin has been redirected |
| `bool`      | `is_all_red()`        | True when stdout, stderr and stdin have been redirected                   |
| `bool`      | `is_alive()`          | True from when the commaand gets loaded to after exit() or fail_safe()    |
| `bool`      | `has_high_priv()`     | True if the command has been run with high/system privileges              |
| `bool`      | `has_sys_priv()`      | True if the command has been run with system privileges                   |
| `bool`      | `ihandles()`          | Retuns a set of all interrupt handles                                     |
| `bool`      | `recv_from_pipe()`    | True if `self.stdin` is pointing to a `pipe`                              |
| `bool`      | `send_to_pipe()`      | True if `self.stdout` is pointing to a `pipe`                             |

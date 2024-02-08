# Contributing

If you are reading this file, it means you're intrested in the project
and want to know how to contribute.  
In this file you'll find some instructions and tips to start working on **Flux**.

## Setup

To start install python if you don't have it on your system yet.

### Install on Windows

You can install it straight from the [official website](https://https://www.python.org/downloads/) (*prefered option*)
or from the [Microsoft Store](https://apps.microsoft.com/store/search?&publisher=Python%20Software%20Foundation).  
It is suggested to add python to PATH during installation

### Install on Linux/MacOS
This command should work on debian based systems,
in alternative replace apt with your own package manager
```sh
$ sudo apt install python3
```
On MacOS instead of `apt` you should have `brew`

### After install
Make sure that your version is **3.8** or above.  
To check your python version, open your terminal and type the following command:

```sh
$ python --version
```

You should get an output like this:

```
Python 3.10.8
```

### Virtual environment

It is suggested to work on a virtual environment, in order to isolate the program from global modules (This makes it easier to move the source code across different PCs).

To do so, just execute the following commands in the project folder 

```sh
$ python3 -m venv venv
$ source ./venv/Scripts/activate # 'source' isn't needed on Windows
(venv) $ # virtulal environment activated
(venv) $ deactivate
$ # virtual environment deactivated
```

Next you will need to install the modules listed in the requirements file, with the following command

```
$ pip install -r requirements.txt
```

If in an update more modules are added to this file, you will need to to install those modules eather. You can use the same command.

### Run
To run the application, you will need to go in the src folder,
and execute `main.py` with 

```
python3 main.py
```
#### Note
With python 3.12 there are some problems with the thread handling, so you
should get a mesage notifying you of that if you use the command `python3 main.py stable` to run. Without the keyword `stable` you run in **unstable mode** which means that you run in a version where background processes and threads are not supported.



# Contributing
If you are reading this file, it means you're intrested in the project 
and want to know how to contribute.  
In this file you'll find some instructions and tips to start woirking on __Cristal__.

## Setup

To start install python if you don't have it on your system yet.
You can install it straight from the [official website](https://https://www.python.org/downloads/)
or from the [Microsoft Store](https://apps.microsoft.com/store/search?&publisher=Python%20Software%20Foundation).

Make sure thet your version is  __3.7__ or above.  
To check your python version, open your terminal and type the following command:
```
$ python --version
```
You should get an output like this:
```
Python 3.10.8
```
Next you will need to install the molules listed in the requirements file, with the following command
```
$ pip install -r requirements.txt
```
If in a PR more more modules are added to this file, you will need to to install those modules eather. You can use the same command.
### Tip
It is suggested to work on a virtual environment, in oorder to isolate the program from global modules (This makes it easier to move the source code across different PCs).

To do so, just execute the following command in the project folder
```
$ pip -m venv .
```
![logo](./img/logo.svg)

Flux is an extensible and cross-platform Unix-like terminal written in python that has many different commands built to help the user to manage many tasks.

## Run flux
To run flux you will need to have python installed (at least version 3.8, but a version >=3.10 is prefered)

### setup (only the first time)

**Linux**  
If you are using linux you can setup the system simply by executing `setup.sh`.  
You can decide to execute the commands manually, then here are the commands for setting up the system in both  and 
```sh
pip install virtualenv
python3 -m venv --prompt venv .venv
source ./.venv/bin/activate
pip install -r linux-requirements.txt
```
**Windows**
```bash
pip install virtualenv
python -m venv --prompt venv .venv
./.venv/Scripts/activate
pip install -r win-requirements.txt
```

### run

to run flux now you will need to move into the `flux` folder
and execute `main.py`

>   **NOTE**: Each time you will need to activate the virtual environment to execute `main.py`,
>   otherwise you will not have access to the dependencies you just installed 
    
**Linux**
```
cd flux && python3 main.py
```
**Windows**
```
cd flux; python main.py
```

## Contributing
If you want to start contributing, you'll need a good knowledge of the python language, 
and feel confortable when using it.  
You'll also need do have some experience with __packages__ and __json__ files in python.  
Fore more information check [CONTRIBUTING.md](CONTRIBUTING.md)
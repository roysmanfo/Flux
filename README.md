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
pip install -r linux-requirements.txt
```
**Windows**
```bash
pip install virtualenv
python -m venv --prompt venv .venv
pip install -r win-requirements.txt
```

### run

to run flux now you will need to activate the
created virtual environment and then move into the `flux` folder
to execute `main.py`

**Linux**
```
source ./.venv/bin/activate && cd flux && python3 main.py
```
**Windows**
```
./.venv/Scripts/activate; cd flux; python main.py
```

## Contributing
If you want to start contributing, you'll need a good knowledge of the python language, 
and feel confortable when using it.  
You'll also need do have some experience with __packages__ and __json__ files in python.  
Fore more information check [CONTRIBUTING.md](CONTRIBUTING.md)
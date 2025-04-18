![logo](./img/logo.svg)

Flux is an extensible and cross-platform Unix-like terminal written in python that has many different commands built to help the user to manage many tasks.

# Installing Flux
1. Clone the repository on your machine
```sh
git clone https://github.com/roysmanfo/Flux.git
```
2. Install Flux using pip
```sh
cd Flux; pip install .
```
3. Verify that the installation has been successfull by running the `flux`
command on your terminal

## Develop your own commands
Flux comes with many scripts for the most common tasks, but it also provides
an API to develop your own scripts and commands.

Read the docs regarding the [Flux API](./docs/api/flux_api.md).  
You can also find a guided tutorial on [how to create your first Flux command](./docs/api/first_command.md) 

## Develop Flux
To run Flux you will need to have python installed (at least version 3.8, but a version >=3.10 is prefered)

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

to run Flux now you will need to move into the `Flux` folder
and execute `main.py`

>   **NOTE**: Each time you will need to activate the virtual environment to execute `main.py`,
>   otherwise you will not have access to the dependencies you just installed 
    
**Linux**
```
cd Flux && python3 main.py
```
**Windows**
```
cd Flux; python main.py
```

## Contributing
If you want to start contributing, you'll need a good knowledge of the python language, 
and feel confortable when using it.  
You'll also need do have some experience with __packages__ and __json__ files in python.  
Fore more information check [CONTRIBUTING.md](CONTRIBUTING.md)
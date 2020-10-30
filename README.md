# SAM Chat Client
Comand line chat client for sam-chat-server

## Requirements
- python 3.8
- pipenv (optional)

## Setup
- using pipenv
```
# activate virtualenv
pipenv shell

# install dependencies
pipenv install

# deactivate virtual env
deactivate
exit
```
- using venv
```
# create virtual env
python3 -m venv venv

# activate virtual env
source venv/bin/activate

# install dependencies
pip install -r requirements.txt

# deactivate virtual env
deactivate
```

## Running locally
```
# usage
python app.py --help
usage: app.py [-h] -u USER

sam chat client

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  user help

# example
python app.py --user john
```
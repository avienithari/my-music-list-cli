# My Music List CLI
## Setup
You'll need .env file with your database credentials to use this tool:
```
$ touch .env
```
Inside of .env you'll need three variables:
```
USERNAME = your_username
HOSTNAME = your_hostname
PASSWORD = your_db_password
```
After providing credentials it's time to setup necessary tables for program to work:
```
python3 main.py

Mode: root

root> setup
```
## Usage
```
Modes:
  (l)ist    -  lists both tables 
  (r)andom  -  picks random band from planning table
  (s)earch  -  searches for band in both tables
  root      -  allows user to take control over tables
```

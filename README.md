# Agrosuite

## Installation

### Prerequisites

To run the project, the next packages must be installed:

- Python 2 (<https://www.python.org/downloads/>)

___

### Config and Run

1.- To run the project it's necessary to add the lib path of agrosuite client to the PYTHONPATH enviroment variable:

> `export PYTHONPATH=$PYTHONPATH:"~/agrosuite/lib"`

2.- Create a config file on the project folder:

> `cd <project_path> && touch config.ini`

You can use this template as an initial config:

```python
[ROUTES]
context = app
root    = login/redirect
login   = login
error   = error
host    = http://127.0.0.1:8282

[DATABASE]
host = 127.0.0.1
port = 3306
user = xxxx
password = xxxx
database = agrosuite

[TOKENS]
expires = 300

[MAIL]
host  = smtp.gmail.com
port  = 465
user  = wad.2016.pale@gmail.com
password = WebApplication
maxTries = 5
bufferSize = 5

[WEB]
theme = agrosuite

[SECURITY]
key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
```

4.- Run the project:

> `python run.py`

You should see now a login page on (<http://localhost:8282/app/login>)

*Welcome to the dark side, enjoy!*

___

## Post installation

After installation, you'll need to create and populate the database of the application.

1.- Before running the create script, make sure you added the correct credentials for your local mysql server on config.ini.

```python
[DATABASE]
host = 127.0.0.1
port = 3306
user = xxxx # Replace with your mysql username
password = xxxx # Replace with your mysql password
database = agrosuite
```

2.- After that, create the __agrosuite__ database.

3.- Then you're good to go running the create script at <http://localhost:8282/app/system/createdb>

> __Note:__ Avoid inserting a password with specialchars on the configuration file, if your root password has specialchars, we recommend creating a new user for this app. (this should be fixed on future releases)

You should see now the __agrosuite db__ populated.

4.- Now , you need to go running the population script at <http://localhost:8282/app/system/initdb>

___

## Cli agrosuite

python cli.py [-h]  [-v] command  action [-p PARAMETERS]

### Available commands

#### db
  - **create**
  - **init**
  - **delete**

#### add
use -p [Name] for the actual filename that will be created
  - **controller**
  - **model**
  - **theme**
  - **view**
  - **content**
  - **layout**

#### run

  - **debug**
  - **prod**


___

## JS models

Once your project was set up and running,

1.- Create your *Controller* with an *action*

2.- Inside your action add the **Model** you need

> self.addJsObject(**Model**)

3.- Then use it inside 'action.js' like this

>  var obj = new **modelName**Obj

4.- You'll available to manage your model with the next methods

- **load(id,callback,children=false)**
- **get(id,data,callback,children=false)**
- **select(data,callback,children=false)**
- **update(id,data,callback)**
- **insert(data,callback)**
- **delete (_id,callback)**
- **soft_delete(_id,callback)**
- **bulk_delete(list,callback)**

___

## Session

Exist Session class which is very useful when it comes to handle users Session

#### Session:

- ** Session.start(token) **

Start a new session for the user owner of the given token
token: valid token that identify the user and return session_id (sid)

- ** Session.end(sid) **

finish  the session identify with the sid given

sid: session_id which identify the hole session

- ** Session.set(sid,key,value) **

set the value which corresponds to the key and the sid given

- ** Session.get(sid,key) **

retive the value of the given key

- ** Session.remove(sid,key) **

remove the key stored in the session for the sid given


___

## i18n

pybabel extract -F **babel.cfg**  -o  **messages.pot** .

pybabel init -i **message.pot** -d [**translations**] -l [**languages**]

now it will be created under translations the language folder for example

> translations/es/LC_MESSAGES/messages.po

now this file is where you edit in order to put your translations, when you are done then you are good to go and run this:

pybabel compile -d [**translations**]

if you ever need to change something inside of .po files, feel free and then run this:

pybabel update -i [**messages.pot**] -d [**translations**]

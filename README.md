"# PFE_backend" 

Installation instructions:

* Install Python 3.11 from https://www.python.org/downloads/ (official website)
* Verify python is installed by using "python3 --version" or "python --version"
* Open project's root directory in a terminal
* Create the virtual environnement by using the command "pip -m venv venv"
* Activate the virtual environnement by using the command "./venv/Scripts/activate"
* "(venv)" must appear in the terminal at the beginning of the line
* Run "pip install -r requirements.txt"
* Run the last command : "wsgi.py" and enjoy :p

If you want to run the app in local you will need a .env file with these informations : 

```shell
JWT_SECRET = <yourSecretHere>
USER=<yourUserHere>
PASSWORD=<yourPasswordHere>
HOST=<yourHostHere>
DATABASE=<nameOfYourDatabaseHere>
```

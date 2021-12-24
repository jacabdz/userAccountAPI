# userAccountAPI
userAccountAPI logs all transactions and keeps track of the points an user has accumulated over time.

# Setup

userAccountAPI uses python 3.10 and Flask 2.0

First clonet the userAccountAPI repo.

Download and intall Python from https://www.python.org/

When Python 3 is installed, install Flask https://flask.palletsprojects.com/en/2.0.x/. Using a terminal at the project folder create a virtual environment using the following commands:

macOS/Linux `python3 -m venv venv`

Windows `py -3 -m venv venv`

Then activate the virtual environment using:

maxOS/Linux `venv/bin/activate`

Windows `venv\Scripts\activate`

Once in the virtual environment, install flask using pip: `pip install Flask`

Finally the server can be started with: `python app.py`


# Using the API

### addTransaction 
PUT method (id:int, payer:string, points:int)

addTransaction takes an id, the name of a payer and how many points will be added. This method uses the form data alongside with the current time to create a transaction at the corresponding account.

### checkBalance 
GET method (id:int)

checkBalance takes a key 'id' and and integer, and will return the point balance for the corresponding account in JSON format.

### spend 
PUT method (id:int, points:int)

spend takes an id for a corresponding account, and checks to see if the user has enough points to spend. If the user has enough points, the method then uses the accounts points up according to the rules set by accounting.

# Setup the project
### Installing and using the virtual environment for python is optional but recommended, to install, type: 
1. ```python -m venv ./path/for/venv/installation``` OR ```python -m venv c:\path\for\venv\installation``` in Powershell (using just the ```venv``` folder as installation path is easier though), instead of ```python```, you might need to use ```python3```, or ```py```, depending on your OS environment settings, check by typing ```python --version```, ```python3 --version```, and ```py --version``` and use one that points to python version 3. 

### Activate venv (from the project directory / parent directory of venv folder):
2. Type ```venv\Scripts\Activate``` in Powershell for activation, and type ```deactivate``` directly to deactivate it.
3. Type ```source .venv/Scripts/activate``` in bash for activation, and type ```deactivate``` directly to deactivate it.

### Installing the required packages:
4. Type ```pip install -r requirements.txt```, instead of ```pip```, you might need to use ```pip3```, depending on your OS environment settings, check both ```pip --version``` and ```pip3 --version``` and use one that points to pip xx.x.x (python 3.x).

# Launch the API server and access it from the browser:
1. Make sure you are in the ```quantmapi``` folder and you see ```manage.py``` file, if not, navigate to this directory and type: ```python manage.py runserver```. Again, you might need to use ```python3``` or ```py``` instead of ```python``` depending on your OS settings, whichever points to python version 3 should work. 
2. List all DB Entries / Add New Entry: ```http://127.0.0.1:8000/api/```
3. Update / Delete Specific DB Entry by Entry ID: ```http://127.0.0.1:8000/api/<entry_id_number>```, where the ```<entry_id_number>``` is an integred from 1 to infinity
4. Instrument Ticker / Symbol Data: ```http://127.0.0.1:8000/api/<ticker_symbol>```, from example: ```http://127.0.0.1:8000/api/BTCUSDT```
5. Intstrument Ticker / Symbol & Timeframe Data: ```http://127.0.0.1:8000/api/<ticker_symbol>/<timeframe_in_minutes>```, for example: ```http://127.0.0.1:8000/api/BTCUSDT/5```, ```http://127.0.0.1:8000/api/BTCUSDT/60``` or ```http://127.0.0.1:8000/api/ETHUSDT/1``` etc...


# Launch the service:
1. In order to launch the service in the background, just access the URL via browser or command line: ```http://127.0.0.1:8000/service/?ticker=<instrument_symbol>&interval=<interval_in_minutes>```, where ```<instrument_symbol>``` is ```BTCUSDT```, ```ETHUSDT```, ```LTCUSDT``` and so on... and ```<interval_in_minutes>``` is time as an integer number indicating candle time interval in minutes, could be one of 3 values: 1, 5, or 60 for 1 minute, 5 minutes, or 1 hour respectively. For example: ```http://127.0.0.1:8000/service/?ticker=ETHUSDT&interval=1```
2. Once the service is launched, it will continue running in the background, unless interrupted from the terminal window, where ```python manage.py runserver``` has been called previously. The browser window can be closed without affecting the background service. 
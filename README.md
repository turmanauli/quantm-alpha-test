# Setup the project
### Installing and using the virtual environment for python is optional but recommended, to install, type: 
1. ```python -m venv ./path/for/venv/installation``` OR ```python -m venv .\path\for\venv\installation``` in PowerShell. (using just the ```./venv``` ( or ```.\venv``` in PowerShell ) is good enough). Instead of ```python```, you might need to use ```python3```, or ```py```, depending on your OS environment settings, check by typing ```python --version```, ```python3 --version```, and ```py --version``` and use one that points to python version 3. 

### Activate venv (from the project directory / parent directory of venv folder):
1. Type ```venv\Scripts\Activate``` in Powershell for activation, and type ```deactivate``` directly to deactivate it.
2. Type ```source .venv/Scripts/activate``` in bash for activation, and type ```deactivate``` directly to deactivate it.

### Installing the required packages:
1. Type ```pip install -r requirements.txt```, instead of ```pip```, you might need to use ```pip3```, depending on your OS environment settings, check both ```pip --version``` and ```pip3 --version``` and use one that points to pip xx.x.x (python 3.x).

# Launch the API server and access it from the browser:
### Run the server:
1. Make sure you are in the ```quantmapi``` folder and you see ```manage.py``` file, if not, navigate to this directory and type: ```python manage.py runserver```. Again, you might need to use ```python3``` or ```py``` instead of ```python``` depending on your OS settings, whichever points to python version 3 should work. 
### Access API Endpoints:
1. OHLCV + MACD + RSI Endpoint: ```http://127.0.0.1:8000/api/<ticker_symbol>/<timeframe_in_minutes>```, for example: ```http://127.0.0.1:8000/api/BTCUSDT/5```, ```http://127.0.0.1:8000/api/BTCUSDT/60``` or ```http://127.0.0.1:8000/api/ETHUSDT/1``` etc...
2. RSI Endpoint: ```http://127.0.0.1:8000/api/<ticker_symbol>/<timeframe_in_minutes>/RSI```, for example ```http://127.0.0.1:8000/api/ETHUSDT/5/RSI```
3. MACD Endpoints: ```http://127.0.0.1:8000/api/<ticker_symbol>/<timeframe_in_minutes>/MACD```, for example ```http://127.0.0.1:8000/api/ETHUSDT/5/MACD```
### Miscelaneous Endpoints:
1. List all DB Entries / Add New Entry: ```http://127.0.0.1:8000/api/```
2. Update / Delete Specific DB Entry by Entry ID: ```http://127.0.0.1:8000/api/<entry_id_number>```, where the ```<entry_id_number>``` is an integer (index) of an enty (data row) in the database. 
3. Instrument Ticker / Symbol Data: ```http://127.0.0.1:8000/api/<ticker_symbol>```, from example: ```http://127.0.0.1:8000/api/BTCUSDT```


# Launch the service:
1. In order to launch the service in the background, just access the URL via browser or command line: ```http://127.0.0.1:8000/service/?ticker=<instrument_symbol>&interval=<interval_in_minutes>```, where ```<instrument_symbol>``` is ```BTCUSDT```, ```ETHUSDT```, ```LTCUSDT``` and so on... and ```<interval_in_minutes>``` is time as an integer number indicating candle time interval in minutes, could be one of 3 values: 1, 5, or 60 for 1 minute, 5 minutes, or 1 hour respectively. For example: ```http://127.0.0.1:8000/service/?ticker=ETHUSDT&interval=1```
2. Once the service is launched, it will continue running in the background, unless interrupted from the terminal window, where ```python manage.py runserver``` has been called previously. The browser window can be closed without affecting the background service. 
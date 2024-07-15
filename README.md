# quantm-alpha test task

## Setup and launch the project
### Installing and using the virtual environment for python is optional but recommended, to install, type: 
1. ```python -m venv ./path/for/venv/installation``` OR ```python -m venv c:\path\for\venv\installation``` in Powershell (using just the ```venv``` folder as installation path is easier though), instead of ```python```, you might need to use ```python3```, or ```py```, depending on your OS environment settings, check by typing ```python --version```, ```python3 --version```, and ```py --version``` and use one that points to python version 3. 

### Activate venv (from the project directory / parent directory of venv folder):
2. Type ```venv\Scripts\Activate``` in Powershell for activation, and type ```deactivate``` directly to deactivate it.
3. Type ```source .venv/Scripts/activate``` in bash for activation, and type ```deactivate``` directly to deactivate it.

### Installing the required packages:
4. Type ```pip install -r requirements.txt```, instead of ```pip```, you might need to use ```pip3```, depending on your OS environment settings, check both ```pip --version``` and ```pip3 --version``` and use one that points to pip xx.x.x (python 3.x).

### Launching the API web server and accessing from the browser:
5. Make sure you are in the ```quantmapi``` folder and you see ```manage.py``` file, if not, navigate to this directory and type: ```python manage.py runserver```. Again, you might need to use ```python3``` or ```py``` instead of ```python``` depending on your OS settings, whichever points to python version 3 should work. 
6. Access it from the browser by navigating to ```http://127.0.0.1:8000/api/```



Steps to Run:

1. download virtualenv for python:
 On Ubuntu: Run 
```$sudo apt install virtualenv```

2. Extract the contents of this folder to any folder and `cd` to it.

3. Next execute "virtualenv env"

4. Next execute "source env/bin/activate"

5. Now you should see "(env)" on the left most corner in the shell

6. Now execute "pip install flask tinydb paho-mqtt"

7. After all the modules get installed, run the command "python main.py &" which will run the MQTT listener service.

8. Now go ahead and run the command "python app.py" which will create open an web application on localhost:5000 by default.

9. Go ahead to browser and see the state logs.



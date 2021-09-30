# Application programming

## Lab4  
#### Deploying flask application on local Linux server/starting flask application using WSGI server  
  
* If you want to deploy this flask application on Linux server, you can find needed instructions here:   
  https://medium.com/swlh/deploy-flask-applications-with-uwsgi-and-nginx-on-ubuntu-18-04-2a47f378c3d2  
* To be able to run the application localy as a Python script using WSGI server follow next steps
  * Clone the repo:  
  `git clone https://github.com/IvanShkvir/application-programming.git`
  * Install all dependecies:  
  `pip install -r requirements.txt`  
  * Run `wsgi.py` file:  
  `python wsgi.py`
  * Go to `http://localhost:5000/` or `http://127.0.0.1:5000/` in your web browser.  

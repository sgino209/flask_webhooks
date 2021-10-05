# Flask with WebHook
Flask WebHook server for algo   
Reference:  https://medium.com/techfront/step-by-step-visual-guide-on-deploying-a-flask-application-on-aws-ec2-8e3e8b82c4f7
   
## Quick Start
### Virtual Environment
First time creation:   
```
python3 -m venv venv
```
Then (activation):   
```
source venv/bin/activate
```
   
### Local Run
Werkzeug’s development WSGI server, which forward requests from a web server:   
```
python app.py
```
   
### Production Run
Assumption:
- EC2 machine inbound traffic allowed on following ports (see Security Groups):
HTTP (Port 80)   
SSH (Port 22)   
HTTPS (Port 443)   

   
1. Apply Gunicorn (production-ready WSGI server) to serve the application:   
```
gunicorn -b 0.0.0.0:8000 app:app
```
   
2. Use the Systemd (boot manager for Linux) to manage Gunicorn:   
- Create a <projectname>.service file in /etc/systemd/system folder and specify what should happen to Gunicorn when system reboots.
- **Unit** part: a description about the project and some dependencies 
- **Service** part: specify user/group we want to run this service after. Also some information about the executables and the commands
- **Install** part: tells systemd at which moment during boot process this service should start
   
```
[Unit]
Description=Gunicorn instance for a simple hello world app
After=network.target
[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/<projectname>
ExecStart=/home/ubuntu/<projectname>/venv/bin/gunicorn -b localhost:8000 app:app
Restart=always
[Install]
WantedBy=multi-user.target
```
   
Then, enable the service:   
```
sudo systemctl daemon-reload
sudo systemctl start <projectname>
sudo systemctl enable <projectname>
```
3. Run Nginx WebServer to accept and route request to Gunicorn
Finally, set up Nginx as a reverse-proxy to accept the requests from the user and route it to gunicorn:   
- Install Nginx
```
sudo apt-get nginx
```
   
- Start the Nginx service and go to the Public IP address of your EC2 on the browser to see the default nginx landing page:
```
sudo systemctl start nginx
sudo systemctl enable nginx
```
- Edit the default file in the sites-available folder (/etc/nginx/sites-available/default) and add the following code:
```
upstream flaskhelloworld {
    server 127.0.0.1:8000;
}
```
- Add a proxy_pass to flaskhelloworld atlocation:
```
# Some code above
location / {
    proxy_pass http://flaskhelloworld;
}
# some code below
```
- Restart Nginx:
```
sudo systemctl restart nginx
```


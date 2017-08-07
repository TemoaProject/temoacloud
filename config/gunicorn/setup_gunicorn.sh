# DO NOT RUN THIS SCRIPT AS IS. PLEASE GO THROUGH EACH STEP AND RUN AS REQUIRED AFTER EDITING
#1. Change [user] in config/gunicorn/gunicorn.service to the one which will run the server

#2. Copy config/gunicorn/gunicorn.service to /etc/systemd/system/
sudo cp config/gunicorn/gunicorn.service /etc/systemd/system/

#3. Make sure the permissions of the /srv/ directory is - owner = user(which runs the server, for example utemoa or yash) and group = www-data IMPORTANT!!
sudo chown -R utemoa:www-data /srv/

#4. Change IP Address in ALLOWED_HOSTS in dproject/settings.py as requried

#5. Run gunicorn service
sudo systemctl start gunicorn

#6. Check if the service is running
sudo systemctl status gunicorn

#7. After this, dproject.sock should be created in /srv/ directory (or the main project directory, whichever it is)
ls /srv/dproject.sock

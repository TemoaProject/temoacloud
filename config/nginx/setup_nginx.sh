# DO NOT RUN THIS SCRIPT AS IS. GO THROUGH ALL THE STEPS AND RUN AS REQURIED AFTER EDITING
#1. Edit IP Address in config/nginx/dproject as required

#2. Copy config/nginx/dproject to /etc/nginx/sites-available/
sudo cp config/nginx/dproject /etc/nginx/sites-available/

#3. Create a link in /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/dproject /etc/nginx/sites-enabled/

#4. 
sudo ufw allow 'Nginx Full'

#5. Start Nginx server
sudo systemctl start nginx 
# or sudo nginx

#6. Check if the nginx is running default configuration of dproject config by opening server address (in browser)

#7. If nginx is running default configuration. - remove default configuration from enabled sites
sudo rm /etc/nginx/sites-enabled/default

#8. Restart nginx
sudo systemctl restart nginx

#9. Check status of nginx to see if it ran successfully
sudo systemctl status nginx

#9. If required restart gunicorn and nginx again
sudo systemctl restart gunicorn
sudo systemctl restart nginx

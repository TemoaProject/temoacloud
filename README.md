#Ubuntu based settings

## Required


    sudo apt-get install libblas-dev liblapack-dev libatlas-base-dev gfortran graphviz

    pip  --user install django numpy scipy pyomo pyomo.extras  
	
	wget http://ftp.gnu.org/gnu/glpk/glpk-4.60.tar.gz
	tar -xvz glpk-4.60.tar.gz
	./configure
	make
	sudo make install
	
	or
	
	sudo apt-get install glpk-utils



We will update this more


## For twilio

    sudo apt-get install postgresql-9.5  postgresql-server-dev-9.5

    pip install --user -r requirements.txt


set password and create db for postgresql

    sudo -u postgres psql postgres
	\password postgres
	
	CREATE DATABASE browser_calls;


# Twilio setup steps

    source .env

    python manage.py migrate

    python manage.py createsuperuser

    python manage.py runserver

    ngrok 8000

    sudo npm install -g localtunnel

    lt --port 8000 --subdomain yash

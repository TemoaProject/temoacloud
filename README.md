The default branch for this repository is "merged"

# INIT
* Clone repo
* Init submodules - git submodule init
* git pull --recurse-submodules && git submodule update --recursive
* cd thirdparty/temoa
* git checkout v3

#Ubuntu based settings

## Required
sudo apt-get install libblas-dev liblapack-dev libatlas-base-dev gfortran graphviz

pip install django==1.9.6 numpy scipy pyomo==4.3.11388 pyomo.extras xlrd xlwt xlutils ipython psycopg2

wget http://ftp.gnu.org/gnu/glpk/glpk-4.60.tar.gz
tar xvzf glpk-4.60.tar.gz
cd glpk-4.60
./configure
make
sudo make install
sudo ldconfig

pip install glpk

We will update this more

./manage.py runserver --noreload --nothreading

## DB
sudo passwd postgres
sudo -u postgres -i

CREATE USER temoauser WITH PASSWORD 'random@123$#%password';

ALTER ROLE temoauser SET client_encoding TO 'utf8';
ALTER ROLE temoauser SET default_transaction_isolation TO 'read committed';
ALTER ROLE temoauser SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE temoa TO temoauser;

# RUN DB
./manage.py migrate dapp zero
./manage.py migrate


# TO RESET
- sudo su - postgres
- psql
- postgres=# drop database temoa;
- postgres=# create database temoa;
- postgres=# GRANT ALL PRIVILEGES ON DATABASE temoa TO temoauser;

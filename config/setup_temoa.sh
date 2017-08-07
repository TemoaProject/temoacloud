#Install Python 2.7.13

# Installing dependencies:
sudo apt-get install build-essential checkinstall
sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev

#Download, configure and install python2.7
cd ~
version=2.7.13
wget https://www.python.org/ftp/python/$version/Python-$version.tgz

tar -xvf Python-$version.tgz
cd Python-$version
./configure
make
sudo checkinstall

# Install pip
sudo apt-get install python-pip


# Set up temoa code
cd /srv/
git clone https://github.com/TemoaProject/dapp.git .
git checkout merged
cd thirdparty/temoa
git submodule init
git submodule update
git checkout energysystem
cd ../../


#Install virtualenv package
sudo apt-get install virtualenv

#Set up virtual env
cd /srv/
virtualenv tprojectenv

sudo -i
cd /srv/
source tprojectenv/bin/activate


#Install requried python packages in virtual environment
apt-get -f install
sudo apt-get install libblas-dev liblapack-dev libatlas-base-dev gfortran graphviz

pip install django==1.9.6 numpy scipy pyomo==4.3.11388 pyomo.extras xlrd xlwt xlutils ipython psycopg2

pip install matplotlib pandas
pip install gunicorn

sudo apt-get install nginx


# Install glpk solver
wget http://ftp.gnu.org/gnu/glpk/glpk-4.55.tar.gz
tar xvzf glpk-4.55.tar.gz
cd glpk-4.55
./configure
make
sudo make install
sudo ldconfig


# Install Cbc Coin-OR solver
wget https://www.coin-or.org/download/binary/Cbc/Cbc-2.4.0-linux-x86_64-gcc4.3.2-parallel.tgz
tar -xvf Cbc-2.4.0-linux-x86_64-gcc4.3.2-parallel.tgz
cd Cbc-2.4.0-linux-x86_64-gcc4.3.2-parallel/
cd bin
sudo cp cbc /usr/local/bin



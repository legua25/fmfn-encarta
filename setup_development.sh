
sudo apt-get install build-essential mysql-server-5.6 python-dev libmysqlclient-dev python-pip
sudo pip install virtualenv
sudo pip install virtualenvwrapper
echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc
source ~/.bashrc
mkvirtualenv fmfn_encarta
workon fmfn_encarta
pip install -r requirements.txt
pip install git+https://github.com/jezdez/django-configurations.git
mysql -u root -p
##  Manual Commands as of now: ##
# CREATE DATABASE fmfn;
# CREATE USER 'fmfn_user'@'localhost' IDENTIFIED BY 'VHSBLnRquEFyPAbZ';
# GRANT ALL PRIVILEGES ON fmfn.* TO 'fmfn_user'@'localhost' WITH GRANT OPTION;
# FLUSH PRIVILEGES;
echo "Manual commands needed to setup the required database, check comments on this file"


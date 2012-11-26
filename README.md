publisher
=========

Use to publish app.

rpm -Uvh http://dl.fedoraproject.org/pub/epel/5/i386/epel-release-5-4.noarch.rpm
yum install git
ssh-keygen -C 'lorry.le@gmail.com' -t rsa
\n\n\n
git config --global user.name 'linode-nj-lorry'
git config --global user.email 'lorry.le@gmail.com'
mkdir /webservers
cd /webservers
git init
mkdir /webservers/publisher
git clone https://github.com/lorry-lee/publisher.git /webservers/publisher
wget https://www.djangoproject.com/m/releases/1.2/Django-1.2.7.tar.gz
tar xzvf Django-1.2.7.tar.gz
cd Django-1.2.7
python setup.py install
yum install mysql-server
yum install libmysqld-dev libmysqlclient-dev fail
yum install python-dev fail
yum install python-setuptools
easy_install "MySQL-python==1.2.3" fail
yum install MySQL-python
yum install python-pip
easy_install pip
yum install gcc
pip install PIL fail
cd ..
rm -rf Django-1.2.7
wget http://pypi.python.org/packages/source/d/django-photologue/django-photologue-2.3.tar.gz
tar xzvf django-photologue-2.3.tar.gz
cd django-photologue-2.3
python setup.py install
cd ..
rm -rf django-photologue-2.3
cd publisher
mysql -uroot < createmysql.sql
python manage.py syncdb --noinput
apt-get install nginx
apt-get install uwsgi
y\n
apt-get install uwsgi-plugin-python
cp www /etc/nginx/sites-enabled
cp www.ini /etc/uwsgi/apps-enabled
service uwsgi restart
service nginx restart
nginx -s reload


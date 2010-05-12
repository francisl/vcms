#!/bin/bash

case $1 in
    "2.4")
        python_version=2.4
        ;;
    "2.5")
        python_version=2.5
        ;;
    "2.6")
        python_version=2.6
        ;;
    *)
        echo "---ERROR --- INVALID PARAMETERS $@"
        echo "- Using default python-2.5 - "
        python_version=2.5
        ;;
esac

python_cmd=python$python_version
easy_install_cmd=easy_install-$python_version


# install SATCHMO dependencies
echo "-----------PyCRYPTO---------"
easy_install pycrypto
echo "-----------REPORTLAB---------"
easy_install reportlab
echo "-----------TRML2PDF---------"
easy_install http://www.satchmoproject.com/snapshots/trml2pdf-1.2.tar.gz
echo "-----------DJANGO-REGISTRATION---------"
easy_install django-registration
echo "-----------PyYAML---------"
easy_install PyYAML

echo "-----------DJANGO-THREADED-MULTIHOST---------"
hg clone https://bkroeze@bitbucket.org/bkroeze/django-threaded-multihost/ django-threaded-multihost
cd django-threaded-multihost
$python_cmd setup.py install
cd ..
rm -rf django-threaded-multihost/

echo "-----------DJANGO-APP-PLUGINS---------"
svn checkout http://django-app-plugins.googlecode.com/svn/trunk/ django-app-plugins-read-only
cd django-app-plugins-read-only
$python_cmd setup.py install
cd ..
rm -rf django-app-plugins-read-only/

echo "-----------DJANGO-SIGNALS-AHOY---------"
hg clone http://bitbucket.org/bkroeze/django-signals-ahoy/ django-signals-ahoy
cd django-signals-ahoy
$python_cmd setup.py install
cd ..
rm -rf django-signals-ahoy/

echo "-----------DJANGO-LIVESETTINGS---------"
hg clone http://bitbucket.org/bkroeze/django-livesettings django-livesettings
cd django-livesettings
$python_cmd setup.py install
cd ..
rm -rf django-livesettings/

echo "-----------DJANGO-KEYEDCACHE---------"
hg clone http://bitbucket.org/mmarshall/django-keyedcache django-keyedcache
cd django-keyedcache
$python_cmd setup.py install
cd ..
rm -rf django-keyedcache/

echo "-----------SATCHMO---------"
hg clone http://bitbucket.org/chris1610/satchmo/ satchmo-trunk
cd satchmo-trunk
$python_cmd setup.py install
cd ..
rm -rf satchmo-trunk




# OPTIONAL FOR DOCUMENTATION

#echo "-----------SPHINX---------"
# $easy_install_cmd Sphinx
#echo "-----------DOCUTILS---------"
# $easy_install_cmd docutils


. ./dep_config.sh

echo "----------- DJANGO-CSS ---------"
mkdir insttemp
cd insttemp
git clone http://github.com/dziegler/django-css.git
cd django-css
$PYTHON_SETUP_INSTALL_CMD
cd ../..
rm -rf insttemp

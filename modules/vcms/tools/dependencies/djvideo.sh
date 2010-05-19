. ./dep_config.sh

echo "-----------DJANGO-APP-PLUGINS---------"
git clone http://git.participatoryculture.org/djvideo/
cd djvideo
cp -rf djvideo/ $INSTALL_PATH
cd ..
rm -rf djvideo/
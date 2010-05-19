. ./dep_config.sh

echo "----------- DJVIDEO ---------"
mkdir insttemp
cd insttemp
git clone http://git.participatoryculture.org/djvideo/
cd djvideo
cp -rf djvideo/ $INSTALL_PATH
cd ../..
rm -rf djvideo/

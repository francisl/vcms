. ./dep_config.sh

echo "----------- BEAUTIFUL-SOUP ---------"
mkdir insttemp
cd insttemp
curl -O "http://www.crummy.com/software/BeautifulSoup/download/3.x/BeautifulSoup-3.0.8.1.tar.gz"
tar -zxf BeautifulSoup-3.0.8.1.tar.gz
cd BeautifulSoup-3.0.8.1
$PYTHON_SETUP_INSTALL_CMD
cd ../..
rm -rf insttemp

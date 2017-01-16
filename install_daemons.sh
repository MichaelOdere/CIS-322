#/bin/bash

repository="https://github.com/postgres/postgres.git"
branch="REL9_5_STABLE"
git clone -b $branch $repository
cd postgres
./configure --prefix=$1
make
make install

cd ..

# Download apache
link=http://www-us.apache.org/dist//httpd/httpd-2.4.25.tar.gz
curl -o apache-2-4-25.tar.gz $link
tar xzf apache-2-4-25.tar.gz
cd httpd-2.4.25
./configure --prefix=$1
make
make install

#/bin/bash

repository="https://github.com/postgres/postgres.git"
branch="REL9_5_STABLE"
echo "Cloning $branch version of postgres"
git clone -b $branch $repository
cd postgres
./configure prefix=$1
make
install

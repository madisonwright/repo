git clone git@github.com:postgres/postgres.git
cd /home/osnapdev/postgres
git checkout -b REL9_5_STABLE origin/REL9_5_STABLE
./configure --prefix=/home/osnapdev/
make
make install
cd ..
curl -o http://mirrors.gigenet.com/apache//httpd/httpd-2.4.25.tar.gz
tar -xjf httpd-2.4.25.tar.bz2
./configure --prefix=/home/osnapdev/
make
make install
cd /home/osnapdev/conf
vi httpd.conf
Listen 8080

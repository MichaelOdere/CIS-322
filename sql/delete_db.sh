#bin/bash

#/home/osnapdev/bin/pg_ctl -D /home/osnapdev/data/ -l logfile stop
#/home/osnapdev/bin/pg_ctl -D /home/osnapdev/data/ -l logfile start
#sleep 1s 
echo "deleting old  db..."
/home/osnapdev/bin/dropdb lost_db
echo "creating new db..."
/home/osnapdev/bin/createdb lost_db
/home/osnapdev/bin/psql -d lost_db -a -f create_tables.sql
python product_insert.py lost_db 5432
/home/osnapdev/bin/psql lost_db

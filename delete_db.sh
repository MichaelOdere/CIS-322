apachectl restart

dropdb lost_db
createdb lost_db
bash preflight.sh lost_db

python fake_data.py

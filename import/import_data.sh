if [ "$#" -ne 2 ]; then
        echo "Usage: bash ./import_data.sh <dbname> <output dir>"
        exit;
fi

python import_data.py $1 $2














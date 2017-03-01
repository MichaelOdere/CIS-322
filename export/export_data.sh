if [ "$#" -ne 2 ]; then
        echo "Usage: bash ./export_data.sh <dbname> <output dir>"
        exit;
fi

python export_data.py $1 $2


#/bin/bash

link=https://classes.cs.uoregon.edu//17W/cis322/files/osnap_legacy.tar.gz
curl -O $link
tar xzf osnap_legacy.tar.gz
tar xzf osnap_legacy.tar.gz
python product_insert.py $1 $2
rm osnap_legacy.tar.gz
rm -r osnap_legacy

# Aquire data from NJIT's parking data site

To use these scripts first insert all SQL/DB credentials in these 
files. Move all of these files into `/opt/parking/`. Then log 
into your SQL server and create te table defined in `parking.py`. 
If you'd like you can import all of the old data by running 
`reload_parking.py` from python2. Setup a cronjob that runs 
`parking.py` from python2. You can then run one of the PHP files 
to pull data out and plot it.

## downloadlastmonth.php

Turn the last month (30 days) of data into a CSV file written to 
stdout.

## downloadlastweek.php

Turn the last week (7 days) of data into a CSV file written to stdout.

## makecsv.php

Turn the entire DB of data into a CSV file written to stdout. 
Don't run this.

## parking.py (python2)

Fetch data from http://mobile.njit.edu/parking/

## reload_parking.py (python2)

Load all of the archived JSON files, from data/, into the database.

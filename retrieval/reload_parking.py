from sqlalchemy import create_engine
from datetime import datetime
from gzip import open as gzopen
from glob import glob
from json import loads
import requests
import time

engine = create_engine('')

# Table Used: CREATE TABLE NJITParking (deck VARCHAR(30), available INT, occupied INT, total INT, entered TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

def main():

	#2017-10-04 17:01:01
	for file in glob('/opt/parking/data/*.json.gz'):
		occurred = datetime.strptime(file, '/opt/parking/data/%Y-%m-%d_%H-%M-%S.json.gz')

		if occurred >= datetime(2017, 10, 4, 17, 1, 1):
			continue

		with gzopen(file, 'rt') as o:
			decks = loads(o.read())['decks']
			print(decks)
			with engine.connect() as db:
				for d in decks:
					deck      = decks[d]['SiteName']
					available = int(decks[d]['Available'])
					occupied  = int(decks[d]['Occupied'])
					total     = int(decks[d]['Total'])

					db.execute("""INSERT INTO NJITParking (deck,available,occupied,total,entered)
							VALUES (%s, %s, %s, %s, %s);""", (deck, available, occupied, total, occurred))


if __name__ == "__main__":
	main()

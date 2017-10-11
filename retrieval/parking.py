from sqlalchemy import create_engine
from gzip import open as gzopen
import requests
import time

engine = create_engine('')

# Table Used: CREATE TABLE NJITParking (deck VARCHAR(30), available INT, occupied INT, total INT, entered TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

def main():
	r = requests.get('http://mobile.njit.edu/parking/data.php', headers={
		'Referer': 'http://mobile.njit.edu/parking/',
		'Origin': 'http://mobile.njit.edu/'
	})
	current_time = time.strftime('%Y-%m-%d_%H-%M-%S')

	if not r:
		print "[{}] Failed to connect".format(current_time)
		return
	else:
		print "[{}] Connected".format(current_time)

	with gzopen('/opt/parking/data/{}.json.gz'.format(current_time), 'wt') as o:
		o.write(r.text)

	decks = r.json['decks']

	with engine.connect() as db:
		for d in decks:
			deck      = decks[d]['SiteName']
			available = int(decks[d]['Available'])
			occupied  = int(decks[d]['Occupied'])
			total     = int(decks[d]['Total'])

			db.execute("INSERT INTO NJITParking (deck, available, occupied, total) VALUES (%s, %s, %s, %s);", (deck, available, occupied, total))


if __name__ == "__main__":
	main()

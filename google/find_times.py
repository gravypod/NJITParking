from csv import DictReader
import requests

from sqlalchemy import create_engine

engine = create_engine('')

# Table Used: CREATE TABLE GoolglePathLength (name VARCHAR(30), seconds INT, entered TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

API="..."
URL="https://maps.googleapis.com/maps/api/directions/json?mode=driving&origin={fromloc:}&destination={toloc:}&key={API:}"


def find_rout_length(from_location, to_location):
	r = requests.get(URL.format(fromloc=from_location, toloc=to_location, API=API))

	if not r:
		return None

	data = r.json

	return int(data['routes'][0]['legs'][0]['duration']['value'])

def main():
	with open("lookups.csv") as i, engine.connect() as db:
		for path in DictReader(i, delimiter='|'):
			from_location = path['from'].replace(" ", "+")
			to_location = path['to'].replace(" ", "+")

			try:
				path_time_seconds = find_rout_length(from_location, to_location)
			except:
				continue

			db.execute("INSERT INTO GoolglePathLength (name, seconds) VALUES (%s, %s);", (path['name'], path_time_seconds))

if __name__ == "__main__":
	main()
